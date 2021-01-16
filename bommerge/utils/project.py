from . import files
import os


def load(filename):
    project = files.load_json_file(filename)
    project_directory = files.get_directory_from_path(filename)
    print("Loading project: " + project_directory)
    for file in project:
        if not os.path.isabs(file['filename']):
            file['filename'] = os.path.normpath(os.path.join(project_directory, file['filename']))
    print(project)
    return project


def save(filename, project):
    project_directory = files.get_directory_from_path(filename)
    for file in project:
        normalized_path = os.path.normpath(file['filename'])
        print(normalized_path)
        file['filename'] = os.path.relpath(normalized_path, project_directory)
    files.save_json_file(filename, project)
