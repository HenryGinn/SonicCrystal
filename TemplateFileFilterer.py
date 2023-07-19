"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

This takes data from a collection of files and reduces the resolution.
The output is put into a single file, and the filtering works by taking
an average of values within a window (not a moving window).
"""

import os

from hgutilities.utils import read_from_path
from hgutilities.utils import save_to_path
from hgutilities.utils import get_group_indexes_fill
import numpy as np

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day = "12"
description = "Test"

#source_file_name = "meas_plotter_20230629_140217"
#source_file_name = "meas_plotter_20230629_152434"
source_file_name = "meas_plotter_20230629_153028"
reduction_factor = 1000
averaging_key = "Impedance (F)"
header_separator = ", "
data_separator = "; "
lines_to_ignore_at_start_of_file = 4

# Source and output folder
folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal2\\"
             f"Processed Data\\{folder_name}\\Data")
source_path = os.path.join(base_path, "Big Files", f"{source_file_name}.txt")
output_path = os.path.join(base_path, "Filtered Files", f"{source_file_name}.txt")
print(f"Output folder: {output_path}\n")

print("Reading data from source files. This may take a minute or two")
data = read_from_path(source_path, data_separator=data_separator,
                      header_separator=header_separator,
                      skip_first_n=lines_to_ignore_at_start_of_file)
row_count = len(data[list(data.keys())[0]])
group_indices = get_group_indexes_fill(row_count, reduction_factor)

def get_filtered_values(values):
    groups = [values[indices] for indices in group_indices]
    filtered_values = [np.mean(group) for group in groups]
    return filtered_values

filtered_data = {key: get_filtered_values(values)
                 for key, values in data.items()}
save_to_path(output_path, filtered_data)
