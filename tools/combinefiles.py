import os

import numpy as np
from hgutilities.utils.readwrite import save_to_path, read_from_path

def save_combined_files(folder_path, name="Combined.txt", blacklist=None):
    results_path = os.path.join(folder_path, name)
    data = combine_files(folder_path, name=name, blacklist=blacklist)
    save_to_path(results_path, data)

def combine_files(folder_path, name="Combined.txt", blacklist=None):
    paths = get_paths(folder_path, blacklist)
    data = get_data(paths)
    return data

def get_data(paths):
    contents = [read_from_path(path) for path in paths]
    header = list(contents[0].keys())
    data = {key: np.concatenate([partial_contents[key]
                                 for partial_contents in contents],
                                axis=0)
            for key in header}
    return data

def get_paths(folder_path, blacklist):
    paths = [os.path.join(folder_path, file_name)
             for file_name in os.listdir(folder_path)
             if blacklist not in file_name]
    return paths
