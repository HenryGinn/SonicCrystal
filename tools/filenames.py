import time
import os
from hgutilities import defaults

class FileName():

    def __init__(self, input_dict, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_input_dict(input_dict)
        self.set_file_name()

    def set_input_dict(self, input_dict):
        self.input_dict = {self.ensure_pascal_case(key): self.convert_to_dict(value)
                      for key, value in input_dict.items()}

    def ensure_pascal_case(self, key):
        words = [word for word_unsplit in key.split(" ")
                 for word in word_unsplit.split("_")]
        pascal_case = [f"{word[0].upper()}{word[1:].lower()}"
                       for word in words]
        key = "".join(pascal_case)
        return key

    def convert_to_dict(self, value):
        if not isinstance(value, dict):
            value = {"value": value}
        return value

    def set_file_name(self):
        component_names = [self.get_component_name(key, value_dict)
                           for key, value_dict in self.input_dict.items()]
        self.add_timestamp(component_names)
        self.file_name = f"{'__'.join(component_names)}.txt"

    def get_component_name(self, key, value_dict):
        if "unit" in value_dict:
            return self.component_name_with_units(key, value_dict)
        else:
            return self.component_name_without_units(key, value_dict)

    def component_name_with_units(self, key, value_dict):
        value = value_dict["value"]
        unit = value_dict["unit"]
        component_name = f"{key}_{value}_{unit}"
        return component_name

    def component_name_without_units(self, key, value_dict):
        value = value_dict["value"]
        component_name = f"{key}_{value}"
        return component_name

    def add_timestamp(self, component_names):
        if self.timestamp:
            timestamp = time.time()
            timestamp_string = f"T_{timestamp}"
            component_names.insert(0, timestamp_string)

defaults.load(FileName)

def get_file_name(input_dict, **kwargs):
    file_name_obj = FileName(input_dict, **kwargs)
    return file_name_obj.file_name

def read_file_name(file_name):
    data = dict(item.split("_")[:2] for item in os.path.splitext(file_name)[0].split("__"))
    return {key: float(value) for key, value in data.items()}
