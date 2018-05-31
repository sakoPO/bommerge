def convertResistanceToOhms(resistance):
    import re
    mul = {'G': 1000000000,
           'M': 1000000,
           'k': 1000,
           'R': 1,
           'm': 0.001,
           'u': 0.000001}

    if resistance == None:
       return None
    separated = re.split('(\d+)', resistance)
    if separated[-1] in mul:
        multiplier = mul[separated[-1]]
        value = float(resistance[:-len(separated[-1])])
        value = value * multiplier
        return value
