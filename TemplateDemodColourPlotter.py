"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

The purpose of this script is to take the demodulator data and create
a figure where all the demods are on the same plot, and a single parameter
is shown against frequency. If the data for each demod has been split over
multiple files, that data is combined and shown on one plot.

This script is based on TemplateDemodPlotter
"""

"""
This script is based on TemplateDemodColourPlotter
"""

import os

import numpy as np
import hgutilities.plotting as plotting
from hgutilities.utils import read_from_path

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day = "28"
description = "Circulating"
#subfolder = "28 Cooling Down Test"

# Parameter names
# frequency, r, phase, x, y, rstddev,
# phasestddev, xstddev, ystddev, nexttimestamp

parameter = "r"

folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data"
             f"\\{folder_name}")
data_path = os.path.join(base_path, "Data")

demod_paths = [os.path.join(data_path, folder_name)
               for folder_name in os.listdir(data_path)
               if folder_name != "Impedance"]

def get_colorplot_obj(demod_path):
    paths = [os.path.join(demod_path, file_name)
             for file_name in os.listdir(demod_path)]
    data = [read_from_path(path) for path in paths]

    x_values = data[0]["frequency"]
    y_values = np.arange(len(data)) + 1
    x_mesh, y_mesh = np.meshgrid(x_values, y_values)
    z_mesh = np.array([trial_data[parameter] for trial_data in data])

    title = os.path.split(demod_path)[1]
    colorplot_obj = plotting.colorplot(x_mesh, y_mesh, z_mesh, title=title)
    return colorplot_obj

colorplot_objects = [get_colorplot_obj(demod_path)
                     for demod_path in demod_paths]

suptitle = f"{folder_name}, Demods: {parameter}"

plotting.create_figures(colorplot_objects, suptitle=suptitle,
                        output="Both", base_path=base_path, plots_folder=True)
