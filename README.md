# CryostatInterface
A set of programs used to interact with the devices that work with the cryostat

## File Naming System

The aim of this is to have a consistent, predictible, and easy to work with system for naming files. The goal is for file names to be easy to create, versitile enough to store the range of metadata we want to include in the file names, and be convenient to read with a program.

- Treating keywords and values as pairs. Previously all words and values were separated by underscores which meant that extracting keyword-value pairs was awkward. We change this so that keyword-value pairs are separated by a double underscore so that we can use `file_name.split("__")` to separate out the pairs.
- Organisation within a keyword-value pair. If we have "keyword_value" then we can extract these with `keyword, value = "keyword_value".split("_")`. If the keyword is something like "probe_power", this will break however and determining what part is the keyword and what part is the value becomes messy. We fix this by converting all keywords into PascalCase to remove the underscores. There is an additional complication with units, as if units are included then we have 3 parts instead of 2. As the units are not going to matter to the program, we can ignore them by slicing the list as follows: `keyword, value = "keyword_value".split("_")[:2]`. We note that we still may want to have the units in the file name as it provides useful information to the user.
- Files appearing out of order. There are three ways in which files can not be a sensible order. The first of these is due to numbers with different lengths of digits being treated as strings and sorted lexicographically (for example "1", "10", "2"). This can be fixed by adding leading zeros. The second is where you have names such as "1", "-1", "2", "-2" which are in lexicographic order. "+1", "+2", "-1", "-2" is an improvement but still not what we want. The third is where the keyword-value pairs are included in a less than sensible order, for example anything where the values can be negative. We solve all these issues by using the timestamp at the moment of file creation as the first keyword-value pair. This is guaranteed to be unique, non-negative, increasing, and the same length (at least until around the year 2289). The files should be saved in the order they are intended to appear.

Decisions about standards

- Keyword order. Apart from including the timestamp at the start, we decide not to sort the keywords as the only advantage is that the file name is slightly more predictible. When we have control over the order however, we can put more important information nearer the start. This is convenient because it means we do not need to expand the file name tab to see information we commonly want to see. For example, it is a common situation to be in a folder where all the values of a particular keyword are the same, so these keyword-value pair can be hidden from view. We also note that it will be very easy and computationally cheap to extract all the keyword-value pairs into a dictionary and the required keyword can be looked up. This means we do not need the keywords to be in any particular order.
- As noted before, having key information near the start of the file name is useful. For this reason, we decide to shorten "TimeStamp" to "T".

## Folder Structure

