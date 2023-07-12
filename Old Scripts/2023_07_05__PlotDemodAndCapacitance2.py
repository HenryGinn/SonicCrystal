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

folder_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Processing Data\\"
                 "2023_07_04__DemodAndCapacitance2\\Data\\Voltage_10_V\\Demod_1")

parameter = "r"

def get_lines_obj(path):
    line_obj = get_line_obj(path)
    line_objects = [line_obj]
    lines_obj = plotting.lines(line_objects, y_label=parameter)
    return lines_obj

def get_line_obj(path):
    data = combine_files(path, blacklist="Parameters")
    x_values = data["frequency"]
    y_values = data[parameter]
    line_obj = plotting.line(x_values, y_values)
    return line_obj

lines_obj = get_lines_obj(folder_path)
plotting.create_figures([lines_obj])
