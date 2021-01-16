# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Dec  7 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.dataview

try:
    import mergeDialog
    import partDetailDialog
except:
    from gui.mergeDialog import MergeDialog
    from gui.partDetailDialog import PartDetailDialog


###########################################################################
## Class MyFrame2
###########################################################################

class ComponentGroup(wx.Panel):
    def __init__(self, parent, name, columns, on_double_click):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.parent = parent
        self.on_double_click = on_double_click
        self.name = name
        self.columns = columns
        self.m_treeListCtrl2 = wx.ListView(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__on_double_click, id=self.m_treeListCtrl2.GetId())
        for column in columns:
            self.m_treeListCtrl2.AppendColumn(column)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)
        bSizer7.Add(self.m_treeListCtrl2, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(bSizer7)
        self.Layout()
        bSizer7.Fit(self)

    def add_items(self, components, validation_status):
        for index, component in enumerate(components):
            item_number = self.m_treeListCtrl2.GetItemCount()
            self.m_treeListCtrl2.InsertItem(item_number, item_number)
            for i, column in enumerate(self.columns):
                if column in component:
                    self.m_treeListCtrl2.SetItem(item_number, i, str(component[column]))

            if validation_status[index] is None:
                self.m_treeListCtrl2.SetItemBackgroundColour(item_number, wx.WHITE)
            elif validation_status[index] == "IncorrectParameters":
                self.m_treeListCtrl2.SetItemBackgroundColour(item_number, wx.YELLOW)
            elif validation_status[index] == "IncorrectParameters":
                self.m_treeListCtrl2.SetItemBackgroundColour(item_number, wx.RED)

    def remove_all_components(self):
        self.m_treeListCtrl2.DeleteAllItems()

    def get_selected_items(self):
        selected_items = []
        item = -1
        while True:
            item = self.m_treeListCtrl2.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if item == -1:
                break
            selected_items.append(item)
        return selected_items

    def __on_double_click(self, event):
        self.on_double_click(event.GetIndex())


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Bommerger", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Open project", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)

        self.m_menuItem3 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"New Project", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem3)

        self.menu_item_export = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Export", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.menu_item_export)

        self.m_menu1.AppendSeparator()

        self.m_menuItem2 = wx.MenuItem(self.m_menu1, wx.ID_EXIT, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem2)

        self.m_menubar1.Append(self.m_menu1, u"File")

        self.SetMenuBar(self.m_menubar1)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_auinotebook1 = wx.aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                 wx.aui.AUI_NB_DEFAULT_STYLE)
        self.components = {}
        self.component_groups = {}
        bSizer5.Add(self.m_auinotebook1, 1, wx.EXPAND | wx.ALL, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer6.Add((0, 0), 1, wx.EXPAND, 5)

        self.merge_button = wx.Button(self, wx.ID_ANY, u"Merge", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.merge_button, 0, wx.ALL, 5)

        self.delete_button = wx.Button(self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.delete_button, 0, wx.ALL, 5)

        self.start_ordering_button = wx.Button(self, wx.ID_ANY, u"Start Ordering", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        bSizer6.Add(self.start_ordering_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer6.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer5.Add(bSizer6, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer5)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.open_project, id=self.m_menuItem1.GetId())
        self.Bind(wx.EVT_MENU, self.new_project, id=self.m_menuItem3.GetId())

        self.Bind(wx.EVT_BUTTON, self.delete_components, id=self.delete_button.GetId())
        self.Bind(wx.EVT_BUTTON, self.merge_components, id=self.merge_button.GetId())

    def add_components_group(self, components):
        self.components[components.name] = components
        tmp = ComponentGroup(self.m_auinotebook1, components.name, components.visible_parameters, self.show_component_detailed_data)
        self.m_auinotebook1.AddPage(tmp, tmp.name, False, wx.NullBitmap)
        self.component_groups[components.name] = tmp
        tmp.add_items(self.components[components.name].components, self.components[components.name].validation_status)

    def __del__(self):
        pass

    def clear_gui(self):
        self.components = {}
        self.m_auinotebook1.DeleteAllPages()
        self.component_groups = {}

    def delete_components(self, event):
        components_group = self.component_groups[
            self.m_auinotebook1.GetPageText(self.m_auinotebook1.GetSelection())]
        selected_items = components_group.get_selected_items()
        self.__delete_components_by_index(components_group.name, selected_items)
        self.__refresh_components_list_view(components_group.name)

    def merge_components(self, event):
        components_group = self.component_groups[
            self.m_auinotebook1.GetPageText(self.m_auinotebook1.GetSelection())]
        selected_items = components_group.get_selected_items()
        print("Merging components:", selected_items)
        components_to_merge = self.get_selected_components_list()
        merged = MergeDialog(self, components_group.columns, components_to_merge)
        merged.ShowModal()
        if merged.result:
            self.__delete_components_by_index(components_group.name, selected_items)
            component = self.__component_from_dictionary(merged.result)
            self.components[components_group.name].append(component)
            self.__refresh_components_list_view(components_group.name)

    def get_selected_components_list(self):
        components_group = self.component_groups[
            self.m_auinotebook1.GetPageText(self.m_auinotebook1.GetSelection())]
        selected_items = components_group.get_selected_items()
        result = []
        for item in selected_items:
            result.append(self.components[components_group.name].get_component(item))
        return result

    def open_project(self, event):
        openFileDialog = wx.FileDialog(None, "Open", "", "",
                                       "BOM merge project (*.bomproj)|*.bomproj",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        result = openFileDialog.ShowModal()
        if result == wx.ID_OK:
            path = openFileDialog.GetPath()
            print(path)
            window = self.project_config_widget(path)
            window.ShowModal()
        openFileDialog.Destroy()
        self.on_project_open(path)

    def new_project(self, event):
        window = self.project_config_widget()
        window.ShowModal()

    def project_config_widget(self, path=None):
        raise RuntimeError("Unimplemented")

    def on_project_open(self, path):
        raise RuntimeError("Unimplemented")

    def show_component_detailed_data(self, index):
        components_group = self.component_groups[
            self.m_auinotebook1.GetPageText(self.m_auinotebook1.GetSelection())]
        print("Show component detail:", components_group.name, "index:", index)
        components = self.components[components_group.name]
        dialog = PartDetailDialog(self, components.get_component(index), components.resolve_component_parameters(index))
        dialog.ShowModal()

    @staticmethod
    def __component_from_dictionary(component_dict):
        integer_keys = ["Quantity"]
        result = {}
        for key in component_dict:
            if key in integer_keys:
                result[key] = int(component_dict[key])
            else:
                result[key] = component_dict[key]
        return result

    def __refresh_components_list_view(self, components_group_name):
        components_group = self.component_groups[components_group_name]
        components_group.remove_all_components()
        components_group.add_items(self.components[components_group_name].components, self.components[components_group_name].validation_status)

    def __delete_components_by_index(self, components_group, selected_items):
        """
        :param components_group: name of component group
        :param selected_items: array of indices to remove
        :return:
        """
        print("Removing components from:", components_group, "index:", selected_items)
        self.components[components_group].remove_components_by_index(selected_items)



if __name__ == "__main__":
    app = wx.App()
    # Create open file dialog
    frame = MainFrame(None)
    components = {"Capacitors": [{"Quantity": 100, "Capacitance": "100nF", "Voltage": "16V", "Tolerance": "10%", "Designator": ""},
                                 {"Quantity": 200, "Capacitance": "200nF", "Voltage": "16V", "Tolerance": "5%", "Designator": ""},
                                 {"Quantity": 50, "Capacitance": "100nF", "Voltage": "25V", "Tolerance": "5%", "Designator": ""}],
                  "Resistors": [{"Quantity": 100, "Resistance": "100R", "Tolerance": "10%"}]}
    frame.set_components("Capacitors", components["Capacitors"])
    frame.Show()
    app.MainLoop()
