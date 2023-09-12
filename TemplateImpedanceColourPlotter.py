"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

The purpose of this script is to take the impedance data and create a figure
where a single parameter is shown against frequency. If the data has been
split over multiple files, that data is combined and shown on one plot.

This script is based on TemplateImpedancePlotter
"""

import os

import numpy as np
import hgutilities.plotting as plotting
from hgutilities.utils import read_from_path

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day = "27"
description = "Circulating"
subfolder = "28 Cooling Down Test"

# Parameter names
# frequency, absz, abszstddev
# realz, imagz, realzstddev, imagzstd,
# param0, param0stddev, param1, param1stddev,
# phasez, phasezstddev, nexttimestamp

parameter = "param1"

folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal3\\Processed Data"
             f"\\{folder_name}\\{subfolder}")
data_path = os.path.join(base_path, "Data", "Impedance")

paths = [os.path.join(data_path, file_name)
         for file_name in os.listdir(data_path)]
data = [read_from_path(path) for path in paths]

x_values = data[0]["frequency"]
y_values = np.arange(len(data)) + 1
x_mesh, y_mesh = np.meshgrid(x_values, y_values)
z_mesh = np.array([trial_data[parameter] for trial_data in data])

colorplot_objects = [plotting.colorplot(x_mesh, y_mesh, z_mesh)]

suptitle = f"{folder_name}, {subfolder} Impedance: {parameter}"

# If all the lines are desired to be the same colour, add
# a value for the "color" keyword argument in this line.
plotting.create_figures(colorplot_objects, suptitle=suptitle,
                        output="Both", base_path=base_path, plots_folder=True)

