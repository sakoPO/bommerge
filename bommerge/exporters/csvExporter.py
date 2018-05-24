import csv

def unify_dictionary_keys(bom):
    unified_keys = set()
    for key in bom.keys():
        for component in bom[key]:
            for key in component.keys():
                unified_keys.add(key)
    
    unified_bom = []
    for key in bom.keys():
        for component in bom[key]:
            unified_component = {}
            for key in unified_keys:
                if key in component:
                    unified_component[key] = component[key]
                else:
                    unified_component[key] = ''
            unified_bom.append(unified_component)
    return unified_bom


def sort_keys(keys):
    def sorting_function(x):
        positions = {'Quantity': 1, 'Manufacturer Part Number': 2, 'Manufacturer': 3, 'Comment': 4, 'Resistance': 5, 'Capacitance': 6, 'Voltage': 7, 'Case': 8, 'Tolerance': 9, 'Dielectric Type' : 10}
        if x in positions:
            return positions[x]
        return 11    
    
    return sorted(keys, key=sorting_function)

def save(bom, filename):
    unified_bom = unify_dictionary_keys(bom)
    with open(filename, "w") as outfile:
        dict_writer = csv.DictWriter(outfile, sort_keys(unified_bom[0].keys()))
        dict_writer.writeheader()
        dict_writer.writerows(unified_bom)
