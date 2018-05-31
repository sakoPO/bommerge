#!/usr/bin/env python2

from gui.projectConfigurationWidget import ProjectConfigurationWidget
from parsers import csvToJson
import os


def loadJsonFile(filename):
    import json
    with open(filename) as inputfile:
       dictionary = json.load(inputfile)
    return dictionary


def loadProject(filename):
    project = loadJsonFile(filename)
    project_directory = getDirectory(filename)
    print "Loading project: " + project_directory
    for file in project:
        if not os.path.isabs(file['filename']):
            file['filename'] = os.path.normpath(os.path.join(project_directory, file['filename']))
    print project
    return project


def saveProject(filename, project):
    def save_json_file(filename, dictionary):
        import json
        with open(filename, 'w') as outputfile:
            outputfile.write(json.dumps(project, indent=4, sort_keys=True, separators=(',', ': ')))

    project_directory = getDirectory(filename)
    for file in project:
        normalized_path = os.path.normpath(file['filename'])
        print normalized_path
        file['filename'] = os.path.relpath(normalized_path, project_directory)
    save_json_file(filename, project)


def parseCSVfiles(files, destynation):
    print "Parsing csv files and saving results to: " + destynation
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


def mergeProject(project, workingDirectory):
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
    manual_merger.merge(automergeOutputFile)

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
        mergeProject(project, workingDirectory)


if __name__ == "__main__":
    main()

