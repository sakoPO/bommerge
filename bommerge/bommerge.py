#!/usr/bin/env python

try:
    from components import resistor
    from components import capacitor
    from components import voltage
    from components import tolerance
except:
    from bommerge.components import resistor
    from bommerge.components import capacitor
    from bommerge.components import voltage
    from bommerge.components import tolerance

from gui.projectConfigurationWidget import ProjectConfigurationWidget
from parsers import csvToJson
from utils import files
import os
from decimal import *

try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


def loadProject(filename):
    project = files.load_json_file(filename)
    project_directory = files.get_directory_from_path(filename)
    print("Loading project: " + project_directory)
    for file in project:
        if not os.path.isabs(file['filename']):
            file['filename'] = os.path.normpath(os.path.join(project_directory, file['filename']))
    print(project)
    return project


def saveProject(filename, project):
    project_directory = files.get_directory_from_path(filename)
    for file in project:
        normalized_path = os.path.normpath(file['filename'])
        print(normalized_path)
        file['filename'] = os.path.relpath(normalized_path, project_directory)
    files.save_json_file(filename, project)


def read_configuration():
    user_dir = files.get_user_home_directory()
    configuration_file = user_dir + '/.bommerge/configuration.json'
    if files.file_exist(configuration_file):
        configuration = files.load_json_file(configuration_file)
        token = str(configuration['Distributors']['TME']['token'])
        app_secret = str(configuration['Distributors']['TME']['app_secret'])
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
    from distributor_connector import partkeepr
    distributors = [tme.TME(tme_config['token'], tme_config['app_secret']),
                    partkeepr.Partkeepr("https://partkeepr.locallan", "auto", "auto")]

    for shop in distributors:
        for component in components_group:
            if 'Manufacturer Part Number' in component and component['Manufacturer Part Number'] != "":
                print("Request for " + component['Manufacturer Part Number'])
                found = shop.find_component(component['Manufacturer Part Number'])
            else:
                if group == "Capacitors":
                    print("Request for " + to_string(component['Capacitance']) + " " + to_string(
                        component['Voltage']) + ' ' + to_string(component['Case']))
                    try:
                        capacitor_parameters = {'Capacitance': capacitor.convert_capacitance_co_farads(component['Capacitance']),
                                                'Case': to_string(component['Case']),
                                                'Voltage': voltage.string_to_voltage(component['Voltage']),
                                                'Dielectric Type': component['Dielectric Type']}
                        found = shop.find_capacitor_by_parameters(capacitor_parameters)
                        if found:
                            for part in found:
                                if 'Voltage' in part['Parameters']:
                                    part['Parameters']['Voltage'] = voltage.volts_to_string(part['Parameters']['Voltage'])
                                if 'Capacitance' in part['Parameters']:
                                    part['Parameters']['Capacitance'] = capacitor.farads_to_string(part['Parameters']['Capacitance'])
                    except InvalidOperation:
                        print(component)
                        raise
                elif group == "Resistors":
                    print("Request for " + to_string(component['Resistance']) + ' ' + to_string(
                        component['Case']) + ' ' + to_string(component['Tolerance']))
                    if component['Resistance'] is None:
                        print("Skipping...")
                        component["Distributors"] = []
                        continue
                    try:
                        resistor_parameters = {'Resistance': resistor.convert_resistance_to_ohms(component['Resistance']),
                                               'Case': component['Case'],
                                               'Tolerance': tolerance.string_to_tolerance(component['Tolerance'])}
                        found = shop.find_resistor_by_parameters(resistor_parameters)
                        if found:
                            for part in found:
                                if 'Resistance' in part['Parameters']:
                                    part['Parameters']['Resistance'] = resistor.ohms_to_string(part['Parameters']['Resistance'])
                                if 'Tolerance' in part['Parameters']:
                                    part['Parameters']['Tolerance'] = tolerance.tolerance_to_string(part['Parameters']['Tolerance'])
                    except TypeError:
                        print(component)
                        raise
                elif group in ["IntegratedCircuits"] and component['Comment'] != '':
                    print("Request for " + to_string(component['Comment']))
                    found = shop.find_component(component['Comment'])
                else:
                    found = None

            if "Distributors" not in component:
                component["Distributors"] = []
            if found:
                component["Distributors"].append({"Name": shop.name, "Components": found})


def find_component_comment(components_group, tme_config):
    from distributor_connector import tme

    shop = tme.tme()

    for component in components_group:
        if 'Comment' in component and component['Comment'] != "":
            print("Request for " + component['Comment'])
            found = shop.find_component(component['Comment'])
            if found:
                print(found)

            # for component in found['Data']['ProductList']:
            #    print(component['Symbol'] + " : " + component['OriginalSymbol'] + " : " + component['Producer'])
            # if 'stockAndPrice' in found:
            #    print(found['stockAndPrice'])


def ged_distributor_stock(merged, tme_config):
    for group in merged.keys():
        find_component(merged[group], group, tme_config)
    # find_component(merged["Resistors"])
    # find_component_comment(merged["IntegratedCircuits"])


def parse_files_if_needed(project_file_list, destynation):
    print("Parsing csv files and saving results to: " + destynation)
    for f in project_file_list:
        file_path = f['filename']
        if files.get_file_extension(file_path) == '.json':
            files.copy(file_path, destynation + '/' + files.get_filename_from_path(file_path))
        else:
            csvToJson.convert(file_path, destynation)


def remove_DNF_and_empty_components(components):
    to_remove = []
    for capacitor in components['Capacitors']:
        if capacitor['Capacitance'] == 'DNF' or capacitor['Capacitance'] == '':
            to_remove.append(capacitor)
    for r in to_remove:
        components['Capacitors'].remove(r)
    # Remove empty resistors
    to_remove = []
    for capacitor in components['Resistors']:
        if capacitor['Resistance'] == 'DNF' or capacitor['Resistance'] == '':
            to_remove.append(capacitor)
    for r in to_remove:
        components['Resistors'].remove(r)
    return components


def mergeProject(project, workingDirectory, nogui):
    import os
    import automaticMerger
    import guiBOM as manual_merger

    directory = workingDirectory + "/tmp"

    files.make_directory_if_not_exist(directory)
    parse_files_if_needed(project, directory)

    for bom in project:
        bom['filename'] = os.path.join(directory,
                                       files.replace_file_extension(files.get_filename_from_path(bom['filename']),
                                                                    '.json'))

    components = automaticMerger.merge(project)
    if nogui is None:
        root = tk.Tk()
        root.title("BOM Merger")
        merger = manual_merger.ManualMerger(root, components)
        root.mainloop()
        if merger.result:
            components = merger.components
        else:
            components = None

    if components:
        files.save_json_file(os.path.join(directory, 'automerged.json'), components)
        from exporters import csvExporter
        csvExporter.save(dict(components), os.path.join(workingDirectory, "mergedBOM.csv"))

        components = remove_DNF_and_empty_components(components)

        tme_config = read_configuration()
        print(tme_config)
        ged_distributor_stock(components, tme_config)
        filename = directory + '/merged.json'
        files.save_json_file(filename, components)

        from gui import orderingDialog
        root = tk.Tk()
        orderingWidget = orderingDialog.OrderWidget(root, filename)
        root.mainloop()
        filename = directory + '/order.json'
        files.save_json_file(filename, orderingWidget.components)
        if orderingWidget.result:
            for supplier in orderingWidget.result.keys():
                csvExporter.save_list(orderingWidget.result[supplier],
                                      workingDirectory + '/' + supplier + '_human_readable.csv')
                order_list = []
                for component in orderingWidget.result[supplier]:
                    order_list.append({'Part number': component['Shop Part Number'], 'Quantity': component['Quantity']})
                csvExporter.save_list(order_list, workingDirectory + '/' + supplier + '.csv', write_header=False)


class ProjectConfigWidget(ProjectConfigurationWidget):
    def load_project(self, filename):
        return loadProject(filename)

    def save_project_file(self, filename):
        project = self.files_widget.create_file_list()
        return saveProject(filename, project)


def first_run():
    user_dir = files.get_user_home_directory()
    configuration_file = user_dir + '/.bommerge/configuration.json'
    return files.file_exist(configuration_file) is False


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proj", help="Project definition file")
    parser.add_argument("--nogui", help="Run bommerge without gui, only automatical merge will be performed.")
    args = parser.parse_args()

    if first_run():
        pass

    project = None
    if args.proj:
        project = loadProject(args.proj)
        working_directory = files.get_directory_from_path(args.proj)

    if project is None:
        projectConfigGui = ProjectConfigWidget()
        if projectConfigGui.result:
            working_directory = files.get_directory_from_path(projectConfigGui.result)
            project = loadProject(projectConfigGui.result)

    if project:
        mergeProject(project, working_directory, args.nogui)


if __name__ == "__main__":
    main()
