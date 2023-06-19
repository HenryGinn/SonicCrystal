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
import sys
sys.path.append("D:\\Documents\\Python Scripts\\Scripts Henry")

from ...hgutilities.plotting import plotting
import numpy as np

from tools import read_from_path

# Where the sweep data is saved and where the plotting folder will be saved
base_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\CapacitativeDirectMeasurement"

capacitances = []
resistances = []
for file_name in os.listdir(base_path)[20:25]:
    if file_name not in ["Parameters.txt", "Plots"]:
        # Extracting the sweep data into a dictionary
        path = os.path.join(base_path, file_name)
        data_dict = read_from_path(path)

        # Data to plot
        frequency = data_dict["frequency"]
        capacitance = data_dict["param1"]
        resistance = data_dict["param0"]

        capacitances.append(capacitance)
        resistances.append(resistance)

capacitances = np.array(capacitances)
resistances = np.array(resistances)

# Creating lines objects
lines_1 = plotting.lines(plotting.line(frequency, capacitances),
                         y_label="Capacitance (F)")
lines_2 = plotting.lines(plotting.line(frequency[3:], resistances[:, 3:]),
                         y_label="Resistance $(\Omega)$")
lines_objects = [lines_1, lines_2]

# Creating plot and saving
title = "Fridge Circulation"
results_path = os.path.join(base_path, "Plots")
plotting.create_animations(lines_objects, path=results_path, maximise=False, figure_size=(15, 10),
                           title=title, axis_fontsize=14, suptitle_fontsize=18, loop=False)
