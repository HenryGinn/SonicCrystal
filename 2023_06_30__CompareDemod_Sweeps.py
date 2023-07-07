import os

import hgutilities.plotting as plotting

from tools.combinefiles import combine_files

folder_path_1 = "D:\\Documents\\Experiments Data\\SonicCrystal\\2023_06_28__BackgroundFrequencySweep"
folder_path_2 = "D:\\Documents\\Experiments Data\\SonicCrystal\\2023_06_29__HeliumFrequencySweep"

parameter = "r"

demod_paths_1 = [os.path.join(folder_path_1, folder_name)
                 for folder_name in os.listdir(folder_path_1)]
demod_paths_2 = [os.path.join(folder_path_2, folder_name)
                 for folder_name in os.listdir(folder_path_2)]

def get_lines_obj(demod_path_1, demod_path_2):
    line_obj_1 = get_line_obj(demod_path_1, "Background")
    line_obj_2 = get_line_obj(demod_path_2, "Helium")
    line_objects = [line_obj_1, line_obj_2]
    lines_obj = plotting.lines(line_objects, legend=True)
    return lines_obj

def get_line_obj(demod_path, label):
    data = combine_files(demod_path, blacklist="Parameters")
    x_values = data["frequency"]
    y_values = data[parameter]
    line_obj = plotting.line(x_values, y_values, label=label)
    return line_obj

for demod_index, (demod_path_1, demod_path_2) in enumerate(zip(demod_paths_1, demod_paths_2)):
    lines_obj = get_lines_obj(demod_path_1, demod_path_2)
    plotting.create_figures([lines_obj], suptitle = f"DemodIndex_{demod_index + 1}")
