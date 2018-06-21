def loadJsonFile(filename):
    import json
    with open(filename) as inputfile:
       dictionary = json.load(inputfile)
    return dictionary


def save_json_file(filename, content):
    import json
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(content, indent=4, sort_keys=True, separators=(',', ': ')))
