"""
This program takes data from the "Circulator" script (sweeps the device)
and plots the results.

These are the quantities saved from the sweeps and what they correspond to.

param0: capacitance
param1: resistance
absz
realz
imagz
phasez

All of the above also have their standard deviations saved.
To access these, add "stddev" on the end, e.g. "param0stddev".
"frequency" and "nexttimestamp" are also recorded.

To change the data being plotted, follow the example below:

    # The y values
    capacitance = data_dict["param1"]

    # Creating a line object
    # This contains data about the data series, not the plot
    line_obj = plotting.line(frequency, capacitance)

    # Creating a lines object
    # This contains data about the plot, not the data series
    lines_obj = plotting.lines(line_obj, y_label="My y label", title="My title")

The plotting function takes in a list of lines objects,
so remember to add your lines_obj to the list.

Most matplotlib parameters can be changed by passing a keyword argument
into the relevant object (follow common sense or check docs) with the
same keyword name as when usually working with matplotlib subplots.

For more help, run "help(plotting)" or check the README:
https://github.com/HenryGinn/hgutilities/tree/main/hgutilities/plotting
"""

import os
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
from tools import read_from_path

data_path = "/home/henry/Documents/Other Programming/Physics Internship/SonicCrystal/DataSets/2023-06-16"
plots_path = "/home/henry/Documents/Other Programming/Physics Internship/SonicCrystal/Plots/2023-06-16"

make_folder(plots_path)

for file_name in os.listdir(data_path)[20:22]:
    if file_name not in ["Parameters.txt", "Plots"]:
        # Extracting the sweep data into a dictionary
        path = os.path.join(data_path, file_name)
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
