try:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox

import os


class file_quantity_widget(ttk.Frame):    
    def __init__(self, parent, remove_callback):
        ttk.Frame.__init__(self, parent)

        self.entry = tk.Entry(self, width=60, disabledbackground='white', disabledforeground='black')
        self.entry.grid(row=0, column=0)

        self.spinbox = tk.Spinbox(self, width=10, from_=1, to=999999, increment=1)
        self.spinbox.delete(0, "end")
        self.spinbox.grid(row=0, column=1)
        self.spinbox.config(state=tk.DISABLED)

        self.removeButton = tk.Button(self, text='Remove', width=10, command=lambda : remove_callback(self.filename))
        self.removeButton.grid(row=0, column=3)
        self.removeButton.config(state=tk.DISABLED)

        self.filename = ''


    def get_quantity(self):
        return int(self.spinbox.get())


    def set_quantity(self, quantity):
        if self.filename == '':
            raise RuntimeError("Adding quantity to uninitialized widget")
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, quantity)


    def get_filename(self):
        return self.filename


    def is_empty(self):
        return self.filename == ''


    def clear(self):
        self.entry.delete(0, "end")
        self.spinbox.delete(0, "end")
        self.filename = ''
        self.removeButton.config(state=tk.DISABLED)
        self.spinbox.config(state=tk.DISABLED)


    def update(self, filename, quantity):
        import ntpath
        if filename != '':
            self.removeButton.config(state=tk.NORMAL)
            self.entry.delete(0, "end")
            basename = ntpath.basename(filename)
            self.entry.insert(len(basename), basename)
            self.spinbox.config(state=tk.NORMAL)
            self.spinbox.delete(0, "end")
            self.spinbox.insert(0, quantity)
            self.filename = filename


class bom_files_table(ttk.Frame):
    def __init__(self, parent, on_empty):
        ttk.Frame.__init__(self, parent)
        self.bom_files = []
        self.on_empty = on_empty
        self.create_empty_rows()
        
    def create_empty_rows(self):
        for i in range(6):
            row_widget = file_quantity_widget(self, self.remove_file)
            row_widget.grid(row=i)
            self.bom_files.append(row_widget)
        
    def add_file(self, filename, quantity = 1):
        if self.is_on_list(filename):
            messagebox.showinfo("Notice", "File already in project, quantity will be increased.")
            widget = self.bom_files[self.get_index_of(filename)]
            widget.set_quantity(widget.get_quantity() + quantity)
        else:
            print("Adding new file: " + filename)
            for widget in self.bom_files:
                if widget.is_empty():
                    widget.update(filename, 1)
                    return
            row_widget = file_quantity_widget(self, self.remove_file)
            row_widget.update(filename, quantity)
            row_widget.grid(row=len(self.bom_files))
            self.bom_files.append(row_widget)
    
    def get_index_of(self, filename):
        for i, row in enumerate(self.bom_files):
            if row.get_filename() == filename:
                return i

    def remove_file(self, filename):
        file_index = self.get_index_of(filename)        
        for i in range(file_index, len(self.bom_files) - 1):
            if self.bom_files[i+1].is_empty():
                self.bom_files[i].clear()
            else:    
                filename_tmp = self.bom_files[i+1].get_filename()
                quantity_tmp = self.bom_files[i+1].get_quantity()
                self.bom_files[i].update(filename_tmp, quantity_tmp)
                
        if len(self.bom_files) > 6:
            self.bom_files[-1].destroy()
            del self.bom_files[-1]
        else:
            self.bom_files[-1].clear()

        if self.is_empty() and self.on_empty:
           self.on_empty()
        
    def is_on_list(self, filename):
        for widget in self.bom_files:
            if widget.get_filename() == filename:
                return True


    def is_empty(self):
        return self.bom_files[0].is_empty()
        
    def create_file_list(self):
        project = []
        for widget in self.bom_files:
            if not widget.is_empty():
                project.append({'filename': widget.get_filename(), 'Quantity': widget.get_quantity()})
        return project

class ProjectConfigurationWidget(tk.Tk):
    def __init__(self, project_filename = None):
        tk.Tk.__init__(self)
        self.title("Project Configurator")

        button_frame = ttk.Frame(self)
        self.openProjectButton = tk.Button(button_frame, text='Open Project', width=10, command=self.open_project)
        self.openProjectButton.grid(row=0, column=0)
        self.saveProjectButton = tk.Button(button_frame, text='Save Project', width=10, state=tk.DISABLED, command=self.save_project)
        self.saveProjectButton.grid(row=0, column=1)
        self.addFileButton = tk.Button(button_frame, text='Add BOM File', width=10, command=self.add_files)
        self.addFileButton.grid(row=0, column=2)
        self.save_and_merge_button = tk.Button(button_frame, text='Save and Merge', width=10, state=tk.DISABLED, command=self.save_and_merge)
        self.save_and_merge_button.grid(row=0, column=3)
        button_frame.grid(row=0)

        self.files_widget = bom_files_table(self, on_empty=self.refresh)
        self.files_widget.grid(row=2)

        self.result = None
        self.projectDir = None        
        if project_filename:
           self.load_project_and_update_widget(project_filename)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_window(self)


    def load_project(self, filename):
        raise RuntimeError("Unimplemented")


    def save_project_file(self, filename):
        raise RuntimeError("Unimplemented")


    def get_initial_dir(self):
        if self.projectDir:
            initial_dir = self.projectDir
        else:
            from os.path import expanduser
            initial_dir = expanduser("~")
        return initial_dir


    def save_project(self):   
        filename = filedialog.asksaveasfilename(initialdir = self.get_initial_dir(), title = "Save file",filetypes = (("BOM merger project","*.bomproj"),("all files","*.*")))
        if filename:
            self.projectDir = os.path.dirname(filename)
            self.project_filename = filename
            self.save_project_file(filename)
            return True
        return False

            
    def save_and_merge(self):
        if self.save_project():
            self.result = self.project_filename
            self.destroy()

    def load_project_and_update_widget(self, filename):
        project = self.load_project(filename)
        for file in project:
            self.files_widget.add_file(file['filename'], file['Quantity'])
        self.projectDir = os.path.dirname(filename)
        self.refresh()


    def open_project(self):
        filename = filedialog.askopenfilename(initialdir = self.get_initial_dir(),title = "Select files",filetypes = (("BOM merger project","*.bomproj"),("all files","*.*")))  
        if filename:
            self.load_project_and_update_widget(filename)


    def add_files(self):
        filenames = filedialog.askopenfilenames(initialdir = self.get_initial_dir(), title = "Select files", filetypes = (("CSV","*.csv"), ("all files","*.*")))
        if filenames:
            for filename in filenames:
                self.files_widget.add_file(filename)
            self.refresh()


    def refresh(self):
        if self.files_widget.is_empty():
            self.save_and_merge_button.config(state=tk.DISABLED)
            self.saveProjectButton.config(state=tk.DISABLED)
        else:
            self.save_and_merge_button.config(state=tk.NORMAL)
            self.saveProjectButton.config(state=tk.NORMAL)

