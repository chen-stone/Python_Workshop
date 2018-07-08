# coding=utf-8


class Test:
    def __init__(self, ip1, ip2="ip2"):
        self.tp1 = "tp1"
        self.tp2 = "tp2"
        ip3 = "ip3"
        diobj.log()

    def run(self, rp1, rp2="rp2"):
        self.tp1="trp1"
        rp3 = "rp3"
        diobj.log()
        try:
            1/0
        except ZeroDivisionError:
            diobj.log()
        1/0


def amhp(ap1, ap2="ap2"):
    ap3 = "ap3"
    diobj.log()
    try:
        1/0
    except:
        diobj.log()
        pass
    # 1/0
    pass


def f3(f3p1, f3p2="f3p2"):
    f3p3 = "f3p3"
    amhp(f3p3)


def f2(f2p1, f2p2="f2p2"):
    f2p3 = "f2p3"
    f3(f2p3)


def f1(f1p1, f1p2="f1p2"):
    f1p3 = "f1p3"
    f2(f1p3)


if __name__ == "__main__":
    # A little bit background work.
    import sys
    pkgpath = __file__[:__file__.find("test")]
    if pkgpath not in sys.path:
        sys.path.append(pkgpath)
    # Beginning test...
    import getdiaginfo
    diobj = getdiaginfo.enable(out2scn=True)
    # Testing function diagnosis information log: just log, except branch log.
    f1("f1p1")
    # Testing class diagnosis information log: just log, except branch log and raised exception.
    t = Test("from main")
    t.run("from main")
    print "End of test."


