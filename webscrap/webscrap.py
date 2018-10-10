# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urlparse import urljoin
import chardet
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import bs4
from langconv import *
import numbermap
import re
import auxtools
import getdiaginfo
dobj = getdiaginfo.enable(conloglevel="log")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RefineArticle:
    def __init__(self, artcname=None, webaddr=None, webtype="outline", **kwargs):
        self.artcname = artcname.decode("utf-8")
        if isinstance(webaddr, list):
            self.webaddrs = webaddr
        elif isinstance(webaddr, str):
            self.webaddrs = [webaddr]
        else:
            raise Exception("Wrong web address input...")
        self._webtype = webtype
        self._chapt = dict()
        # New beginning...
        self.__validchptpapa = {"div": ["class", "id"], "table": ["class", "id"]}
        self.__daelemblks = dict()
        self.__dblkscores = dict()
        self.__contents = []
        self.__rechp = re.compile(ur"第[一二三四五六七八九十\d]+章|第[一二三四五六七八九十\d]+节|^\d{1,5}")
        self.__requestsparas = {"headers":
                                    {'content-type': 'application/json',
                                     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/67.0.3396.59 Mobile/15E302 Safari/604.1'},
                                "verify": False}
        self.__randomuseragent = UserAgent()
        self.__excludetag = ["script"]
        self.__notcntpapa = ["p", "br"]
        self.__dchptcntscores = {}
        if kwargs:
            self.__requestsparas.update(kwargs)

    def __del__(self):
        self.artcname = self.webaddr = self._chapt = None

    def __diff_web_type(self, sp):
        # Todo: fulfill the function
        return self._webtype

    def __gather_chpts_urls(self, baseurl, sp):
        for chpthrefelem in sp.find_all("a"):
            if "href" in chpthrefelem.attrs:
                daelemhref = (Converter('zh-hans').convert(chpthrefelem.text.strip()),
                              self.__validate_url(baseurl, chpthrefelem["href"]))
                chpthrefathername = self.__find_chpturl_father(chpthrefelem)
                self.__daelemblks.setdefault(chpthrefathername, []).append(daelemhref)

    def __find_chpturl_father(self, chpthrefelem):
        # Todo Need to be modified...
        for father in chpthrefelem.parents:
            if father.name in self.__validchptpapa:
                fatherattrs = [attr + "=" + str(father[attr]) for attr in father.attrs if
                               attr in self.__validchptpapa[father.name]]
                return father.name + ": " + ", ".join(fatherattrs)
        return "Unclassified"

    def __validate_url(self, baseurl, orginurl):
        return urljoin(baseurl, orginurl)

    def __calc_a_blk_score(self):
        for blk in self.__daelemblks:
            aelemcntsc = self.__calc_a_number_score(blk)
            aelemnamesc = self.__calc_a_name_score(blk)
            self.__dblkscores.setdefault(aelemcntsc+aelemnamesc, []).append(blk)
        return max(self.__dblkscores.keys())

    def __calc_a_number_score(self, blk):
        acntscore = 0
        acnt = len(self.__daelemblks[blk])
        if acnt <= 5:
            acntscore = 10
        elif acnt <= 10:
            acntscore = 50
        elif 10 < acnt <= 20:
            acntscore = 60
        elif 20 < acnt <= 30:
            acntscore = 80
        elif acnt > 30:
            acntscore = 100
        return acntscore

    def __calc_a_name_score(self, blk):
        chpcnt = 0
        for danamehref in self.__daelemblks[blk]:
            if self.__rechp.search(danamehref[0]):
                chpcnt += 1
        return round(chpcnt/float(len(self.__daelemblks[blk])), 1)*100

    def __get_chapters_content(self, bestblks):
        for bestblk in self.__dblkscores[bestblks]:
            totalchp = len(self.__daelemblks[bestblk])
            dobj.briefing(contents=self.__daelemblks[bestblk])
            getchpprogress = auxtools.ProgressBar("Begin to get every chapter")
            for pos, blkchapter in enumerate(self.__daelemblks[bestblk]):
                getchpprogress(pos+1, totalchp)
                self.__contents.append((blkchapter[0], self.__strip_chpt_content(blkchapter[1])))
        with open(u"D:\\wstmp.txt", "w") as fp:
            [fp.write("\n".join(cp).encode("utf-8")) for cp in self.__contents]

    def __strip_chpt_content(self, curl):
        dcontentblks, self.__dchptcntscores = dict(), dict()
        sp = self.__requests_get_with_paras(curl.encode("utf-8"))
        lenchapterweb = len(sp.text)
        for txtelem in sp.descendants:
            if isinstance(txtelem, bs4.NavigableString) and txtelem.parent.name not in self.__excludetag:
                papa = txtelem.parent
                while papa.name in self.__notcntpapa:
                    papa = papa.parent
                papaname = papa.name + str(papa.attrs)
                dcontentblks.setdefault(papaname, []).append(self.__analysis_text(txtelem, papaname, lenchapterweb))
        self.__dchptcntscores = {v: k for k, v in self.__dchptcntscores.items()}
        return u"".join(dcontentblks[self.__dchptcntscores[max(self.__dchptcntscores.keys())]])

    def __analysis_text(self, txtelem, papaname, totallen):
        self.__dchptcntscores[papaname] = self.__dchptcntscores.get(papaname, 0) + 0.1 + len(txtelem) * 100 / totallen
        return self.__adjust_content(txtelem)

    def __adjust_content(self, content):
        # Removing continues black line
        content = re.sub(ur"\r?\n\s*\n?", ur"", content)
        return Converter('zh-hans').convert(content.rstrip() + u"\n") if content else ""

    def __requests_get_with_paras(self, url):
        self.__requestsparas["headers"].update({'User-Agent': self.__randomuseragent.random})
        respcontent = requests.get(url, **self.__requestsparas).content
        detset = chardet.detect(respcontent)["encoding"].lower()
        encodeset = detset if detset not in auxtools.dwebcharsetmap else auxtools.dwebcharsetmap[detset]
        return BeautifulSoup(respcontent, features="html.parser", from_encoding=encodeset)

    def scrap_contents(self):
        while self.webaddrs:
            curl = self.webaddrs.pop()
            sp = self.__requests_get_with_paras(curl)
            webtype = self.__diff_web_type(sp)
            if webtype == "outline":
                self.__gather_chpts_urls(curl, sp)
                bestblks = self.__calc_a_blk_score()
                self.__get_chapters_content(bestblks)
            elif webtype == "explore":
                pagetitle = Converter('zh-hans').convert(sp.title.string)
                # print sp.title.string
                if self.artcname in pagetitle and pagetitle not in self._chapt:
                    self._chapt[pagetitle] = self._get_chapt(sp)
                    self._gather_href(curl, sp)
            else:
                raise Exception("Unknown web type, can't handle it!")
        # with open(u"D:\\wstmp.txt", "w") as fp:
        #     [fp.write(self._chapt[cp].encode("utf-8")) for cp in sorted(self._chapt)]

    def _get_chapt(self, sp):
        maxcnt, content = 0, ""
        for elem in sp.descendants:
            if isinstance(elem, bs4.element.NavigableString):
                elem = Converter('zh-hans').convert(elem)
                if len(elem) > maxcnt:
                    maxcnt, content = len(elem), elem
        return content

    def _gather_href(self, curl, sp):
        for a in sp.find_all("a"):
            acontent = Converter('zh-hans').convert(a.string) if a.string else ""
            if (self.artcname in acontent and acontent not in self._chapt) or u"下一章" in acontent:
                url = curl + a["href"] if "http" not in a["href"] else a["href"]
                self.webaddrs.append(url)


if __name__ == "__main__":
    import time
    t0 = time.time()
    ra = RefineArticle("王国血脉", r"https://www.piaotian.com/html/8/8484/index.html")
    # ra = RefineArticle("王国血脉", r"https://book.qidian.com/info/1003586227#Catalog")
    # ra = RefineArticle("廖雪峰", r"https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
    ra.scrap_contents()
    print "\ntotal time is ", time.time() - t0, " seconds"
