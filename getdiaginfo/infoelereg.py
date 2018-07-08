#coding=utf-8
import os


def screen_out_control_file():
    sof = os.path.join(os.path.split(__file__)[0], "ScreenOutElement.txt")
    if not os.path.isfile(sof):
        with open(sof, "w") as sofp:
            sofp.writelines("Begin\nUser Description\nProcess ID\nProcess Name\nFunction Name\nFunction's File\nException Type\nException Value\nError Code Line\nCall Chain\nEnd")
    return sof


def file_out_control_file():
    fof = os.path.join(os.path.split(__file__)[0], "FileOutElement.txt")
    if not os.path.isfile(fof):
        with open(fof, "w") as fofp:
            fofp.writelines("Begin\nUser Description\nProcess ID\nProcess Name\nFunction Name\nFunction's File\nException Type\nException Value\nError Code Line\nCall Chain\nVariable Records\nEnd")
    return fof


if __name__ == "__main__":
    print "Screen file", screen_out_control_file()
    print "File file", file_out_control_file()
    import linecache
