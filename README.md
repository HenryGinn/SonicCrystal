# SonicCrystal
A set of programs used to interact with the MFIA in the sonic crystal experiment.

Documentation for each experiment can be found in a file called "Experiments Log" in the base folder where the experiment data is saved (SonicCrystal)

1. [Conventions and Notes](#conventions-and-notes)
1. [Tools](#tools)
    1. [Quick Plot](#quick-plot)
    1. [File Naming System](#file-naming-system)
    1. [Reading and Writing to Files](#reading-and-writing-to-files)
    1. [Peak Finder](#peak-finder)
    1. [Run Experiment](#run-experiment)
    1. [Run Experiment V2](#run-experiment-v2)
1. [Time Estimator](#time-estimator)

## Conventions and Notes

- Sweep numbers may be used to index into lists to define settings. For this reason they should be 0 indexed.
- Demod numbers should not be 0 indexed as they refer to one of the demodulators and are not indexes.
- Trial numbers should not be used as indexes for anything, except in post processing. Their main purpose is for human readability to distinguish between trials, so they should start from 1.
- All scripts should have the date in yyyy_mm_dd__Description format so that it is clear what experiment it is used for. This should be kept consistent with the experiment documentation.
- Every experiment should be done in a new script, even if it is an exact copy apart from a few parameters being changed. This is to help keep track of what we have done. It also applies to plotting scripts.
- Code intended for plotting and measuring should be in separate scripts. This is for two reasons: firstly, the two scripts can be run simultaneously without interferring with the other, and secondly, it keeps the measurement code simple, and reduces possibilities of it crashing. If the data needs to be viewed, the plotting code should be run from a separate shell and read the files that the measurement script has already produced.

Warning: when measurement code is being ran, be careful what shell you are running scripts from. If you are unsure, close the script you wanted to run, open a new IDLE shell, and open the script from that new shell. If you are still unsure, do not run the script. Check that the measurement script is still running afterwards.

## Tools

These are a collection of programs used to simplify and standardise the collection and plotting of data

1. [Quick Plot](#quick-plot)
1. [File Naming System](#file-naming-system)
1. [Reading and Writing to Files](#reading-and-writing-to-files)
1. [Peak Finder](#peak-finder)
1. [Run Experiment](#run-experiment)

## Quick Plot

This is from the hgutilities module, not the "tools" folder. It is designed to take in a path and produce a plot. It gives very little control and the aim is to get an idea of what the data looks like very fast. The format of the files with the data are expected to have a single line header with the names of the variables and these will be used as the axis labels. The columns are assumed to be separated by tabs, but this is controllable with the `separator` keyword. The independent and dependent variables are assumed to be the 0'th and 1st columns, but these can be changed with the `x` and `y` keyword arguments by passing in the 0 based index of the column number. The main control is given by the form of the input of the data to plot, detailed below. Use of the `subplots` keyword argument can also be helpful for controlling the number of subplots on each figure.

- Path to file. A single plot with a single line on it.
- Path to folder with `one_line_per_plot=True`. Each file within the folder will be plotted on it's own subplot.
- Path to folder with `one_line_per_plot=False`. All files within the folder will be plotted on one subplot.
- List of paths to files with `one_line_per_plot=True`. Each file plotting on it's own subplot.
- List of paths to files with `one_line_per_plot=False`. All files plotting on one subplot.
- Two dimensional list of paths to files. Each outer list corresponds to one subplot.
- List of paths to folders. The contents of each folder will be plotted on one subplot each.

If a dictionary is given in place of a list/tuple/array then the values will be used and not the keys.

Any keyword arguments will be fed into the figures object, figure object, line object, and lines object classes of hgutilities so much of that functionality remains, although the values for those keyword arguments will be set for every instance of each object. If finer control is required, this feature should not be used.

## File Naming System

1. [Usage](#usage)
1. [Design](#design)
1. [Decisions About Standards](#decisions-about-standards)

### Usage

The information about the file name is described with a dictionary. The name of the piece of information to be stored is given as the key, and the value of that information is given as the value. If the unit of the value is to be stored in the file name, the value will be given as a dictionary instead like in the example below. When extracting data from file names, units are ignored and the values are assumed to be numbers and so are converted to floats.

```
# Creating a file name
from filenames import get_file_name

input_dict = {"probe power": {"value": 26, "unit": "dBm"},
                "cavity frequency": 39884000,
                "detuning": 3000000}
file_name = get_file_name(input_dict)

# Extracting data from a file name
from filenames import read_file_name
file_name_data = read_file_name(file_name)
```

The file name produced is: "T_1686226733.9690254__ProbePower_26_dBm__CavityFrequency_39884000__Detuning_3000000.txt".

The data extracted is: {'T': 1686226733.9690254, 'ProbePower': 26, 'CavityFrequency': 39884000, 'Detuning': 3000000}

## Design

The aim of this is to have a consistent, predictible, and easy to work with system for naming files. The goal is for file names to be easy to create, versitile enough to store the range of metadata we want to include in the file names, and be convenient to read with a program.

- Treating keywords and values as pairs. Previously all words and values were separated by underscores which meant that extracting keyword-value pairs was awkward. We change this so that keyword-value pairs are separated by a double underscore so that we can use `file_name.split("__")` to separate out the pairs.
- Organisation within a keyword-value pair. If we have "keyword_value" then we can extract these with `keyword, value = "keyword_value".split("_")`. If the keyword is something like "probe_power", this will break however and determining what part is the keyword and what part is the value becomes messy. We fix this by converting all keywords into PascalCase to remove the underscores. There is an additional complication with units, as if units are included then we have 3 parts instead of 2. As the units are not going to matter to the program, we can ignore them by slicing the list as follows: `keyword, value = "keyword_value".split("_")[:2]`. We note that we still may want to have the units in the file name as it provides useful information to the user.
- Files appearing out of order. There are three ways in which files can not be a sensible order. The first of these is due to numbers with different lengths of digits being treated as strings and sorted lexicographically (for example "1", "10", "2"). This can be fixed by adding leading zeros. The second is where you have names such as "1", "-1", "2", "-2" which are in lexicographic order. "+1", "+2", "-1", "-2" is an improvement but still not what we want. The third is where the keyword-value pairs are included in a less than sensible order, for example anything where the values can be negative. We solve all these issues by using the timestamp at the moment of file creation as the first keyword-value pair. This is guaranteed to be unique, non-negative, increasing, and the same length (at least until around the year 2289). The files should be saved in the order they are intended to appear.

### Decisions About Standards

- Keyword order. Apart from including the timestamp at the start, we decide not to sort the keywords as the only advantage is that the file name is slightly more predictible. When we have control over the order however, we can put more important information nearer the start. This is convenient because it means we do not need to expand the file name tab to see information we commonly want to see. For example, it is a common situation to be in a folder where all the values of a particular keyword are the same, so these keyword-value pair can be hidden from view. We also note that it will be very easy and computationally cheap to extract all the keyword-value pairs into a dictionary and the required keyword can be looked up. This means we do not need the keywords to be in any particular order.
- As noted before, having key information near the start of the file name is useful. For this reason, we decide to shorten "Timestamp" to "T".

## Reading and Writing to Files

To write data to a file, pass in the path where it is going to be saved, and a dictionary with the data. The column headers are the keys, the data in each column are the corresponding values. Entries will be separated with tabs and this function takes no optional keywords.

```
from data import read_from_path
input_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\meas_sweep_20230607_110205.txt"
data_dict = read_from_path(input_path, separater=", ", skip_first_n=4)
```

To read data from a file, a path is given and a dictionary is returned (this dictionary has the same format as the input to the write-to-file function).

Optional keywords:
- separator: this is what is used to separate the columns. Default is "\t" (tab).
- skip_first_n: if the first several lines have comments that are not part of the data, these can be skipped. Default is 0.

```
from data import save_to_path
output_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\output.txt"
save_to_path(output_path, data_dict)
```

## Peak Finder

This will run a sweep over a wide region, identify where the peak is, and then run a sweep over a small region around the peak to get a more precise measurement. This process is repeated until the desired resolution is reached, or the maximum number of iterations is reached. If the keyword argument `plot_results=True` is given then all of the attempts are plotted. If the keyword argument `save_data=True` is passed in then the data will be saved in a folder called "FindingPeak". The location of this folder is set to be the capacitance experiment folder, but this should be changed by passing in a value to the `base_path` keyword argument.

## Run Experiment

This tool is made so that the user can more easily prescribe what they want to happen during the experiment. The user can prescribe several layers of variables that need to be iterated through (like in a series of nested for loops), and this will be handled for them. The user specifies a folder structure and starts the experiment like so:

```
from tools.runexperiment import run_experiment

folder_structure = {"power": [24, 25],
                    "trial": [1, 2],
                    "detuning": [0, 1]}

run_experiment(folder_structure)
```

This will generate the following folder structure:

```
├───power_24
│   ├───trial_1
│   │   ├───detuning_0
│   │   └───detuning_1
│   └───trial_2
│       ├───detuning_0
│       └───detuning_1
└───power_25
    ├───trial_1
    │   ├───detuning_0
    │   └───detuning_1
    └───trial_2
        ├───detuning_0
        └───detuning_1
```

It will also run a script which contains the details of what is meant to happen (this would be the code inside all the nested for loops). The variables that have been iterated through are set as global variables. Here is some example code along with it's output.
```
print(f"power: {power}, "
    f"trial: {trial}, "
    f"detuning: {detuning}")
```

```
power: 24, trial: 1, detuning: 0
power: 24, trial: 1, detuning: 1
power: 24, trial: 2, detuning: 0
power: 24, trial: 2, detuning: 1
power: 25, trial: 1, detuning: 0
power: 25, trial: 1, detuning: 1
power: 25, trial: 2, detuning: 0
power: 25, trial: 2, detuning: 1
```

The path to the folder that has been created will also be set as a global variable and is called "base_path". At the root of this folder tree is a folder with the date when the script is run in the format yyyy_mm_dd. This folder is within the "CapacitanceExperiment" folder inside "Experiments Data" folder. This can be changed by passing a path into the `run_experiment` function with the `base_path` keyword argument.