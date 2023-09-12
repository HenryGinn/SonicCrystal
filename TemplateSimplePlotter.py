"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

This is a general script that is intended to be fast and can probably
be made to do what you want if it is sufficiently simple. Give it a path
or list of paths and it will attempt to plot it somewhat sensibly.
If this doesn't work then do not try and poke around until it does,
it is recommended that you start from scratch and do not use this.

For more information see the Quick Plot subsection of Tools in the README.
"""

import hgutilities.plotting as plotting

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day =
description =

# Impedance parameters
# 0: frequency,
# 1: absz, 2: abszstddev
# 3: realz, 4: imagz,
# 5: realzstddev, 6: imagzstd
# 7: param0, 8: param0stddev
# 9: param1, 10: param1stddev
# 11: phasez, 12: phasezstddev
# 13: nexttimestamp

# Demod parameters
# 0: frequency,
# 1: r, 2: phase, 3: x, 4: y,
# 5: rstddev, 6: phasestddev,
# 7: xstddev, 8: ystddev,
# 9: nexttimestamp

column_index = 1

base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal3\\Processed Data"
             f"\\{year}_{month}_{day}__{description}\\Data\\")

# If all the lines are desired to be the same colour, add
# a value for the "color" keyword argument in this line.
# The boolean keyword argument "one_line_per_plot" can be
# used to change the behaviour of the output.
# A list of strings can be passed in to the keyword argument
# "blacklist", and any file that contains any of those strings
# will not be plotted.

# For more documentation see the link below:
# https://github.com/HenryGinn/hgutilities/tree/main/hgutilities/plotting#quick-plot
plotting.quick(base_path, subplots=1, y=column_index)

