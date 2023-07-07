#import os
#
#import hgutilities.plotting as plotting
#
#base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Processing Data\\"
#             "2023_06_30__DemodAndCapacitance\\Data")
#voltage_2 = os.path.join(base_path, "Voltage_2_V\\Impedance")
#voltage_4 = os.path.join(base_path, "Voltage_4_V\\Impedance")
#plotting.quick(voltage_2, output="Save", one_line_per_plot=False)
#plotting.quick(voltage_4, output="Save", one_line_per_plot=False)

import os

import hgutilities.plotting as plotting

from tools.combinefiles import combine_files

folder_path_1 = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Processing Data\\"
                 "2023_06_30__DemodAndCapacitance\\Data\\Voltage_2_V\\Impedance")
folder_path_2 = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Processing Data\\"
                 "2023_06_30__DemodAndCapacitance\\Data\\Voltage_4_V\\Impedance")

parameter = "param1"

def get_lines_obj(path_1, path_2):
    line_obj_1 = get_line_obj(path_1, "Background")
    line_obj_2 = get_line_obj(path_2, "Helium")
    line_objects = [line_obj_1, line_obj_2]
    lines_obj = plotting.lines(line_objects, legend=True)
    return lines_obj

def get_line_obj(path, label):
    data = combine_files(path, blacklist="Parameters")
    x_values = data["frequency"]
    y_values = data[parameter]
    line_obj = plotting.line(x_values, y_values, label=label)
    return line_obj

lines_obj = get_lines_obj(folder_path_1, folder_path_2)
plotting.create_figures([lines_obj])
