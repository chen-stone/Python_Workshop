# coding=utf-8

import time
import sys


class InputDataErr(Exception):
    pass


def generate_digit_list(scmd):
    """Parse parameter range.测试

    Unfold "1-2" "1,3,5" "1-10-2" to parameter list.
    """
    try:
        ldigit = []
        if scmd.isdigit():
            ldigit.append(int(scmd))
        else:
            if "-" not in scmd:
                ldigit.extend([int(i) for i in scmd.split(",")])
            else:
                for i in scmd.split(","):
                    if i.isdigit():
                        ldigit.append(int(i))
                    else:
                        ldigit.extend(range(*map(lambda j: int(j), i.split("-"))))
    except ValueError as e:
        raise InputDataErr("Wrong parameter is passed to generate_digit_list:\n {1}".format(__name__, e))
    return ldigit


class ProgressBar:
    def __init__(self, taskname=""):
        self.t0 = 0
        if taskname:
            print(taskname + ":")

    def reset_time(self):
        self.t0 = 0

    def __call__(self, pos, total):
        if self.t0 == 0:
            self.t0 = time.time()
        if pos > total:
            raise InputDataErr("Progress is more than 100%, input error!!!")
        progress = round(float(pos) / total, 2)
        barLength = 25  # Modify this to change the length of the progress bar
        block = int(round(barLength * progress))
        text = "\rPercent: [{0}] {1}% ({2}/{3}) {4} seconds".format("#" * block + "-" * (barLength - block),
                                                                    progress * 100,
                                                                    pos, total,
                                                                    round(time.time() - self.t0, 2))
        sys.stdout.write(text)
        sys.stdout.flush()


dwebcharsetmap  = {"gbk": "gb18030",
                   "gb2312": "gb18030",
                   "utf-8": "utf-8"}


def iterelement(data):
    for elem in data:
        yield elem


def iterkvpair(data):
    for k, v in data.items():
        yield str(k)
        yield [v]


def find_type(data):
    return type(data)


def format_output(data, level, linehead, levelsign="\t"):
    print("{0}{1}{2}".format(linehead, levelsign*level, data))


satomoutputdata = {int, float, str, unicode}
mixedata = {list: iterelement,
            tuple: iterelement,
            set: iterelement,
            dict: iterkvpair}


def data_output(data, output_func=format_output, classify_func=find_type, linehead="", level=-1):
    datatype = classify_func(data)
    if datatype in satomoutputdata:
        output_func(data, level, linehead)
    elif datatype in mixedata:
        for subdata in mixedata[datatype](data):
            data_output(subdata, output_func, classify_func, linehead, level+1)
    else:
        print "data type is unhandled: ", datatype
        output_func(data, level, linehead)


def _delimiter_print(spinfo):
    print "*" * 20, spinfo, "*" * 20


def _main_test():
    # generate_digit_list test begin...
    _delimiter_print("generate_digit_list test begin...")
    print generate_digit_list("3,4,5,6")
    print generate_digit_list("3")
    print generate_digit_list("3-10")
    print generate_digit_list("3-10,11,12-16,20")
    print generate_digit_list("3-10-2,11,12-16,20")
    # print generate_digit_list("3-10-2,11,12-16,20k")
    _delimiter_print("generate_digit_list test end.")
    # generate_digit_list test end.

    # Class ProgressBar test begin...
    _delimiter_print("Class ProgressBar test begin...")
    progress = ProgressBar("Testing task")
    for p in range(11):
        progress(p, 10)
        time.sleep(0.1)
    _delimiter_print("Class ProgressBar test end.")
    # Class ProgressBar test end.

    # Function data_output test begin...
    _delimiter_print("Function data_output test begin...")
    datas = [1, 1.0, "first-str",
             set(["s1", "s2", "s3"]),
             ['l1', 'l2', 'l3'],
             {"dk1": {"dk11": "dv11"}, "dk2": ["dv21", "dv22"], ('dk31', 'dk32'): {"dv31", "dv32"}}]
    [data_output(data) for data in datas]
    _delimiter_print("Function data_output test end.")
    # Function data_output test end.


if __name__ == "__main__":
    _main_test()



