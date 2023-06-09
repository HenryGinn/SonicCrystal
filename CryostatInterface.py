"""
import zhinst.core
import time

#results_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results"

daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
daq.setDouble('/dev6641/imps/0/freq', 10000)

sweeper = daq.sweep()
sweeper.set('device', 'dev6641')
sweeper.subscribe('/dev6641/imps/0/sample')
sweeper.execute()
sweeper.unsubscribe("*")
#sweeper.set('save/directory', results_path)
#sweeper.set("save/saveonread", True)
sweeper.save()
a = sweeper.read()
print(a)

"""


from tools.getpeak import get_peak
peak = get_peak(plot_results=True)


"""
from filenames import get_file_name
from filenames import read_file_name

input_dict = {"probe power": {"value": 26, "unit": "dBm"},
              "cavity frequency": 39884000,
              "detuning": 3000000}
file_name = get_file_name(input_dict)
file_name_data = read_file_name(file_name)
print(file_name)
print(file_name_data)
"""

"""
input_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\meas_sweep_20230607_110205.txt"
data_dict = read_from_path(input_path, separater=", ", skip_first_n=4)

output_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results\\output.txt"
save_to_path(output_path, data_dict)
"""

"""
from tools.runexperiment import run_experiment

folder_structure = {"power": [24, 25],
                    "trial": [1, 2, 3],
                    "detuning": [0, 1, 2]}

run_experiment(folder_structure)
"""
