import os

import numpy as np
from hgutilities.utils.groups import get_group_indexes_fill

lines_per_file = 1000000

base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\"
             "2023_06_29__HeliumInCell")

file_number = "153028"
file_name = f"meas_plotter_20230629_{file_number}.txt"
source_path = os.path.join(base_path, file_name)

lines_at_start_to_ignore = 4

with open(source_path, "r") as file:
    for line_number in range(lines_at_start_to_ignore):
        file.readline()
    header = file.readline().strip().split(", ")
    data = [[float(number) for number in line.strip().split("; ")]
             for line in file]

group_indexes = get_group_indexes_fill(len(data), lines_per_file)

data = list(zip(*data))
data = [np.array(column) for column in data]
data[0] += 1688049028
data = [list(zip(*[column[indexes] for column in data]))
        for indexes in group_indexes]

for file_index, data_partial in enumerate(data):
    file_name = f"AveragedResults__File_{file_number}__Index_{file_index}.txt"
    print(file_index)
    results_path = os.path.join(base_path, file_name)
    with open(results_path, "w") as file:
        file.writelines("\t".join(header))
        file.writelines("\n")
        for line in data_partial:
            file.writelines("\t".join([str(value) for value in line]))
            file.writelines("\n")
