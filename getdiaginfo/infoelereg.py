# coding=utf-8


# Deciding which elements can be output to console and their output order
_lbriefelereg = ["Begin",
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
_ldetailelereg = _lbriefelereg[:-1] + ["Variable Records", "End"]


def diag_elements_register():
    """Defining output information elements and their orders.

    Only used in DiagInfo's __init__ method.
    """
    return _lbriefelereg, _ldetailelereg


if __name__ == "__main__":
    for ele in _lbriefelereg:
        print ele
