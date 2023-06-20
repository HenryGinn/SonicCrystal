"""
This program takes data from the "Circulator" script (sweeps the device)
and plots the results.

These are the quantities saved from the sweeps and what they correspond to.

param0: capacitance
param1: resistance
absz
realz
imagz
phasez

All of the above also have their standard deviations saved.
To access these, add "stddev" on the end, e.g. "param0stddev".
"frequency" and "nexttimestamp" are also recorded.

To change the data being plotted, follow the example below:

    # The y values
    capacitance = data_dict["param1"]

    # Creating a line object
    # This contains data about the data series, not the plot
    line_obj = plotting.line(frequency, capacitance)

    # Creating a lines object
    # This contains data about the plot, not the data series
    lines_obj = plotting.lines(line_obj, y_label="My y label", title="My title")

The plotting function takes in a list of lines objects,
so remember to add your lines_obj to the list.

Most matplotlib parameters can be changed by passing a keyword argument
into the relevant object (follow common sense or check docs) with the
same keyword name as when usually working with matplotlib subplots.

For more help, run "help(plotting)" or check the README:
https://github.com/HenryGinn/hgutilities/tree/main/hgutilities/plotting
"""

import os
import math

from hgutilities import plotting
from hgutilities.utils.paths import make_folder
from tools import read_from_path
from tools import read_file_name

def get_paths_grouped_by_setting_sweep(group_size):
    paths = get_paths()
    paths_dict = get_paths_dict(paths)
    path_groups = get_path_groups(paths, paths_dict, group_size)
    return path_groups

def get_paths():
    paths = [os.path.join(data_path, file_name)
             for file_name in os.listdir(data_path)
             if file_name != "Parameters.txt"]
    return paths

def get_paths_dict(paths):
    paths_dict = {path: read_file_name(os.path.split(path)[1])
                  for path in paths}
    return paths_dict

def get_path_groups(paths, paths_dict, group_size):
    path_groups = get_path_groups_unsorted(paths, paths_dict, group_size)
    path_groups = [sorted(paths_group)
                   for paths_group in path_groups]
    return path_groups

def get_path_groups_unsorted(paths, paths_dict, group_size):
    path_groups = [[path for path in paths
                    if (group_size*index <= paths_dict[path]["SweepNumber"]
                        and paths_dict[path]["SweepNumber"] < group_size*(index+1))]
                   for index in range(math.ceil(len(paths) / group_size))]
    return path_groups


def create_figure(index, path_group, lines_obj_function, name):
    lines_objects = [lines_obj_function(sweep_path)
                     for sweep_path in path_group]
    suptitle = f"Effect of Different Settings on {name} Precision {index + 1}"
    file_name = f"Measurement_{name}__Index_{index + 1}"
    plotting.create_figures(lines_objects, axis_fontsize=12, suptitle=suptitle,
                            title_fontsize=15, suptitle_fontsize=20, output="Save",
                            base_path=plots_path, file_name=file_name, format="png")
    
def get_lines_obj_resistance(sweep_path):
    lines_obj = get_lines_obj(sweep_path, "param0")
    lines_obj.y_label = "Resistance"
    return lines_obj

def get_lines_obj_capacitance(sweep_path):
    lines_obj = get_lines_obj(sweep_path, "param1")
    lines_obj.y_label = "Capacitance"
    lines_obj.plot_type = "semilogy"
    return lines_obj

def get_lines_obj_absz(sweep_path):
    lines_obj = get_lines_obj(sweep_path, "absz")
    lines_obj.y_label = "|Z|"
    lines_obj.plot_type = "semilogy"
    return lines_obj
    
def get_lines_obj_phasez(sweep_path):
    lines_obj = get_lines_obj(sweep_path, "phasez")
    lines_obj.y_label = "arg(Z)"
    return lines_obj


def get_lines_obj(sweep_path, parameter_name):
    frequency, values = get_frequency_and_values(sweep_path, parameter_name)
    line_obj = plotting.line(frequency, values)
    title = get_title(sweep_path)
    lines_obj = plotting.lines(line_obj, x_label="Frequency", title=title,
                               xlim_lower=0, xlim_upper=5e6)
    return lines_obj

def get_frequency_and_values(path, parameter):
    data_dict = read_from_path(path)
    frequency = data_dict["frequency"][ignore_first:]
    values = data_dict[parameter][ignore_first:]
    return frequency, values

def get_title(sweep_path):
    sweep_metadata = read_file_name(os.path.split(sweep_path)[1])
    title = (f"Drive Voltage: {sweep_metadata['DriveVoltage']}, "
             f"Bias Voltage: {sweep_metadata['BiasVoltage']}")
    return title


data_path = "/home/henry/Documents/Other Programming/Physics Internship/SonicCrystal/DataSets/2023-06-16"
plots_path = "/home/henry/Documents/Other Programming/Physics Internship/SonicCrystal/Plots/2023-06-16"
make_folder(plots_path)

paths_grouped_by_setting_sweep = get_paths_grouped_by_setting_sweep(10)

ignore_first = 100

line_obj_functions = [get_lines_obj_resistance,
                      get_lines_obj_capacitance,
                      get_lines_obj_absz,
                      get_lines_obj_phasez]
names = ["Resistance", "Capacitance", "AbsZ", "PhaseZ"]

for index, path_group in enumerate(paths_grouped_by_setting_sweep):
    for line_obj_function, name in zip(line_obj_functions, names):
        create_figure(index, path_group, line_obj_function, name)
