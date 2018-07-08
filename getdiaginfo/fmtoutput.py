#coding=utf-8
def fmt_area(lflag, label, value):
    multiprint(value, lflag)


def fmt_str_same_line(lflag, label, value):
    multiprint("{0: <20}{1}".format(label+":", value), lflag)


def fmt_str_dif_line(lflag, label, value):
    multiprint(label+":", lflag)
    [multiprint("  "+line.rstrip(), lflag) for line in value]
        

def fmt_dict_dif_line(lflag, label, value):
    multiprint(label+":", lflag)
    _output(value, lflag)


def _output(value, lflag, tabkeynum=1):
    for key in value:        
        if isinstance(value[key], dict):
            multiprint("{0}{1}:\n".format("\t"*tabkeynum, key), lflag)
            _output(value[key], lflag, tabkeynum+1)
        elif isinstance(value[key], set):
            pass    # ToDo: Should be finished for set in the future
        #elif isinstance(value[key], str):
        #    [multiprint("{0}{1}\n".format("\t"*tabkeynum, line), lflag) for line in value[key].split()]
        else:
            multiprint("{0}{1}: {2}\n".format("\t"*tabkeynum, key, value[key]), lflag)

            
def multiprint(s, lflag):
    if lflag[0]:
        print s
    if lflag[1]:        
        lflag[1].writelines(s.rstrip()+"\n")

dftfuncmap = {"Begin": fmt_area,
              "End": fmt_area,
              "User Description": fmt_str_same_line,
              "Process ID": fmt_str_same_line,
              "Process Name": fmt_str_same_line,
              "Exception Type": fmt_str_same_line,
              "Exception Value": fmt_str_same_line,
              "Function Name": fmt_str_same_line,
              "Function's File": fmt_str_same_line,
              "Error Code Line": fmt_str_dif_line,
              "Call Chain": fmt_str_dif_line,
              "Variable Records": fmt_dict_dif_line }


if __name__ == "__main__":
    pass