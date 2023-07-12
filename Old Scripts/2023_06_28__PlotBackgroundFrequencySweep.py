import os
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
from tools import read_from_path

data_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Processing Data\\"
             "2023_06_28__BackgroundFrequencySweep\\Data")
plots_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Processing Data\\"
              "2023_06_28__BackgroundFrequencySweep\\Plots")

make_folder(plots_path)

for folder_name in os.listdir(data_path):
    folder_path = os.path.join(data_path, folder_name)
    for file_name in os.listdir(folder_path):
        # Extracting the sweep data into a dictionary
        path = os.path.join(folder_path, file_name)
        data_dict = read_from_path(path)

        # Data to plot
        frequency = data_dict["frequency"]
        capacitance = data_dict["absz"]
        resistance = data_dict["phasez"]

        # Creating lines objects
        lines_1 = plotting.lines(plotting.line(frequency[3:], capacitance[3:]),
                                 y_label="Abs z")
        lines_2 = plotting.lines(plotting.line(frequency[3:], resistance[3:]),
                                 y_label="Phase z")
        lines_objects = [lines_1, lines_2]

        # Creating plot and saving
        title = os.path.splitext(file_name)[0]
        plotting.create_figures(lines_objects, path=plots_path, output="Save",
                                title=title, format="png", axis_fontsize=14, suptitle_fontsize=18)
