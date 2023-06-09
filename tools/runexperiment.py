import os
from datetime import datetime

from hgutilities import defaults
from hgutilities.utils.paths import make_folder

class RunExperiment():

    def __init__(self, folder_structure, **kwargs):
        defaults.kwargs(self, kwargs)
        self.folder_structure = folder_structure
        self.set_experiment_path()
        self.set_code()
        self.run_experiment()

    def set_code(self):
        with open("Experiment.py", "r") as file:
            self.code = "".join([line for line in file])

    def set_experiment_path(self):
        date = datetime.today().strftime('%Y_%m_%d')
        self.experiment_path = os.path.join(self.base_path, date)

    def run_experiment(self):
        variable_dict = {key: None for key in self.folder_structure.keys()}
        self.recurse_through_globals(0, variable_dict)

    def recurse_through_globals(self, depth, code_globals):
        if depth == len(self.folder_structure):
            self.run_code(code_globals)
        else:
            self.prepare_next_recursion(depth, code_globals)

    def run_code(self, code_globals):
        code_globals["base_path"] = self.get_path(code_globals)
        make_folder(code_globals["base_path"])
        exec(self.code, code_globals, {})

    def get_path(self, code_globals):
        path = os.path.join(self.experiment_path,
                            *[f"{key}_{value}"
                              for key, value in code_globals.items()
                              if key in self.folder_structure])
        return path
        

    def prepare_next_recursion(self, depth, code_globals):
        key = list(self.folder_structure.keys())[depth]
        for value in self.folder_structure[key]:
            code_globals[key] = value
            self.recurse_through_globals(depth + 1, code_globals)

defaults.load(RunExperiment)

def run_experiment(*args, **kwargs):
    run_experiment_obj = RunExperiment(*args, **kwargs)
