from decimal import *

multiply = {'G': Decimal('1000000000'),
            'GV': Decimal('1000000000'),
            'M': Decimal('1000000'),
            'MV': Decimal('1000000'),
            'k': Decimal('1000'),
            'kV': Decimal('1000'),
            'V': Decimal('1'),
            'm': Decimal('0.001'),
            'mV': Decimal('0.001'),
            'u': Decimal('0.000001'),
            'uV': Decimal('0.000001'),
            'n': Decimal('0.000000001'),
            'nV': Decimal('0.000000001'),
            'p': Decimal('0.000000000001'),
            'pV': Decimal('0.000000000001'),
            'f': Decimal('0.000000000000001'),
            'fV': Decimal('0.000000000000001')}


def volts_to_string(voltage):
    if voltage is None:
        return None
    for key in ['fV', 'pV', 'nV', 'uV', 'mV', 'V', 'kV', 'MV', 'GV']:
        value = voltage / multiply[key]
        if Decimal('1000.0') > value >= Decimal('0.0'):
            value = value.quantize(Decimal('.01'))
            return str(value).rstrip('0').rstrip('.') + str(key)
