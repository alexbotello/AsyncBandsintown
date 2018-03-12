class TooManyRequests(Exception):
    """
    Raise when API rate limit is reached
    """
    pass

class MissingArgument(Exception):
    """
    Raise when an argument was not given
    """
    pass
