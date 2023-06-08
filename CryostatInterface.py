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
from getpeak import get_peak
#peak = get_peak(plot_results=True)

from filenames import get_file_name
from filenames import read_file_name

input_dict = {"probe power": {"value": 26, "unit": "dBm"},
              "cavity frequency": 39884000,
              "detuning": 3000000}
print("Input to file name creator:")
print(input_dict)
print("")
file_name = get_file_name(input_dict)
print(f"File name:\n{file_name}\n")

print(f"Extracting from file name:\n{read_file_name(file_name)}")
