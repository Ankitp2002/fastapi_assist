def check_or_raise_error(condition, err_msg: str = "Condition not met"):
    """
    Checks a condition and raises a general error if it is not met.
    """
    if not condition:
        raise Exception(err_msg)
