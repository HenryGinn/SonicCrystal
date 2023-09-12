"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

A HDF5 file (extension name is .h5) stores data in a tree like structure.
They can be opened with Visual Studio Code using an extension, but you
cannot copy and paste the data.

This program reads the contents of the HDF5 file and puts it into
folders with the same structure. The arrays are put into text documents.
If the arrays are two dimensional then there the dimensions will span the
columns. If instead there are multiple one dimensional arrays within a
group then they will be put into one file where each array is one column.

This program is based off HDF5Converter. A file with the temperature log
that contains the time period where the measurements were taken is provided.
When the arrays are one dimensional a column for the temperature is added.
These values are interpolated, and as the temperature is only taken every
five seconds there can be long sequences of equal temperattures.
"""

import os

import h5py
import numpy as np
from hgutilities.utils import make_folder
from hgutilities.utils import save_to_path
from hgutilities.utils import read_from_path


# Base path is the directory where the HDF5 file is located
# The string literal is deliberately unterminated as a reminder
# to complete the path.
#
# The temperature path gives the location of the temperature log
# file that was taken from FridgeDaddy.
# This program assumes that the file has been renamed to "Temperature.txt".
base_path = "D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data\\
source_path = os.path.join(base_path, "sweep_00000.h5")
temperature_path = os.path.join(base_path, "Temperature.txt")

file_name = os.path.split(source_path)[1]
folder_name = os.path.splitext(file_name)[0]
destination_path = os.path.join(base_path, folder_name)


# For more information see the "Timestamps"
# file in the "Documentation" folder.
#clockbase = 1800000000  # MFIA
clockbase = 210000000   # HF2LI
temperature_dict = get_temperature_dict(temperature_path)

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
        print(self.key)
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
        data = self.get_data()
        timestamp, zi_timestamp, path_temperature = self.get_timestamp()
        data = self.add_temperature_column(data, timestamp, zi_timestamp)
        path = os.path.join(f"{self.path}__{path_temperature}.txt")
        save_to_path(path, data)

    def write_data_two_dimension(self):
        make_folder(self.path)
        for index in range(self.children[0].obj.shape[0]):
            timestamp, zi_timestamp, path_temperature = self.get_timestamp()
            data = self.add_temperature_column(data, timestamp, zi_timestamp)
            path = os.path.join(self.path, f"Index_{index}__{path_temperature}.txt")
            save_to_path(path, data)

    def get_data(self):
        data = {child.name: child.obj
                for child in self.children
                if child.obj.shape[0] > 1}
        return data

    def get_timestamp(self):
        chunkheader = [child.obj for child in self.children
                       if "chunkheader" in child.key][0]
        timestamp = chunkheader[0][-3]
        zi_timestamp = chunkheader[0][6]
        path_temperature = f"Timestamp_{timestamp}__ZurichTimestamp_{zi_timestamp}"
        return timestamp, zi_timestamp, path_temperature

    def add_temperature_column(self, data, timestamp, zi_timestamp):
        timestamps = (data["nexttimestamp"] - zi_timestamp)/ clockbase + timestamp
        temperatures = get_temperatures(timestamps)
        data["Temperature"] = temperatures
        return data

    def __str__(self):
        string = (f"Name: {self.key}\n"
                  f"Path length: {self.path_length}\n")
        return string


def get_temperature_dict(path):
    temperature_data = read_from_path(path)
    keys = list(temperature_data.keys())
    temperature_dict = {"Timestamp": temperature_data[keys[0]] - 2082844800,
                        "Temperature": temperature_data[keys[1]]}
    return temperature_dict

def get_temperatures(timestamps):
    temperatures = np.interp(timestamps,
                             temperature_dict["Timestamp"],
                             temperature_dict["Temperature"])
    return temperatures

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
        data = Data(key_name, file[key_name])
        datas.append(data)

def find_relations():
    for data in datas:
        data.find_relations()

def write_data():
    for data in datas:
        if data.parent is None:
            data.write_data()

datas = []
read_hdf5(source_path)
