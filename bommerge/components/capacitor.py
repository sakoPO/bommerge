from decimal import *
import re
    
multiply = {'G': Decimal('1000000000'),
       'GF': Decimal('1000000000'),
       'M': Decimal('1000000'),
       'MF': Decimal('1000000'),
       'k': Decimal('1000'),
       'kF': Decimal('1000'),
       'F': Decimal('1'),
       'm': Decimal('0.001'),
       'mF': Decimal('0.001'),
       'u': Decimal('0.000001'),
       'uF': Decimal('0.000001'),
       'n': Decimal('0.000000001'),
       'nF': Decimal('0.000000001'),
       'p': Decimal('0.000000000001'),
       'pF': Decimal('0.000000000001'),
       'f': Decimal('0.000000000000001'),
       'fF': Decimal('0.000000000000001')}


def convert_capacitance_co_farads(capacitance):
    try:
        if capacitance is None:
            return None
        if capacitance == 'DNF':
            return 'DNF'
        separatedCapacitance = re.split('(\d+)', capacitance)
        if separatedCapacitance[-1] in multiply:
            multiplier = multiply[separatedCapacitance[-1]]
            value = Decimal(capacitance.replace(separatedCapacitance[-1], ''))
            value = value * multiplier
            return value
        else:
            for i, chunk in enumerate(separatedCapacitance):
                if chunk in multiply:
                    multiplier = multiply[chunk]
                    capacitance = Decimal(capacitance.replace(chunk, '.'))
                    capacitance = capacitance * multiplier
                    return capacitance
            return Decimal(capacitance)
    except:
        print(capacitance)
        raise


def farads_to_string(farads):
    if farads is None:
        return None
    if farads == "DNF":
        return "DNF"
    for key in ['fF', 'pF', 'nF', 'uF', 'mF', 'F','kF', 'MF', 'GF']:
        value = farads / multiply[key]
        if value < Decimal('1000.0') and value >= Decimal('0.0'):
            value = value.quantize(Decimal('.01'))
            return str(value).rstrip('0').rstrip('.') + str(key)

