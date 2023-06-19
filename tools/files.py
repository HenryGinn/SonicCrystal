import numpy as np

def save_to_path(path, data):
    with open(path, "w") as file:
        write_header_to_file(file, data)
        write_columns_to_file(file, data)

def write_header_to_file(file, data):
    header_string = '\t'.join([str(key) for key in data.keys()])
    file.writelines(header_string + "\n")

def write_columns_to_file(file, data):
    rows = zip(*list(data.values()))
    for row in rows:
        file.writelines("\t".join([str(value) for value in row]) + "\n")

def read_from_path(path, separater="\t", skip_first_n=0):
    with open(path, "r") as file:
        skip_first_lines(file, skip_first_n)
        keys = file.readline().strip("% \n").split(separater)
        values = get_data_from_file(file, separater)
        return dict(zip(keys, values))

def skip_first_lines(file, skip_first_n):
    for line_number in range(skip_first_n):
        file.readline()

def get_data_from_file(file, separater):
    rows = [[float(number)
             for number in line.strip().split(separater)]
            for line in file]
    columns = [np.array(column) for column in zip(*rows)]
    return columns
