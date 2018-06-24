# based on https://search.murata.co.jp/Ceramy/image/img/A01X/partnumbering_e_02.pdf
import re
from components import capacitor
from decimal import *

dimension = {'03': '0201',
             '15': '0402',
             '18': '0603',
             '21': '0805',
             '31': '1206',
             '32': '1210',
             '43': '1812',
             '55': '2220' }

height_excepat_kc = {'3': '0.3mm',
          '5': '0.5mm',
          '6': '0.6mm',
          '8': '0.8mm',
          '9': '0.85mm',
          'A': '1mm',
          'B': '1.25mm',
          'C': '1.6mm',
          'D': '2mm',
          'E': '2.5mm',
          'M': '1.15mm',
 #         'N': '1.35mm',
          'Q': '1.5mm',
 #         'R': '1.8mm',
          'X': 'Depends on individual standards'}

height_kc_only = {'L': '2.8mm',
                  'Q' : '3.7mm',
                  'T' : '4.8mm',
                  'W' : '6.4mm'}

dielectric_type = {'0C' : 'CHA',
                   '1C' : 'CG',
                   '2C' : 'CH',
                   '3C' : 'CJ',
                   '4C' : 'CK',
                   '5C' : 'C0G',
                   '5G' : 'X8G',
                   '7U' : 'U2J',
                   '9E' : 'ZLM',
                   'C7' : 'X7S',
                   'C8' : 'X6S',
                   'D7' : 'X7T',
                   'L8' : 'X8L',
                   'M8' : 'X8M',
                   'M9' : 'X9M',
                   'R1' : 'R',
                   'R6' : 'X5R',
                   'R7' : 'X7R',
                   'R9' : 'X8R'}

voltage = {'0E' : '2.5VDC',
           '0G' : '4VDC',
           '0J' : '6.3VDC',           
           '1A' : '10VDC',
           '1C' : '16VDC',
           '1E' : '25VDC',
           'YA' : '35VDC',
           '1H' : '50VDC',
           '1J' : '63VDC',
           '1K' : '80VDC',
           '2A' : '100VDC',
           '2E' : '250VDC',
           '2W' : '450VDC',
           '2J' : '630VDC',
           '3A' : '1000VDC',
           'MF' : '250VAC'}

tolerance = {'B' : '+-0.1pF',
             'C': '+-0.25pF',
             'D': '0.5pF',
             'F' : '1%',
             'G' : '2%',
             'J': '5%',
             'K': '10%',
             'M': '20%',
             'R' : 'Depends on individual standards.',
             'W' : '+-0.05pF'}

package = {'L' : 'ø180mm Embossed Taping',
           'D' : 'ø180mm Paper Taping',
           'W' : 'ø180mm Paper Taping',
           'K' : 'ø330mm Embossed Taping',
           'J' : 'ø330mm Paper Taping',
           '#' : 'Unknown package'}


def build_group(dictionary):
    group = '('
    for key in dictionary.keys():
        group = group + str(key) + '|'
    group =  group[:-1] +')'
    return group


def build_regexpr(product_id, series, height_dimmension):
    product_series_group = '(' + product_id + build_group(series) + ')' # 1 and 2
    dimmensions_group = build_group(dimension) # 3
    height_group = build_group(height_dimmension) # 4
    temperature_group = build_group(dielectric_type) #5
    voltage_group = build_group(voltage) # 6
    capacitance_group = '(R\d{2}|\dR\d|\d{3})' # 7
    tolerance_group = build_group(tolerance) # 8
    individual_specificatin_code_group = '(.{3})' # 9
    package_group = build_group(package)
    
    return product_series_group + dimmensions_group + height_group + temperature_group + voltage_group + capacitance_group + tolerance_group + individual_specificatin_code_group + package_group+ '?'


def capacitanceStringToFarads(string):
    value = Decimal(string[:2])    
    mul = Decimal(string[2])
    return value * Decimal('10')**mul * Decimal('10')**Decimal('-12')

def decode_match(match, series_code, height):
    component = {}
    component['Series'] = match.group(1)
    component['Note'] = series_code[match.group(2)]
    component['Case'] = dimension[match.group(3)]
    component['Height'] = height[match.group(4)]
    component['Dielectric Type'] = dielectric_type[match.group(5)]
    component['Voltage'] = voltage[match.group(6)]
    component['Capacitance'] = capacitor.farads_to_string(capacitanceStringToFarads(match.group(7)))
    component['Tolerance'] = tolerance[match.group(8)]
    component['Manufacturer'] = 'Murata'
    return component


def resolve_GC(partname):
    product_id = 'GC'
    series_code = {'3' : 'High Effective Capacitance & High Ripple Current Chip Multilayer Ceramic Capacitors for Automotive',
                   'B' : 'Ni Plating + Pd Plating termination Conductive Glue Mounting Chip Multilayer Ceramic Capacitors for Automotive',
                   'D' : 'MLSC Design Chip Multilayer Ceramic Capacitors for Automotive',
                   'E' : 'Soft Termination MLSC Design Chip Multilayer Ceramic Capacitors for Automotive',
                   'G' : 'AgPd Termination Conductive Glue Mounting Chip Multilayer Ceramic Capacitors for Automotive',
                   'J' : 'Soft Termination Chip Multilayer Ceramic Capacitors for Automotive',
                   'M' : 'Chip Multilayer Ceramic Capacitors for Automotive',
                   'Q' : 'High Q Chip Multilayer Ceramic Capacitors for Automotive'}

    regexpr = build_regexpr(product_id, series_code, height_excepat_kc)
    match = re.match(regexpr, partname)
    if match:
        return decode_match(match, series_code, height_excepat_kc)


def resolve_GG(partname):
    product_id = 'GG'
    series_code = {'D' : 'Water Repellent MLSC Design Chip Multilayer Ceramic Capacitors for Automotive',
                   'M' : 'Water Repellent Chip Multilayer Ceramic Capacitors for Automotive'}

    regexpr = build_regexpr(product_id, series_code, height_excepat_kc)
    match = re.match(regexpr, partname)
    if match:
        return decode_match(match, series_code, height_excepat_kc)


def resolve_GR(partname):
    product_id = 'GR'
    series_code = {'T' : 'AEC-Q200 Compliant Chip Multilayer Ceramic Capacitors for Infotainment'}

    regexpr = build_regexpr(product_id, series_code, height_excepat_kc)
    match = re.match(regexpr, partname)
    if match:
        return decode_match(match, series_code, height_excepat_kc)


def resolve_GX(partname):
    product_id = 'GX'
    series_code = {'T' : 'AEC-Q200 Compliant Water Repellent Chip Multilayer Ceramic Capacitors for Infotainment'}

    regexpr = build_regexpr(product_id, series_code, height_excepat_kc)
    match = re.match(regexpr, partname)
    if match:
        return decode_match(match, series_code, height_excepat_kc)


def resolve_KC(partname):
    product_id = 'KC'
    series_code = {'3' : 'High Effective Capacitance & High Allowable Ripple Current Metal Terminal Type Multilayer Ceramic Capacitors for Automotive',
                   'A' : 'Safety Standard Certified Metal Terminal Type Multilayer Ceramic Capacitors for Automotive',
                   'M' : 'Metal Terminal Type Multilayer Ceramic Capacitors for Automotive'}

    regexpr = build_regexpr(product_id, series_code, height_kc_only)
    match = re.match(regexpr, partname)
    if match:
        return decode_match(match, series_code, height_kc_only)


def resolve(partname):
    part = resolve_GC(partname)
    if part:
        print ('Capacitor mached: ' + partname)
        return part
    part = resolve_GG(partname)
    if part:
        print ('Capacitor mached: ' + partname)
        return part
    part = resolve_GR(partname)
    if part:
        print ('Capacitor mached: ' + partname)
        return part
    part = resolve_GX(partname)
    if part:
        print ('Capacitor mached: ' + partname)
        return part
    part = resolve_KC(partname)
    if part:
        print ('Capacitor mached: ' + partname)
        return part

