# SonicCrystal
A set of programs used to interact with the MFIA in the sonic crystal experiment.

1. [Conventions and Notes](#conventions-and-notes)
1. [Template Scripts](#template-scripts)
    1. [TemplateMeasurementScript](#templatemeasurementscript)
    1. [TemplateMeasurementScriptMultipleSettings](#templatemeasurementscriptmultiplesettings)
    1. [TemplateSimplePlotter](#templatesimpleplotter)
    1. [TemplateImpedancePlotter](#templateimpedanceplotter)
    1. [TemplateDemodPlotter](#templatedemodplotter)
    1. [TemplateImpedanceColourPlotter](#templateimpedancecolourplotter)
    1. [TemplateDemodColourPlotter](#templatedemodcolourplotter)
    1. [Time Estimator](#time-estimator)
1. [Data Processing Scripts](#data-processing-scripts)
    1. [HDF5Converter](#hdf5converter)
    1. [HDF5ConverterWithTemperature](#hdf5converterwithtemperature)
    1. [TemplateFileSplitter](#templatefilesplitter)
    1. [TemplateFileFilterer](#templatefilefilterer)
1. [Tools](#tools)
    1. [Quick Plot](#quick-plot)
    1. [File Naming System](#file-naming-system)
    1. [Reading and Writing to Files](#reading-and-writing-to-files)
    1. [Peak Finder](#peak-finder)
    1. [Run Experiment](#run-experiment)

## Conventions and Notes

- If something is intended to be read by humans (e.g. in a plot title or a file name) then it should be labelled as a number and not an index, and it should also start from one. They might still be used as indices under the hood, but the output to the user takes priority so they are to be treated as number labels. This applies to sweep numbers, demod numbers, and trial numbers. Warning: in the LabOne API the demods are labelled by their index. 
- Sweep numbers should be used when a larger sweep is split into multiple sweeps. If a new sweep is done with different settings or as part of another trial, the sweep number should start from 1 again. Sweep numbers should not be used to determine which setting is to be used for a particular sweep, for example by having a list of voltages, iterating an index variable up to the sweep number, and then using the index variable to determine the voltage (voltage = voltages[sweep_number - 1]). A separate loop should be used for this.
- All scripts should have the date in yyyy_mm_dd__Description format so that it is clear what experiment it is used for. This should be kept consistent with the experiment documentation.
- Every experiment should be done in a new script, even if it is an exact copy of a previous script. This is to help keep track of what we have done. It also applies to plotting scripts. This is because not all changes will be anticipated, and any changes should only affect a single experiment. If an old experiment is to be redone then the scripts used for it should reproduce the same experiment.
- Code intended for plotting and measuring should be in separate scripts. This is for two reasons: firstly, the two scripts can be run simultaneously without interferring with the other (as long as they use different shells), and secondly it keeps the measurement code simple, and reduces possibilities of it crashing. If the data needs to be viewed, the plotting code should be run from a separate shell and read the files that the measurement script has already produced.

Warning: when measurement code is being ran, be careful what shell you are running scripts from. If you are unsure, close the script you wanted to run, open a new IDLE shell, and open the script from that new shell. If you are still unsure, do not run the script. Always check that any previously running measurement scripts  still running afterwards.


## Template Scripts

These scripts are a good starting point for most purposes. The following documentation can also be found in each of the scripts themselves. We note that the demodulator data has a different structure than the impedance data so we have separate scripts for each of them.

All scripts start with the following declaration as in line with the conventions: "This script is meant to be copy and pasted into a new script for each new experiment. Do not tailor this script for a specific experiment. If you want a template that fits the new experiment, make a new template."

1. [TemplateMeasurementScript](#templatemeasurementscript)
1. [TemplateMeasurementScriptMultipleSettings](#templatemeasurementscriptmultiplesettings)
1. [TemplateSimplePlotter](#templatesimpleplotter)
1. [TemplateImpedancePlotter](#templateimpedanceplotter)
1. [TemplateDemodPlotter](#templatedemodplotter)
1. [TemplateImpedanceColourPlotter](#templateimpedancecolourplotter)
1. [TemplateDemodColourPlotter](#templatedemodcolourplotter)
1. [Time Estimator](#time-estimator)

### TemplateMeasurementScript

This script is for taking a single sweep over a frequency range. It has been designed to be easily adjustable and taking high resolution/long sweeps. It extracts impedance and demodulator data, but this can be changed as needed. Other measurement scripts should use this as a base.

A very small sweep will be done first with the same settings, and all the data from this will be saved into a file called "Metadata.txt". For the main sweep, only a selection of parameters will be saved.

### TemplateMeasurementScriptMultipleSettings

This script is based off TemplateMeasurementScript and is very similar. It does the same thing but it has been prepared to iterate through several settings. Due to the large variability in its intended use, more of the structure has deliberately been omitted.

### TemplateSimplePlotter

This is a general script that is intended to be fast and can probably be made to do what you want if it is sufficiently simple. Give it a path
or list of paths and it will attempt to plot it somewhat sensibly. If this doesn't work then do not try and poke around until it does, it is recommended that you start from scratch and do not use this.

For more information see the Quick Plot subsection of Tools in the README.

### TemplateImpedancePlotter

The purpose of this script is to take the impedance data and create a figure where a single parameter is shown against frequency. If the data has been
split over multiple files (for very large sweeps for example), that data is combined and shown on one plot.

### TemplateDemodPlotter

The purpose of this script is to take the demodulator data and create a figure where all the demods are on the same plot, and a single parameter is shown against frequency. If the data for each demod has been split over multiple files (for example with large sweeps), that data is combined and shown on one plot.

### TemplateImpedanceColourPlotter

The purpose of this script is to take the impedance data and create a figure where a single parameter is shown against frequency. If the data has been split over multiple files, that data is combined and shown on one plot.

This script is based on TemplateImpedancePlotter

### TemplateDemodColourPlotter

The purpose of this script is to take the demodulator data and create a figure where all the demods are on the same plot, and a single parameter is shown against frequency. If the data for each demod has been split over multiple files, that data is combined and shown on one plot.

This script is based on TemplateDemodPlotter

### Time Estimator

This is a feature build into the template measurement scripts and it gives the user an idea of when the experiment will finish. It bases this on the number of points and the maximum bandwidth. It has a 1% accuracy for sensible values of these settings, although for bandwidths smaller than 1 and numbers of points larger than 50,000 the accuracy cannot be guaranteed as it was not tested beyond these points. The original data and the regression calculations can be found in the following desmos: https://www.desmos.com/calculator/uzgv34ueme. The time taken depends on whether the demodulator data is being recorded as well and the data assumes that it is. The difference is not significant, but for experiments over a weekend the estimation may be off by a few hours (do not trust this assessment, this has not been explored much).


## Data Processing Scripts

These scripts are not used for gathering or plotting data. Their purpose is to manipulate the data into more useful forms.

1. [HDF5Converter](#hdf5converter)
1. [HDF5ConverterWithTemperature](#hdf5converterwithtemperature)
1. [TemplateFileSplitter](#templatefilesplitter)
1. [TemplateFileFilterer](#templatefilefilterer)

### HDF5Converter

A HDF5 file (extension name is .h5) stores data in a tree like structure. They can be opened with Visual Studio Code using an extension, but you cannot copy and paste the data.

This program reads the contents of the HDF5 file and puts it into folders with the same structure. The arrays are put into text documents. If the arrays are two dimensional then there the dimensions will span the columns. If instead there are multiple one dimensional arrays within a group then they will be put into one file where each array is one column.

### HDF5ConverterWithTemperature

A HDF5 file (extension name is .h5) stores data in a tree like structure. They can be opened with Visual Studio Code using an extension, but you cannot copy and paste the data.

This program reads the contents of the HDF5 file and puts it into folders with the same structure. The arrays are put into text documents. If the arrays are two dimensional then there the dimensions will span the columns. If instead there are multiple one dimensional arrays within a group then they will be put into one file where each array is one column.

This program is based off HDF5Converter. A file with the temperature log that contains the time period where the measurements were taken is provided. When the arrays are one dimensional a column for the temperature is added. These values are interpolated, and as the temperature is only taken every five seconds there can be long sequences of equal temperatures.

### TemplateFileSplitter

If the data from an experiment has been put into very large files, it may be desired that they are split up into smaller ones. This program does that. Its main purpose is for data attained from the plotter section of LabOne.

### TemplateFileFilterer

This takes data from a collection of files and reduces the resolution. The output is put into a single file, and the filtering works by taking an average of values within a window (not a moving window). Currently the average used is the mean.

## Tools

These are a collection of programs used to simplify and standardise the collection and plotting of data. The files for these scripts should be copied and pasted into the script folder for each experiment and then the functions imported into the script they are needed in individually (for example, `from filesnames import get_file_name`). The "Default Values" folder also needs to be copied into the same folder as the script for a tool.

1. [Quick Plot](#quick-plot)
1. [File Naming System](#file-naming-system)
1. [Reading and Writing to Files](#reading-and-writing-to-files)
1. [Peak Finder](#peak-finder)
1. [Run Experiment](#run-experiment)

## Quick Plot

This is from the hgutilities module, not the tools folder. It is designed to take in a path and produce a plot that matches the file and folder structure of the given path. It gives very little control over aesthetic details and the aim is to get an idea of what the data looks like very fast. The main control is given by the form of the input of the data to plot, detailed below. If you want a specific output such as comparing two different plots, then this tool will likely not suit your needs. The format of the files with the data are expected to have a single line header with the names of the variables and these will be used as the axis labels. The columns are assumed to be separated by tabs, but this is controllable with the `separator` keyword. The independent and dependent variables are assumed to be the 0'th and 1st columns, but these can be changed with the `x` and `y` keyword arguments by passing in the 0 based index of the column number. Use of the `subplots` keyword argument can also be helpful for controlling the number of subplots on each figure.

- Path to file. A single plot with a single line on it.
- Path to folder with `one_line_per_plot=True`. Each file within the folder will be plotted on it's own subplot.
- Path to folder with `one_line_per_plot=False`. All files within the folder will be plotted on one subplot.
- List of paths to files with `one_line_per_plot=True`. Each file plotting on it's own subplot.
- List of paths to files with `one_line_per_plot=False`. All files plotting on one subplot.
- Two dimensional list of paths to files. Each outer list corresponds to one subplot.
- List of paths to folders. The contents of each folder will be plotted on one subplot each.

If a dictionary is given in place of a list/tuple/array then the values will be used and not the keys. A blacklist of strings can be passed in and any file name containing any of these strings will not be included in the plots. This is controlled using the `blacklist` keyword argument.

Any keyword arguments will be fed into the figures object, figure object, line object, and lines object classes of hgutilities so much of that functionality remains, although the values for those keyword arguments will be set for every instance of each object. If finer control is required, this feature should not be used. This means properties such as axis details, font details, legend presence and position, figure size, etc can still be modified.

For more information go to https://github.com/HenryGinn/hgutilities/tree/main/hgutilities/plotting, although if you need to do this then you probably should not be using this.

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

### Design

The aim of this is to have a consistent, predictible, and easy to work with system for naming files. The goal is for file names to be easy to create, versitile enough to store the range of metadata we want to include in the file names, and be convenient to read with a program.

- Treating keywords and values as pairs. Previously all words and values were separated by underscores which meant that extracting keyword-value pairs was awkward. We change this so that keyword-value pairs are separated by a double underscore so that we can use `file_name.split("__")` to separate out the pairs.
- Organisation within a keyword-value pair. If we have "keyword_value" then we can extract these with `keyword, value = "keyword_value".split("_")`. If the keyword is something like "probe_power", this will break however and determining what part is the keyword and what part is the value becomes messy. We fix this by converting all keywords into PascalCase to remove the underscores. There is an additional complication with units, as if units are included then we have 3 parts instead of 2. As the units are not going to matter to the program, we can ignore them by slicing the list as follows: `keyword, value = "keyword_value".split("_")[:2]`. We note that we still may want to have the units in the file name as it provides useful information to the user.
- Files appearing out of order. There are three ways in which files can not be a sensible order. The first of these is due to numbers with different lengths of digits being treated as strings and sorted lexicographically (for example "1", "10", "2"). This can be fixed by adding leading zeros. The second is where you have names such as "1", "-1", "2", "-2" which are in lexicographic order. "+1", "+2", "-1", "-2" is an improvement but still not what we want. The third is where the keyword-value pairs are included in a less than sensible order, for example anything where the values can be negative. We solve all these issues by using the timestamp at the moment of file creation as the first keyword-value pair. This is guaranteed to be unique, non-negative, increasing, and the same length (at least until around the year 2289). The files should be saved in the order they are intended to appear.

### Decisions About Standards

- Keyword order. Apart from including the timestamp at the start, we decide not to sort the keywords as the only advantage is that the file name is slightly more predictible. When we have control over the order however, we can put more important information nearer the start. This is convenient because it means we do not need to expand the file name tab to see information we commonly want to see. For example, it is a common situation to be in a folder where all the values of a particular keyword are the same, so this keyword-value pair can be hidden from view. We also note that it will be very easy and computationally cheap to extract all the keyword-value pairs into a dictionary and the required keyword can be looked up. This means we do not need the keywords to be in any particular order. It may still be 
- As noted before, having key information near the start of the file name is useful. For this reason, we decide to shorten "Timestamp" to "T".

## Reading and Writing to Files

To write data to a file, pass in the path where it is going to be saved, and a dictionary with the data. The column headers are the keys, the data in each column are the corresponding values. Entries will be separated with tabs and this function takes no optional keywords. If the path to the folders does not exist then it will be created.

```
from data import save_to_path
output_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\output.txt"
save_to_path(output_path, data_dict)
```

To read data from a file, a path is given and a dictionary is returned (this dictionary has the same format as the input to the save_to_path function).

Optional keywords:
- separator: this is what is used to separate the columns. Default is "\t" (tab).
- skip_first_n: if the first several lines have comments that are not part of the data, these can be skipped. Default is 0.

```
from data import read_from_path
input_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\meas_sweep_20230607_110205.txt"
data_dict = read_from_path(input_path, separater=", ", skip_first_n=4)
```

## Peak Finder

This will run a sweep over a wide region, identify where the peak is, and then run a sweep over a small region around the peak to get a more precise measurement. This process is repeated until the desired resolution is reached, or the maximum number of iterations is reached. If the keyword argument `plot_results=True` is given then all of the attempts are plotted. If the keyword argument `save_data=True` is passed in then the data will be saved in a folder called "FindingPeak". The location of this folder is set to be the Raw Data folder in SonicCrystal3, but this should be changed by passing in a value to the `base_path` keyword argument.

## Run Experiment

This tool is made so that the user can more easily prescribe what they want to happen during the experiment. The user can prescribe several layers of variables that need to be iterated through (like in a series of nested for loops), and this will be handled for them. This tool should only be used for very low effort experiments and if the structure is any more complicated than the example below then it should be scripted manually. An example of this would be looking at pairs of settings that take values (a_0, b_0), (a_1, b_1), and (a_2, b_2). The user specifies a folder structure and starts the experiment like so:

```
from runexperiment import run_experiment

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

It will run a script which contains the details of what is meant to happen (this would be the code inside all the nested for loops). The variables that have been iterated through are set as global variables. The name of this script should be passed in as a value of the keyword argument, `experiment_script_name`, and its default value is "experiment.py". Here is some example code within this script along with it's output.
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

The path to the folder that has been created will also be set as a global variable and is called "base_path". At the root of this folder tree is a folder with the date when the script is run in the format yyyy_mm_dd. This folder is by default saved to "Experiments Data\\SonicCrystal3\\Raw Data". This can be changed by passing a path into the `run_experiment` function with the `base_path` keyword argument.