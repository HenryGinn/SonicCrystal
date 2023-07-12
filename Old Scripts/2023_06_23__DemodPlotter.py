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
from hgutilities.utils import make_folder
from hgutilities.utils import read_from_path
from hgutilities.utils import read_file_name
from hgutilities.utils import print_iterable
from hgutilities.utils import transpose_list

def get_paths_grouped_by_setting_sweep():
    paths = get_paths()
    trials = int(max([read_file_name(path)["TrialNumber"]
                      for demod_paths in paths
                      for path in demod_paths])) + 1
    path_groups = get_path_groups(paths, trials)
    return path_groups

def get_paths():
    paths = [[os.path.join(demod_folder_path, file_name)
              for file_name in os.listdir(demod_folder_path)
              if "Parameters" not in file_name]
             for demod_folder_path in demod_folder_paths]
    return paths

def get_path_groups(paths, trials):
    path_groups = [[[path for path in demod_paths
                     if read_file_name(path)["TrialNumber"] == trial_number]
                    for trial_number in range(trials)]
                   for demod_paths in paths]
    return path_groups


def create_figures(demod_index, index, path_group):
    lines_objects = [line_obj_function(path_group)
                     for line_obj_function in line_obj_functions]
    suptitle = f"Effect of Different Settings on Measurement Precision Demod_{demod_index}__Trial_{index + 1}"
    file_name = f"DemodIndex_{demod_index}__GroupIndex_{index + 1}"
    plotting.create_figures(lines_objects, axis_fontsize=12, suptitle=suptitle,
                            title_fontsize=15, suptitle_fontsize=20, output="Save",
                            base_path=plots_path, file_name=file_name, format="png",
                            universal_legend=True)
    
def get_lines_obj_x(path_group):
    lines_obj = get_lines_obj(path_group, "x")
    lines_obj.y_label = "x"
    return lines_obj

def get_lines_obj_y(path_group):
    lines_obj = get_lines_obj(path_group, "y")
    lines_obj.y_label = "y"
    #lines_obj.plot_type = "semilogy"
    return lines_obj

def get_lines_obj_r(path_group):
    lines_obj = get_lines_obj(path_group, "r")
    lines_obj.y_label = "R"
    #lines_obj.plot_type = "semilogy"
    return lines_obj
    
def get_lines_obj_phase(path_group):
    lines_obj = get_lines_obj(path_group, "phase")
    lines_obj.y_label = "Phase"
    return lines_obj

def get_lines_obj_r_stddev(path_group):
    lines_obj = get_lines_obj(path_group, "rstddev")
    lines_obj.y_label = "R Standard Deviation"
    #lines_obj.plot_type="semilogy"
    return lines_obj


def get_lines_obj(path_group, parameter_name):
    line_objects = [get_line_obj(sweep_path, parameter_name)
                    for sweep_path in path_group
                    if "DriveVoltage_0_" not in sweep_path]
    lines_obj = plotting.lines(line_objects, x_label="Frequency",
                               xlim_lower=0, xlim_upper=5e6)
    return lines_obj

def get_line_obj(sweep_path, parameter_name):
    frequency, values = get_frequency_and_values(sweep_path, parameter_name)
    file_name_data = read_file_name(os.path.split(sweep_path)[1])
    label = f"Drive_{file_name_data['DriveVoltage']}__Bias_{file_name_data['BiasVoltage']}"
    line_obj = plotting.line(frequency, values, label=label)
    return line_obj

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


#data_path = "/home/henry/Documents/Other Programming/Physics Internship/SonicCrystal/DataSets/2023-06-16"
#plots_path = "/home/henry/Documents/Other Programming/Physics Internship/SonicCrystal/Plots/2023-06-16"

data_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-23__Demod"
plots_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\Plots\\2023-06-23"
make_folder(plots_path)
demod_folder_paths = [os.path.join(data_path, file_name)
                      for file_name in os.listdir(data_path)]

paths_grouped_by_setting_sweep = get_paths_grouped_by_setting_sweep()
paths_grouped_by_setting_sweep = transpose_list(paths_grouped_by_setting_sweep)

ignore_first = 100

line_obj_functions = [get_lines_obj_x,
                      get_lines_obj_r,
                      get_lines_obj_r_stddev,
                      get_lines_obj_y,
                      get_lines_obj_phase]


for sweep_index, path_group in enumerate(paths_grouped_by_setting_sweep):
    for demod_index, demod_path in enumerate(path_group):
        create_figures(demod_index, sweep_index, demod_path)
