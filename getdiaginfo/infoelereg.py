# coding=utf-8

# Deciding which elements can be output to console and their output order
lbriefelereg = ["Begin",
                "User Description",
                "Process ID",
                "Process Name",
                "Function Name",
                "Function's File",
                "Exception Type",
                "Exception Value",
                "Error Code Line",
                "Call Chain",
                "End"]

# Deciding which elements can be output to log file and their output order
ldetailelereg = lbriefelereg[:-1] + ["Variable Records", "End"]

if __name__ == "__main__":
    for ele in lbriefelereg:
        print ele
