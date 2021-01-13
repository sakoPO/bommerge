import os
import wx
import wx.xrc
import ntpath


class FileQuantityWidget(wx.BoxSizer):
    def __init__(self, parent, remove_callback):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.filename = ''

        self.entry = wx.TextCtrl(parent, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.entry.SetMinSize(wx.Size(500, 10))
        self.entry.Disable()
        self.spinbox = wx.SpinCtrl(parent, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0)
        self.spinbox.Disable()
        self.removeButton = wx.Button(parent, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0)
        self.removeButton.Bind(wx.EVT_BUTTON, lambda x, y: remove_callback(self.filename))
        self.removeButton.Enable(False)

        self.Add(self.entry, 1, wx.ALL | wx.EXPAND, 5)
        self.Add(self.spinbox, 0, wx.ALL, 5)
        self.Add(self.removeButton, 0, wx.ALL, 5)

    def get_quantity(self):
        return int(self.spinbox.GetValue())

    def set_quantity(self, quantity):
        if self.filename == '':
            raise RuntimeError("Adding quantity to uninitialized widget")
        self.spinbox.SetValue(quantity)

    def get_filename(self):
        return self.filename

    def is_empty(self):
        return self.filename == ''

    def clear(self):
        self.entry.ChangeValue("")
        self.spinbox.SetValue(0)
        self.filename = ''
        self.removeButton.Disable()
        self.spinbox.Disable()

    def update(self, filename, quantity):
        if filename != '':
            self.removeButton.Enable(True)
            basename = ntpath.basename(filename)
            self.entry.ChangeValue(basename)
            self.spinbox.Enable(True)
            self.spinbox.SetValue(quantity)
            self.filename = filename


class BomFilesTable(wx.ScrolledWindow):
    def __init__(self, parent, on_empty):
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.bom_files = []
        self.on_empty = on_empty
        self.create_empty_rows()
        self.SetScrollRate(5, 5)
        self.SetSizer(self.sizer)
        self.Layout()

    def create_empty_rows(self):
        for i in range(6):
            row_widget = FileQuantityWidget(self, self.remove_file)
            self.sizer.Add(row_widget, 0, wx.ALL, 5)
            self.bom_files.append(row_widget)

    def add_file(self, filename, quantity=1):
        if self.is_on_list(filename):
            wx.MessageBox("File already in project, quantity will be increased.", "Notice", wx.OK, self)
            widget = self.bom_files[self.get_index_of(filename)]
            widget.set_quantity(widget.get_quantity() + quantity)
        else:
            print("Adding new file: " + filename)
            for widget in self.bom_files:
                if widget.is_empty():
                    widget.update(filename, 1)
                    return
            row_widget = FileQuantityWidget(self, self.remove_file)
            row_widget.update(filename, quantity)
            self.sizer.Add(row_widget, 0, wx.ALL, 5)
            self.bom_files.append(row_widget)

    def get_index_of(self, filename):
        for i, row in enumerate(self.bom_files):
            if row.get_filename() == filename:
                return i

    def remove_file(self, filename):
        file_index = self.get_index_of(filename)
        for i in range(file_index, len(self.bom_files) - 1):
            if self.bom_files[i + 1].is_empty():
                self.bom_files[i].clear()
            else:
                filename_tmp = self.bom_files[i + 1].get_filename()
                quantity_tmp = self.bom_files[i + 1].get_quantity()
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


class ProjectConfigurationWidget(wx.Dialog):
    def __init__(self, parent, project_filename=None):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Project Configurator", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.saveProjectButton = wx.Button(self, wx.ID_ANY, u"Save Project", wx.DefaultPosition, wx.DefaultSize, 0)
        self.saveProjectButton.Enable(False)
        self.saveProjectButton.Bind(wx.EVT_BUTTON, self.save_project)
        self.addFileButton = wx.Button(self, wx.ID_ANY, u"Add BOM File", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addFileButton.Bind(wx.EVT_BUTTON, self.add_files)
        self.save_and_merge_button = wx.Button(self, wx.ID_ANY, u"Save and Marge", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        self.save_and_merge_button.Enable(False)
        self.save_and_merge_button.Bind(wx.EVT_BUTTON, self.save_and_merge)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add((0, 0), 1, wx.EXPAND, 5)
        buttons_sizer.Add(self.saveProjectButton, 0, wx.ALL, 5)
        buttons_sizer.Add(self.addFileButton, 0, wx.ALL, 5)
        buttons_sizer.Add(self.save_and_merge_button, 0, wx.ALL, 5)
        buttons_sizer.Add((0, 0), 1, wx.EXPAND, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(buttons_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.files_widget = BomFilesTable(self, on_empty=self.refresh)
        main_sizer.Add(self.files_widget, 1, wx.ALL | wx.EXPAND, 5)

        self.result = None
        self.projectDir = None
        self.project_filename = project_filename
        if project_filename:
            self.load_project_and_update_widget(project_filename)

        self.SetSizer(main_sizer)
        self.Layout()
        main_sizer.Fit(self)

        self.Centre(wx.BOTH)
        # Connect Events

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

    def save_project(self, event):
        if self.project_filename:
            filename = self.project_filename
        else:
            with wx.FileDialog(self, "Save file", wildcard="BOM merger project (*.bomproj)|*.bomproj",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                filename = fileDialog.GetPath()
        self.projectDir = os.path.dirname(filename)
        self.project_filename = filename
        self.save_project_file(filename)
        return True

    def save_and_merge(self, event):
        if self.save_project(event):
            self.result = self.project_filename
            self.Destroy()

    def load_project_and_update_widget(self, filename):
        project = self.load_project(filename)
        self.project_filename = filename
        for file in project:
            self.files_widget.add_file(file['filename'], file['Quantity'])
        self.projectDir = os.path.dirname(filename)
        self.refresh()

    def add_files(self, event):
        open_file_dialog = wx.FileDialog(None, "Select files", "", "",
                                         "CSV (*.csv)|*.csv",
                                         wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        result = open_file_dialog.ShowModal()
        if result == wx.ID_OK:
            filenames = open_file_dialog.GetPaths()
            for filename in filenames:
                self.files_widget.add_file(filename)
            self.refresh()

    def refresh(self):
        self.save_and_merge_button.Enable(not self.files_widget.is_empty())
        self.saveProjectButton.Enable(not self.files_widget.is_empty())
