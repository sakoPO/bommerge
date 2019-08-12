from decimal import *

multiply = {u'G': Decimal('1000000000'),
       u'G\u03a9': Decimal('1000000000'),
       u'GR': Decimal('1000000000'),
       u'M': Decimal('1000000'),
       u'M\u03a9': Decimal('1000000'),
       u'MR': Decimal('1000000'),
       u'k': Decimal('1000'),
       u'k\u03a9': Decimal('1000'),
       u'kR': Decimal('1000'),
       u'R': Decimal('1'),
       u'\u03a9': Decimal('1'),
       u'm': Decimal('0.001'),
       u'm\u03a9': Decimal('0.001'),
       u'mR': Decimal('0.001'),
       u'u': Decimal('0.000001'),
       u'u\u03a9': Decimal('0.000001'),
       u'uR': Decimal('0.000001')}


def convert_resistance_to_ohms(resistance):
    import re

    if resistance == None or resistance == "<VALUE>":
       return None
    if resistance == "DNF" or resistance == "DNP" or resistance == "DNC":
       return "DNF"
    resistance = resistance.replace("Ohms", "\u03a9")
    resistance = resistance.replace("Ohm", "\u03a9")
    try:
        separated = re.split('(\d+)', resistance)
        if separated[-1] in multiply:
            multiplier = multiply[separated[-1]]
            value = Decimal(resistance.replace(separated[-1], ''))
            value = value * multiplier
            return value
        else:
            for i, chunk in enumerate(separated):
                if chunk in multiply:
                    multiplier = multiply[chunk]
                    resistance = Decimal(resistance.replace(chunk, '.'))
                    resistance = resistance * multiplier
                    return resistance
            return Decimal(resistance)
    except:
        print("Unable to convert resistance: " + resistance)
        raise


def ohms_to_string(ohms):
    if ohms == None:
        return None
    if ohms == "DNF":
        return "DNF"
    if ohms == Decimal('0'):
        return u'0\u03a9'
    for key in ['u\u03a9', 'm\u03a9', '\u03a9','k\u03a9', 'M\u03a9', 'G\u03a9']:
        value = ohms / multiply[key]
        if value < Decimal('1000.0') and value >= Decimal('0.0'):
            value = value.quantize(Decimal('.01'))
            return str(value).rstrip('0').rstrip('.') + str(key)

