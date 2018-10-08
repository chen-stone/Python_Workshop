# coding=utf-8

_lbriefconelemreg = ["Variable Records"]


# Deciding which elements can be output to console and their output order
_logconelemreg = ["Begin",
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
_logfilelemreg = _logconelemreg[:-1] + ["Variable Records", "End"]


def diag_elements_register():
    """Defining output information elements and their orders.

    Only used in DiagInfo's __init__ method.
    """
    return _lbriefconelemreg, _logconelemreg, _logfilelemreg


if __name__ == "__main__":
    for ele in _logconelemreg:
        print ele
