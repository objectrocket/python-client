
def comparable_dictionaries(d1, d2):
    """
    :param d1: dictionary
    :param d2: dictionary
    :return: True if d1 and d2 have the same keys and False otherwise

    util function to compare two dictionaries for matching keys (including
    nested keys), ignoring values
    """
    for key in d1:
        if key not in d2:
            return False
        else:
            if type(d1[key]) == dict:
                if type(d2[key]) == dict:
                    return comparable_dictionaries(d1[key], d2[key])
                else:
                    return False
            return True
