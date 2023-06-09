# CryostatInterface
A set of programs used to interact with the devices that work with the cryostat

1. [File Naming System](#file-naming-system)
1. [Reading and Writing to Files](#reading-and-writing-to-files)
1. [Peak Finder](#peak-finder)
1. [Folder Structure](#folder-structure)

## File Naming System

1. [Usage](#usage)
1. [Design](#design)
1. [Decisions About Standards](#decisions-about-standards)

### Usage

The information about the file name is described with a dictionary. The name of the piece of information to be stored is given as the key, and the value of that information is given as the value. If the unit of the value is to be stored in the file name, the value will be given as a dictionary instead like in the example below. When extracting data from file names, units are ignored and the values are assumed to be numbers and so are converted to floats.

    # Creating a file name
    from filenames import get_file_name

    input_dict = {"probe power": {"value": 26, "unit": "dBm"},
                  "cavity frequency": 39884000,
                  "detuning": 3000000}
    file_name = get_file_name(input_dict)
    
    # Extracting data from a file name
    from filenames import read_file_name
    file_name_data = read_file_name(file_name)

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

    from data import read_from_path
    input_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\meas_sweep_20230607_110205.txt"
    data_dict = read_from_path(input_path, separater=", ", skip_first_n=4)

To read data from a file, a path is given and a dictionary is returned (this dictionary has the same format as the input to the write-to-file function).

Optional keywords:
separator: this is what is used to separate the columns. Default is "\t" (tab).
skip_first_n: if the first several lines have comments that are not part of the data, these can be skipped. Default is 0.

    from data import save_to_path
    output_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\output.txt"
    save_to_path(output_path, data_dict)

## Peak Finder

This will run a sweep over a wide region, identify where the peak is, and then run a sweep over a small region around the peak to get a more precise measurement. This process is repeated until the desired resolution is reached, or the maximum number of iterations is reached. If the keyword argument `plot_results=True` is given then all of the attempts are plotted.

TODO: add functionality to save data.

## Folder Structure

The user will specify a folder structure like so:

    folder_structure = {"power": [24, 25],
                        "trial": [1, 2, 3],
                        "detuning": [0, 1, 2]}

This means they want to iterate through the powers 24 and 25, and then at the next level down iterate through the trials, and so on, where each new level is in it's own folder. The will 