from gui.mainWindow import MainWindow
from gui.projectConfigurationWidget import ProjectConfigurationWidget
from parsers import csvToJson


def loadJsonFile(filename):
    import json
    with open(filename) as inputfile:
       dictionary = json.load(inputfile)
    return dictionary


def loadProject(filename):   
    project = loadJsonFile(filename)
    return project
    

def saveProject(filename, project):
    import json
    with open(filename, 'w') as outputfile:
        outputfile.write(json.dumps(project, indent=4, sort_keys=True, separators=(',', ': ')))   


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


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proj", help="Project definition file")
    parser.add_argument("-d", "--directory", help="Working directory, this is place where project files will be crated.")
    args = parser.parse_args()
    
    project = None
    if args.proj:
        project = loadProject(args.proj)
        workingDirectory = getDirectory(args.proj)
        
    if args.directory:
        projename = getProjectFilename(args.directory)
        if projname:
            project = loadProject(projname)
            workingDirectory = getDirectory(projname)
            
    if project == None:        
        mainWindow = MainWindow()
        projectConfigGui = ProjectConfigurationWidget(mainWindow, project)
        if projectConfigGui.result:  
            workingDirectory = getDirectory(projectConfigGui.result)
            project = loadProject(projectConfigGui.result)
        
    if project:
        mergeProject(project, workingDirectory)
    
    mainWindow.mainloop()
    

if __name__ == "__main__":
    main()
    
