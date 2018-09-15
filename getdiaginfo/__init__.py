#coding=utf-8
import sys
import diaginfo


__all__ = ["enable"]


def enable(logdir="D:\\", hooksysexp=True, out2scn=True, excdvars=None, incdvars=None):
    """Creating a object of diaginfo class and deciding to use it to instead of system's exception handler or not.

    return this object.
    all its parameters are :
        logdir: string, Specifing a directory to store detail log file.
        hooksysexp: bool, deciding to hook system's exception handler or not.
        out2scn: boot, silence in console or not.
        excdvars: list, default is empty. Specifing which variables don't need to be log
        incdvars: list, default is empty. Specifing only those variables which need to be log
    """
    lexcdvars = ["__doc__", "__builtins__"]
    lincdvars = list()
    if excdvars:
        lexcdvars.extend(excdvars)
    if incdvars:
        lincdvars.extend(incdvars)
    diobj = diaginfo.DiagInfo(logdir=logdir, out2scn=out2scn, excdvars=lexcdvars, incdvars=lincdvars)
    if hooksysexp:
        sys.excepthook = diobj
    return diobj


if __name__ == "__main__":
    pass