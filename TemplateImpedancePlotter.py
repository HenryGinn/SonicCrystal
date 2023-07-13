import os

import hgutilities.plotting as plotting
from hgutilities.utils import combine_files

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day =
description =

# Parameter names
# frequency, absz, abszstddev
# realz, imagz, realzstddev, imagzstd,
# param0, param0stddev, param1, param1stddev,
# phasez, phasezstddev, nexttimestamp

parameter = "r"

folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data"
             f"\\{folder_name}\\Data\\Impedance")

def get_line_obj():
    data = combine_files(base_path)
    x_values = data["frequency"]
    y_values = data[parameter]
    line_obj = plotting.lines(x_values, y_values)
    return line_obj

title = f"{folder_name} Impedance"
line_objects = [get_line_obj()]
lines_objects = plotting.lines(line_objects, legend=True)
plotting.create_figures(lines_objects, title=title,
                        output="Both", base_path=base_path, plots_folder=True)

