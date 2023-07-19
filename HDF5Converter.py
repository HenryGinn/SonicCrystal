import os

import h5py
import numpy as np
from hgutilities.utils import make_folder
from hgutilities.utils import save_to_path

class Data():

    def __init__(self, key, obj):
        self.key = key
        self.obj = obj
        self.structure = type(self.obj).__name__
        self.set_path_data()

    def set_path_data(self):
        self.h5_path = tuple(self.key.split("/"))
        self.path_length = len(self.h5_path)
        self.name = self.h5_path[-1]
        if self.structure == "Group":
            self.set_path()

    def set_path(self):
        self.path = destination_path
        for folder in self.h5_path:
            self.path = os.path.join(self.path, folder)

    def find_relations(self):
        self.find_children()
        self.find_parent()

    def find_children(self):
        self.children = [data for data in datas
                         if data.path_length == self.path_length + 1
                         if (data.h5_path[:self.path_length]
                             == self.h5_path[:self.path_length])]

    def find_parent(self):
        self.parent = [data for data in datas
                        if data.path_length == self.path_length - 1
                        if (data.h5_path[:data.path_length]
                             == self.h5_path[:data.path_length])]
        self.set_parent()

    def set_parent(self):
        if self.parent == []:
            self.parent = None
        else:
            self.parent = self.parent[0]

    def write_data(self):
        if self.has_no_grandchildren():
            self.write_data_dataset()
        else:
            self.write_data_group()

    def has_no_grandchildren(self):
        return np.any([(len(child.children) == 0)
                       for child in self.children])

    def write_data_group(self):
        make_folder(self.path)
        for child in self.children:
            child.write_data()

    def write_data_dataset(self):
        dimensions = len(self.children[0].obj.shape)
        if dimensions == 1:
            self.write_data_one_dimension()
        elif dimensions == 2:
            self.write_data_two_dimension()
        else:
            print(f"Cannot output data with {dimensions} dimensions")

    def write_data_one_dimension(self):
        data = {child.name: child.obj
                for child in self.children}
        path = os.path.join(f"{self.path}.txt")
        save_to_path(path, data)

    def write_data_two_dimension(self):
        make_folder(self.path)
        for index in range(self.children[0].obj.shape[0]):
            data = {child.name: child.obj[index]
                    for child in self.children}
            path = os.path.join(self.path, f"Index_{index}.txt")
            save_to_path(path, data)

    def __str__(self):
        string = (f"Name: {self.key}\n"
                  f"Path length: {self.path_length}\n")
        return string

def read_hdf5(path):
    key_names = []
    with h5py.File(path, 'r') as file:
        read_hdf5_from_file(key_names, file)

def read_hdf5_from_file(key_names, file):
    file.visit(key_names.append)
    create_data_objects(key_names, file)
    find_relations()
    write_data()

def create_data_objects(key_names, file):
    for key_name in key_names:
        if "chunkheader" not in key_name:
            data = Data(key_name, file[key_name])
            datas.append(data)

def find_relations():
    for data in datas:
        data.find_relations()

def write_data():
    for data in datas:
        if data.parent is None:
            data.write_data()

source_path = "D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data\\2023_07_18__HDF5Test\\a.h5"
destination_path = "D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data\\2023_07_18__HDF5Test"

file_name = os.path.split(source_path)[1]
folder_name = os.path.splitext(file_name)[0]
destination_path = os.path.join(destination_path, folder_name)

datas = []
read_hdf5(source_path)
