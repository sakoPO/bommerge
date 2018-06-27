import os
    
    
def load_json_file(filename):
    import json
    with open(filename) as inputfile:
       dictionary = json.load(inputfile)
    return dictionary


def save_json_file(filename, content):
    import json
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(content, indent=4, sort_keys=True, separators=(',', ': ')))


def replace_file_extension(filename, newExtension):
    return os.path.splitext(filename)[0] + newExtension


def get_file_extension(filename):
    print(filename)
    filename, file_extension = os.path.splitext(filename)
    return file_extension


def get_user_home_directory():
    from os.path import expanduser
    return expanduser("~")


def file_exist(file_path):
    if os.path.exists(get_directory_from_path(file_path)) and os.path.isfile(file_path):
        return True
    return False


def get_filename_from_path(path):
    import ntpath
    return ntpath.basename(path)


def get_directory_from_path(path):
    absoluteProjectFilenamePath = os.path.abspath(path)
    return os.path.dirname(absoluteProjectFilenamePath)


def copy(src, dst):
    import shutil
    shutil.copyfile(src, dst)


def make_directory_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
