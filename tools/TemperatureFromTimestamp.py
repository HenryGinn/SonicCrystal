import numpy as np
from hgutilities.utils import read_from_path

def get_temperature_dict(path):
    temperature_data = read_from_path(path)
    keys = list(temperature_data.keys())
    temperature_dict = {"Timestamp": temperature_data[keys[0]] - 2082844800,
                        "Temperature": temperature_data[keys[0]]}
    return temperature_dict

def get_temperatures(timestamps, temperature_dict):
    temperatures = np.interp(temperature_dict["Timestamp"],
                             timestamps,
                             temperature_dict["Temperature"])
    return temperatures
