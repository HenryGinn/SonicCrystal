"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

The purpose of this script is to take the impedance data and create a figure
where a single parameter is shown against frequency. If the data has been
split over multiple files (for very large sweeps for example), that data
is combined and shown on one plot.
"""

import os

import hgutilities.plotting as plotting
from hgutilities.utils import combine_files

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = 
day = 
description = 

# Parameter names
# frequency, absz, abszstddev
# realz, imagz, realzstddev, imagzstd,
# param0, param0stddev, param1, param1stddev,
# phasez, phasezstddev, nexttimestamp

parameter = "param1"

folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal3\\Processed Data"
             f"\\{folder_name}\\28 Cooling Down\\")
data_path = os.path.join(base_path, "Data", "Impedance")

def get_line_obj():
    data = combine_files(data_path)
    x_values = data["frequency"]
    y_values = data[parameter]
    line_obj = plotting.line(x_values, y_values)
    return line_obj

title = f"{folder_name} Impedance"
line_objects = [get_line_obj()]

# If all the lines are desired to be the same colour, add
# a value for the "color" keyword argument in this line.
lines_objects = plotting.lines(line_objects, legend=False)
plotting.create_figures(lines_objects, title=title,
                        output="Both", base_path=base_path, plots_folder=True)

