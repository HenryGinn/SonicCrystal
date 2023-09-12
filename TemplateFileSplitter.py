"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

If the data from an experiment has been put into very large files, it may
be desired that they are split up into smaller ones. This program does that.
Its main purpose is for data attained from the plotter section of LabOne.
"""

import os

from hgutilities.utils import read_from_path
from hgutilities.utils import save_to_path
from hgutilities.utils import get_group_indexes_fill

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day = 
description = 

source_file_name = 
start_output_file_numbering_at = 1
rows_per_file = 50000
lines_to_ignore_at_start_of_file = 0
data_separator = 

# Source and output folder
folder_name = f"{year}_{month}_{day}__{description}"
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal3\\"
             f"Processed Data\\{folder_name}\\Data")
source_path = os.path.join(base_path, "Big Files", f"{source_file_name}.txt")
output_path = os.path.join(base_path, "Split Files")
print(f"Output folder: {output_path}\n")

print("Reading data from source file. This may take a minute or two")
data = read_from_path(source_path, separator=data_separator,
                      skip_first_n=lines_to_ignore_at_start_of_file)
row_count = len(data[list(data.keys())[0]])
group_indicies = get_group_indexes_fill(row_count, rows_per_file)

for file_index, indicies in enumerate(group_indicies):
    file_number = file_index + start_output_file_numbering_at
    percentage = round(100 * file_index * rows_per_file / row_count, 1)
    print(f"File number: {file_number}, percentage: {percentage}%")
    split_data = {key: value[indicies]
                  for key, value in data.items()}
    file_name = f"{source_file_name}__FileNumber_{file_number}.txt"
    path = os.path.join(output_path, file_name)
    save_to_path(path, split_data)
