import csv

def unify_dictionary_keys(bom):
    unified_keys = set()
    unified_keys.add('Value')
    for key in bom.keys():
        for component in bom[key]:
            for key in component.keys():
                unified_keys.add(key)
    
    unified_bom = []
    for key in bom.keys():
        for component in bom[key]:
            unified_component = {}
            for key in unified_keys:
                dest_key = 'Value' if key in ['Capacitance', 'Inductance', 'Resistance'] else key                
                if key in component:
                    unified_component[dest_key] = component[key]
                elif dest_key not in unified_component.keys():
                    unified_component[dest_key] = ''
#                    print(str(key) + " key not found in component: " + str(component))
            unified_bom.append(dict(unified_component))
    return unified_bom


def sort_keys(keys):
    def sorting_function(x):
        positions = {'Quantity': 0, 'Manufacturer Part Number': 2, 'Manufacturer': 3, 'Comment': 4, 'Resistance': 5, 'Capacitance': 6, 'Value': 7, 'Voltage': 8, 'Case': 9, 'Tolerance': 10, 'Dielectric Type' : 11}
        if x in positions:
            return positions[x]
        return 12    
    
    return sorted(keys, key=sorting_function)

def save(bom, filename):
    unified_bom = unify_dictionary_keys(bom)
    with open(filename, "w") as outfile:
        dict_writer = csv.DictWriter(outfile, sort_keys(unified_bom[0].keys()))
        dict_writer.writeheader()
        dict_writer.writerows(unified_bom)

def save_list(bom, filename, write_header = True):
    with open(filename, "w") as outfile:
        dict_writer = csv.DictWriter(outfile, sort_keys(bom[0].keys()))
        if write_header == True:
            dict_writer.writeheader()
        dict_writer.writerows(bom)
