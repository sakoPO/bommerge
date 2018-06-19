#!/usr/bin/env python2

from gui.projectConfigurationWidget import ProjectConfigurationWidget
from parsers import csvToJson
import os

try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    

def loadJsonFile(filename):
    import json
    with open(filename) as inputfile:
       dictionary = json.load(inputfile)
    return dictionary


def loadProject(filename):
    project = loadJsonFile(filename)
    project_directory = getDirectory(filename)
    print("Loading project: " + project_directory)
    for file in project:
        if not os.path.isabs(file['filename']):
            file['filename'] = os.path.normpath(os.path.join(project_directory, file['filename']))
    print(project)
    return project


def saveProject(filename, project):
    def save_json_file(filename, dictionary):
        import json
        with open(filename, 'w') as outputfile:
            outputfile.write(json.dumps(project, indent=4, sort_keys=True, separators=(',', ': ')))

    project_directory = getDirectory(filename)
    for file in project:
        normalized_path = os.path.normpath(file['filename'])
        print(normalized_path)
        file['filename'] = os.path.relpath(normalized_path, project_directory)
    save_json_file(filename, project)


def parseCSVfiles(files, destynation):
    print("Parsing csv files and saving results to: " + destynation)
    for f in files:
        csvToJson.convert(f['filename'], destynation)


def getDirectory(path):
    import os
    absoluteProjectFilenamePath = os.path.abspath(path)
    return os.path.dirname(absoluteProjectFilenamePath)


def replaceFileExtension(filename, newExtension):
    import os
    return os.path.splitext(filename)[0] + newExtension


def getFilenameFromPath(path):
    import ntpath
    return ntpath.basename(path)


def get_user_home_directory():
    from os.path import expanduser
    return expanduser("~")

def file_exist(file_path):
    import os
    
    if os.path.exists(getDirectory(file_path)) and os.path.isfile(file_path):
        return True
    return False

def read_configuration():
    user_dir = get_user_home_directory()
    configuration_file = user_dir + '/.bommerge/configuration.json'
    if file_exist(configuration_file):
        configuration = loadJsonFile(configuration_file)
        token = str(configuration['Distributors']['TME']['token'])
        app_secret =  str(configuration['Distributors']['TME']['app_secret'])
        tme_config = {'token': token, 'app_secret': app_secret}
        return tme_config
    else:
        print("Unable to read bommerge configuration file. " + str(configuration_file))


def find_component(components_group, group, tme_config):
    def to_string(case):
        if case:
            return case
        return 'None'
        
    from distributor_connector import tme
#    config = loadJsonFile('config.json')     
 #   token = str(config['Distributors']['TME']['token'])
 #   app_secret =  str(config['Distributors']['TME']['app_secret'])
 #   print app_secret[0]
    shop = tme.TME(tme_config['token'], tme_config['app_secret'])
    
    for component in components_group:        
        if 'Manufacturer Part Number' in component and component['Manufacturer Part Number'] != "":
            print("Request for " + component['Manufacturer Part Number'])
            found = shop.find_component(component['Manufacturer Part Number'])            
        else:        
            if group == "Capacitors":
                print("Request for " + to_string(component['Capacitance']) + " " + to_string(component['Voltage']) + ' ' + to_string(component['Case']))
                found = shop.find_capacitor_by_parameters(component)
            elif group == "Resistors":
                print("Request for " + to_string(component['Resistance']) + ' ' + to_string(component['Case']) + ' ' + to_string(component['Tolerance']))
                found = shop.find_resistor_by_parameters(component)
            elif group in ["IntegratedCircuits"] and component['Comment'] != '':
                print("Request for " + to_string(component['Comment']))
                found = shop.find_component(component['Comment'])
            else:
                found = None
            #for component in found['Data']['ProductList']:
            #    print(component['Symbol'] + " : " + component['OriginalSymbol'] + " : " + component['Producer'])
            #if 'stockAndPrice' in found:
            #    print(found['stockAndPrice'])

        if "Distributors" not in component:
            component["Distributors"] = []
        if found:
            #print found            
            component["Distributors"].append({"Name": "TME", "Components": found})

def find_component_comment(components_group, tme_config):
    from distributor_connector import tme
    
    shop = tme.tme()
    
    for component in components_group:        
        if 'Comment' in component and component['Comment'] != "":
            print("Request for " + component['Comment'])
            found = shop.find_component(component['Comment'])
            if found:
                print(found)
               
            #for component in found['Data']['ProductList']:
            #    print(component['Symbol'] + " : " + component['OriginalSymbol'] + " : " + component['Producer'])
            #if 'stockAndPrice' in found:
            #    print(found['stockAndPrice'])
            

def ged_distributor_stock(merged, tme_config):
    for group in merged.keys():
        find_component(merged[group], group, tme_config)
    #find_component(merged["Resistors"])
    #find_component_comment(merged["IntegratedCircuits"])
    
        
def saveFile(filename, content):
    import json
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(content, indent=4, sort_keys=True, separators=(',', ': ')))


def mergeProject(project, workingDirectory, nogui):
    import os
    import automaticMerger
    import guiBOM as manual_merger
    directory = workingDirectory + "/tmp"
    if not os.path.exists(directory):
        os.makedirs(directory)
    parseCSVfiles(project, directory)
    for bom in project:
        bom['filename'] = os.path.join(directory, replaceFileExtension(getFilenameFromPath(bom['filename']), '.json'))

    automergeOutputFile = os.path.join(directory, 'automerged.json')
    automaticMerger.merge(project, automergeOutputFile)
    if nogui == None:
        manual_merger.merge(automergeOutputFile)

    components = loadJsonFile(automergeOutputFile)
    tme_config = read_configuration()
    print(tme_config)
    ged_distributor_stock(components, tme_config)
    filename = directory + '/order.json'
    saveFile(filename, components)
    
    from gui import orderingDialog
    root = tk.Tk()
    orderingDialog.OrderWidget(root, filename)
    root.mainloop()

    from exporters import csvExporter
    csvExporter.save(dict(loadJsonFile(automergeOutputFile)), os.path.join(workingDirectory, "mergedBOM.csv"))


class ProjectConfigWidget(ProjectConfigurationWidget):
    def load_project(self, filename):
        return loadProject(filename)

    def save_project_file(self, filename):
        project = self.files_widget.create_file_list()
        return saveProject(filename, project)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proj", help="Project definition file")
    parser.add_argument("--nogui", help="Run bommerge without gui, only automatical merge will be performed.")
    args = parser.parse_args()

    project = None
    if args.proj:
        project = loadProject(args.proj)
        workingDirectory = getDirectory(args.proj)

    if project == None:
        projectConfigGui = ProjectConfigWidget()
        if projectConfigGui.result:
            workingDirectory = getDirectory(projectConfigGui.result)
            project = loadProject(projectConfigGui.result)

    if project:
        mergeProject(project, workingDirectory, args.nogui)


if __name__ == "__main__":
    main()

