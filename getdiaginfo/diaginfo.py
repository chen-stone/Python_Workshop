# coding=utf-8
"""Collecting and logging diagnosis information for problem locating and solving.

Written by Chen Dexing, Email chendexing@gmail.com
    
Limitations:
    1. Must called by package, or there will be a problem about locating problem failed.
    2. Delimiter in file has some problem.
       -Solved. Consuming a little bit more time.

Example of Diagnosis information output: 
    ********************************Begin********************************
    #Those information below is show in screen and file at the same time.
    Description: xxx
    Process ID:  xxx
    Process Name:   xxx
    Exception Type: xxx
    Function Name:  xxx
    Function's File:    xxx
    Error Code Line:
        line1
        line2 -Error line1
        line3
    Call Chain:
        F1 in line xxx, file xxx   
        F2 in line xxx, file xxx 
        ...  
        Fn in line xxx, file xxx 
    #Those information below is only recorded in file.
    Function-latest
        Locals:
            p1=xxx
            p2=xxx
            ...
            pn=xxx
        globals:
            gp1=xxx
            gp2=xxx
            ...
            gpn=xxx
    Funtion-the beginner of call chain.
        Locals:
            p1=xxx
            p2=xxx
            ...
            pn=xxx
        globals:
            gp1=xxx
            gp2=xxx
            ...
            gpn=xxx
    *********************************End*********************************
"""

import multiprocessing
import os
import sys
import time
import traceback
import inspect
import linecache
import infoelereg
import fmtoutput

if __debug__:
    import cgitb
    #cgitb.enable(format="text")


class DiagException(Exception):
    """Throw an exception manually if necessary.

    When there is no exception when diagnosis information is needed. use it.
    """
    pass


def _diag_elements_register():
    """Defining output information elements and their orders.

    Only used in __init__ method.
    """
    lbco = infoelereg.lbriefelereg
    ldfo = infoelereg.ldetailelereg
    return lbco, ldfo


class DiagInfo(object):
    """Collecting and outputting diagnosis information when needed.

    There are two usages:
        1. Registering python's default exception handler by __call__ method.
        2. Using DiagInfo's log method to log specified diagnosis information.
    Example:
        diobj = DiagInfo(logdir="D:\\")
        sys.excepthook = diobj  # Registering python's default exception handler.
        di.log()    # logging diagnosis information at certain location.
    """

    def __init__(self, logdir=None, out2scn=True, excdvars=[], incdvars=[]):
        """Constructor for DiagInfo class.

        Initializing parameters for object of this class.
        """
        self.__logdir = logdir  # Directory of logging file.
        self.__dinfo = None  # Storing diagnosis information, be initialized in log method.
        self.__lbrief, self.__ldetail = _diag_elements_register()
        self.__out2scn = out2scn  # Switch control output in screen or not.
        self.__excdvars = excdvars  # Dumping all variables except those in __excdvars list.
        self.__incdvars = incdvars  # Dumping the specified variables in __incdvars list.
        self.__dexp = dict()
        self.__dexpitem = ["etype", "evalue", "tb", "sehandler"]
        self.__logfp = self.__create_log_file() if self.__logdir else None  # Creating logging file.

    def __del__(self):
        """Deconstructor.

        Releasing resources.
        """
        self.__dexp.clear()
        if self.__logfp:
            self.__logfp.close()

    def __call__(self, etype, evalue, tb):
        """Magic function of class makes object can be used like a function.

        Using this feature to instead of system's exception handler.
        Example:
            diobj = DiagInfo(logdir="D:\\")
            sys.excepthook = diobj  # Registering python's default exception handler.
        """
        self.__dexp = dict(zip(self.__dexpitem, [etype, evalue, tb, True]))
        self.log()

    def __create_log_file(self):
        """Creating log file if log file directory is specified in method __init__.

        File name is just like "DiagInfo_06.16-17h55m05s.log"
        """
        filename = "".join(["DiagInfo_cdx", 
                            ".log"])
        return open(os.path.join(self.__logdir, filename), "w")

    def log(self, desp="", excdvars=[], incdvars=[]):
        """Logging diagnosis information and outputting it.

        Printing brief information in console and detail information in log file.
        Example:
            di = DiagInfo(logdir="D:\\")
            di.log()
        """
        excdvarsbak = len(self.__excdvars)
        incdvarsbak = len(self.__incdvars)
        self.__excdvars.extend(excdvars)
        self.__incdvars.extend(incdvars)

        self.__dinfo = dict()
        self.__dinfo["Begin"] = "".join(["\n"*3, "*"*42, "Begin", "*"*42])
        self.__dinfo["End"] = "".join(["*"*42, "End", "*"*42])   
        self.__dinfo["User Description"] = desp

        self.__collect_diag_info()
        self.__fmt_output()

        self.__excdvars = self.__excdvars[:excdvarsbak]
        self.__incdvars = self.__excdvars[:incdvarsbak]
        self.__dexp = {}

    def __fmt_output(self):
        """Defining format of output information.

        Only used in log method. No further use.
        """
        [fmtoutput.dftfuncmap[label]([self.__out2scn, None], label, self.__dinfo[label]) for label in self.__lbrief]
        [fmtoutput.dftfuncmap[label]([False, self.__logfp], label, self.__dinfo[label]) for label in self.__ldetail]

    def __collect_diag_info(self):
        """Collecting diagnosis information.

        Only called by log method.
        If there is no exception happened, raising DiagException for information gathering.
        """
        # Gathering process information.
        self.__get_proc_info()
        if not self.__dexp:
            try:
                etype, evalue, tb = sys.exc_info()
                if not etype:
                    try:
                        raise DiagException("No exception happened, for gathering information.")
                    except DiagException:
                        etype, evalue, tb = sys.exc_info()
                self.__dexp = dict(zip(self.__dexpitem, [etype, evalue, tb, False]))
            finally:
                etype=evalue=tb = None
        self.__get_exc_info()

    def __get_proc_info(self):
        """Getting the process information, including process name and id.

        Only used in __collect_diag_info method. No further use. 
        """
        pinfo = multiprocessing.current_process()
        self.__dinfo.update({"Process ID": pinfo.pid, "Process Name": pinfo.name})

    def __get_exc_info(self):
        """Extracting raw traceback from current stack frame.

        """
        self.__dinfo.update({"Exception Type": self.__dexp["etype"].__name__,
                             "Exception Value": str(self.__dexp["evalue"])})
        if self.__dexp["sehandler"]:
            self.__get_exc_info_raise()
        else:
            self.__get_exc_info_log()

    def __get_exc_info_log(self):
        tb = self.__dexp["tb"]
        isde = (self.__dexp["etype"].__name__ == "DiagException")
        f = tb.tb_frame.f_back.f_back if isde else tb.tb_frame
        # print "isde ", isde
        # time.sleep(10)
        fn = 1
        for f, filename, lineno, funcname, lcodes, lind in inspect.getouterframes(f, context=3):
            if 1 == fn:
                # lineno = f.f_lineno if isde else tb.tb_lineno
                if not isde:
                    filename, lineno, funcname, lcodes, lind = inspect.getframeinfo(tb, context=3)
                dtvars = self.__record_vars(f.f_locals, f.f_globals)
                self.__dinfo.update({"Function Name": funcname,
                                     "Function's File": filename,
                                     "Error Code Line": lcodes,
                                     "Call Chain": [self.__fmt_call_chain(funcname, lineno, filename, lcodes[lind])],
                                     "Variable Records": {funcname: dtvars}})
            else:
                self.__dinfo["Call Chain"].append(self.__fmt_call_chain(funcname, lineno, filename, lcodes[lind]))
            fn += 1
        else:
            if fn > 1:
                self.__dinfo["Variable Records"].update({funcname: self.__record_vars(f.f_locals, f.f_globals)})
        if "Call Chain" in self.__dinfo:
            self.__dinfo["Call Chain"].reverse()

    def __get_exc_info_raise(self):
        """Extracting diagnosis information from traceback object when exception raise up and

        there is no except branch for handling it.
        All diagnosis information store in self.__dinfo dictionary.
        """
        fn = 1
        for f, filename, lineno, funcname, lcodes, lind in inspect.getinnerframes(self.__dexp["tb"], context=3):
            if 1 == fn:
                self.__dinfo["Call Chain"] = [self.__fmt_call_chain(funcname, lineno, filename, lcodes[lind])]
            else:
                self.__dinfo["Call Chain"].append(self.__fmt_call_chain(funcname, lineno, filename, lcodes[lind]))
            fn += 1
        else:
            dtvars = self.__record_vars(f.f_locals, f.f_globals)
            self.__dinfo.update({"Function Name": funcname,
                                 "Function's File": filename,
                                 "Error Code Line": lcodes,
                                 "Variable Records": {funcname: dtvars}})
            if fn > 1:
                self.__dinfo["Variable Records"].update({funcname: self.__record_vars(f.f_locals, f.f_globals)})
        # if "Call Chain" in self.__dinfo:
        #     self.__dinfo["Call Chain"].reverse()

    def __fmt_call_chain(self, funcname, lineno, filename, errcode):
        # ch = "Function {0}: line {1}, file {2}\n    {3}".format(funcname, lineno, filename, errcode)
        ch = "Func {0}  ------>  {3}\t******\tin line {1}, file {2}".format(funcname, lineno, filename, errcode.strip())
        return ch

    def __record_vars(self, localvars, globalvars):
        classvars = dict()
        dvars = dict()
        # If exception or log happened in an object of a class, try to record.
        if "self" in localvars and hasattr(localvars["self"], "__dict__"):
            classvars = localvars["self"].__dict__
        # If excdvars and incdvars both are empty [], dumping all classvars, localvars and globalvars;
        # elif incdvars is not empty, dumping the specified variables.
        # elif excdvars is not empty, dumping all variables except those in excdvars list.
        if self.__incdvars:
            dvars = {"user define": {}}
            for iv in self.__incdvars:
                if iv in localvars:
                    dvars["user define"].update({iv: localvars[iv]})
                elif iv in classvars:
                    dvars["user define"].update({iv: classvars[iv]})
                elif iv in globalvars:
                    dvars["user define"].update({iv: globalvars[iv]})
        elif self.__excdvars:
            for iv in self.__excdvars:
                if iv in localvars:
                    del localvars[iv]
                elif iv in classvars:
                    del classvars[iv]
                elif iv in globalvars:
                    del globalvars[iv]          
        if not self.__incdvars:
            dvars = {"locals": localvars, "globals": globalvars, "classes": classvars}
        return dvars    


if __name__ == "__main__":
    di = DiagInfo("D:\\")
    di.log(excdvars=["__doc__", "__builtins__"])
    print "End of the story!"
            

        
        

