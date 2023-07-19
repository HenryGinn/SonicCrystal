"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

The purpose of this script is to take the demodulator data and create
a figure where all the demods are on the same plot, and a single parameter
is shown against frequency. If the data for each demod has been split over
multiple files, that data is combined and shown on one plot.
"""

import os

import hgutilities.plotting as plotting
from hgutilities.utils import combine_files

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day =
description = 

# Parameter names
# frequency, r, phase, x, y, rstddev,
# phasestddev, xstddev, ystddev, nexttimestamp

parameter = "r"

folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data"
             f"\\{folder_name}\\Data")

demod_paths = [os.path.join(base_path, folder_name)
               for folder_name in os.listdir(base_path)
               if folder_name != "Impedance"]

def get_line_obj(demod_path):
    data = combine_files(demod_path)
    x_values = data["frequency"]
    y_values = data[parameter]
    label = os.path.split(demod_path)[1]
    line_obj = plotting.lines(x_values, y_values, label=label)
    return line_obj

title = f"{folder_name} Demods"
line_objects = [get_line_obj(demod_path) for demod_path in demod_paths]

# If all the lines are desired to be the same colour, add
# a value for the "color" keyword argument in this line.
lines_objects = plotting.lines(line_objects, legend=True,
                               x_label="Frequency (Hz)", y_label=parameter)

plotting.create_figures(lines_objects, title=title,
                        output="Both", base_path=base_path, plots_folder=True)
