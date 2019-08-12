from decimal import *
import re


def string_to_tolerance(tolerance_string):
    if tolerance_string is None:
        return None
    try:
        match = re.match(r"(\D)?(\d+)(\D)", tolerance_string)
        print(match.groups())
        print(match.group(2))
        return Decimal(match.group(2))
    except:
        print(tolerance_string)
        raise


def tolerance_to_string(tolerance):
    return str(tolerance) + "%"
