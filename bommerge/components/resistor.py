def convertResistanceToOhms(resistance):
    import re
    mul = {u'G': 1000000000,
           u'G\u03a9': 1000000000,
           u'M': 1000000,
           u'M\u03a9': 1000000,
           u'k': 1000,
           u'k\u03a9': 1000,
           u'R': 1,
           u'\u03a9': 1,
           u'm': 0.001,
           u'm\u03a9': 0.001,
           u'u': 0.000001,
           u'u\u03a9': 0.000001}

    if resistance == None:
       return None
    separated = re.split('(\d+)', resistance)
#    print resistance +', ' + str(len(separated))  + ', ' + str(separated)
    if separated[-1] in mul:
        multiplier = mul[separated[-1]]
        value = float(resistance[:-len(separated[-1])])
        value = value * multiplier
        return value
    else:
        return float(resistance)

