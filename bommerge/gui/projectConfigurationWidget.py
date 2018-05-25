try:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog

import os

class ProjectConfigurationWidget(tk.Toplevel):
    def __init__(self, parent, project):
        tk.Toplevel.__init__(self, parent)
        self.title("Project Configurator")
        self.parent = parent
        self.result = None
        self.project = project
        if self.project == None:
            self.project = []
        self.projectDir = None

        frame = ttk.Frame(self)
        self.openProjectButton = tk.Button(frame, text='Open Project', width=10, command=self.openProject).grid(row=0, column=0)
        self.saveProjectButton = tk.Button(frame, text='Save Project', width=10, command=self.saveProject).grid(row=0, column=1)
        self.addFileButton = tk.Button(frame, text='Add BOM File', width=10, command=self.addFile).grid(row=0, column=2)
        frame.grid(row=0)

        self.filesFrame = ttk.Frame(self)
        self.filesFrame.grid(row=2)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_window(self)


    def showOpenFileDialog(self, filetypes):
        if self.projectDir:
            initialDir = self.projectDir
        else:
            from os.path import expanduser
            initialDir = expanduser("~")   
        filename = filedialog.askopenfilename(initialdir = initialDir,title = "Select file",filetypes = filetypes)
        return filename


    def openProject(self):
        def loadProject(filename):
            import json
            with open(filename) as inputfile:
               project = json.load(inputfile)
            return project   

        filename = self.showOpenFileDialog((("BOM merger project","*.bomproj"),("all files","*.*")))
        if filename:
            self.project = loadProject(filename)
            self.projectDir = os.path.dirname(filename)
            self.result = filename
            self.updateFilelist()
        
        
    def saveProject(self):
        def saveProject(filename, project):
            import json
            with open(filename, 'w') as outputfile:
                outputfile.write(json.dumps(project, indent=4, sort_keys=True, separators=(',', ': ')))  
            
        if self.projectDir:
            initialDir = self.projectDir
        else:
            from os.path import expanduser
            initialDir = expanduser("~")   
        filename = filedialog.asksaveasfilename(initialdir = initialDir,title = "Save file",filetypes = (("BOM merger project","*.bomproj"),("all files","*.*")))
        if filename:
            self.projectDir = os.path.dirname(filename)
            self.result = filename
            saveProject(filename, self.project)
            self.destroy()


    def addFile(self):
        filename = self.showOpenFileDialog((("CSV","*.csv"),("all files","*.*")))         
        if filename:
            self.project.append({"filename" : filename, "Quantity" : 1})
            self.updateFilelist()


    def removeFile(self, filename):
        for file in self.project:
            if filename == file['filename']:
                self.project.remove(file)
                self.updateFilelist()


    def updateQuantity(self, filename, quantity):
        print "new quantity: " + str(quantity) + " for file: " + filename
        for file in self.project:
            if filename == file['filename']:
                file['Quantity'] = int(quantity)


    def updateFilelist(self):
        for i, file in enumerate(self.project):
            widget = self.createFileRow(file)
            widget.grid(row=i+2)


    def createFileRow(self, file):
        import ntpath
        
        frame = ttk.Frame(self.filesFrame)
        entry = tk.Entry(frame, width=60, disabledbackground='white', disabledforeground='black')
        entry.insert(20, ntpath.basename(file["filename"]))
        entry.grid(row=0, column=0)
        entry.config(state=tk.DISABLED)
        
        spinbox = None
        spinbox = tk.Spinbox(frame, width=10, from_=1, to=999999, increment=1, command=lambda : self.updateQuantity(file['filename'], spinbox.get()))
        spinbox.delete(0,"end")
        spinbox.insert(0,file['Quantity'])
        spinbox.grid(row=0, column=1)
        
        removeButton = tk.Button(frame, text='Remove', width=10, command=lambda : self.removeFile(file['filename']))
        removeButton.grid(row=0, column=3)
        return frame
        
        
