from gui.projectConfigurationWidget import ProjectConfigurationWidget
from gui.mainWindow import MainFrame
from parsers import csvToJson
from utils import files
from utils import project
import wx
import os
import automaticMerger
from exporters import csvExporter
from componentsGroup import ComponentsGroup


class ProjectConfigWidget(ProjectConfigurationWidget):
    def load_project(self, filename):
        return project.load(filename)

    def save_project_file(self, filename):
        project_file_list = self.files_widget.create_file_list()
        return project.save(filename, project_file_list)


def parse_files_if_needed(project_file_list, destynation):
    print("Parsing csv files and saving results to: " + destynation)
    for f in project_file_list:
        file_path = f['filename']
        if files.get_file_extension(file_path) == '.json':
            files.copy(file_path, destynation + '/' + files.get_filename_from_path(file_path))
        else:
            csvToJson.convert(file_path, destynation)


class MainWindow(MainFrame):
    def project_config_widget(self, path=None):
        return ProjectConfigWidget(self, path)

    def on_project_open(self, path):
        self.load_project(path)

    def load_project(self, project_path):
        proj = project.load(project_path)
        working_directory = files.get_directory_from_path(project_path)
        directory = working_directory + "/tmp"

        files.make_directory_if_not_exist(directory)
        parse_files_if_needed(proj, directory)

        for bom in proj:
            bom['filename'] = os.path.join(directory,
                                           files.replace_file_extension(files.get_filename_from_path(bom['filename']),
                                                                        '.json'))
        components = automaticMerger.merge(proj)
        self.clear_gui()
        for components_group in components:
            tmp = ComponentsGroup(components_group, components[components_group])
            self.add_components_group(tmp)

    def export(self, path):
        merged_dict = {}
        for components in self.components:
            merged_dict[components.name] = components.components

        files.save_json_file(os.path.join(path, 'automerged.json'), merged_dict)
        csvExporter.save(merged_dict, os.path.join(path, "mergedBOM.csv"))



def main():
    components = files.load_json_file("automerged.json")
    app = wx.App()
    frame = MainWindow(None)
    #for components_group in components:
    #    tmp = ComponentsGroup(components_group, components[components_group])
    #    frame.add_components_group(tmp)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()