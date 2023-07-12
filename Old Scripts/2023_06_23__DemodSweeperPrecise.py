import time
import os
import datetime
import math

import zhinst.core
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
import numpy as np

from tools import *

# Setting up the MFIA
daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6) # Connect API to device
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs

# Setting up the sweeper
sweeper = daq.sweep()
sweeper.set('device', 'dev6641') # The MFIA device
sweeper.set('xmapping', 0) # x axis mode: 0: linear, 1: log

# Enabling demodulators (0 based)
daq.setInt('/dev6641/demods/1/enable', 1) # Demod 2
daq.setInt('/dev6641/demods/2/enable', 1) # Demod 3
daq.setInt('/dev6641/demods/3/enable', 1) # Demod 4

# Set demodulator harmonics (0 based)
daq.setInt('/dev6641/demods/1/harmonic', 2)
daq.setInt('/dev6641/demods/2/harmonic', 3)
daq.setInt('/dev6641/demods/3/harmonic', 4)

# Set voltage
daq.setInt('/dev6641/system/impedance/filter', 1)
daq.setDouble('/dev6641/imps/0/output/range', 10) # Set voltage range
daq.setInt('/dev6641/imps/0/auto/output', 0) # Set manual mode

# Start and stop frequency
sweeper.set('start', 1e3)
sweeper.set('stop', 5e6)
sweeper.set('samplecount', 16991) # The number of points in a sweep

# Bandwidth
daq.setDouble('/dev6641/imps/0/maxbandwidth', 1)
sweeper.set('bandwidth', 1)
sweeper.set('maxbandwidth', 1)
sweeper.set('bandwidthoverlap', 1)

# Other (values taken from the API log)
sweeper.set('averaging/sample', 10) # Number of samples per point to average
sweeper.set('settling/inaccuracy', 0.01)
sweeper.set('averaging/tc', 15)
sweeper.set('averaging/time', 0.1)
sweeper.set('omegasuppression', 80)
sweeper.set('order', 8)
sweeper.set('gridnode', '/dev6641/oscs/0/freq')

# Making the folders where the settings will be saved
base_paths = ["D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-23__Demod\\Demod_0",
              "D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-23__Demod\\Demod_1",
              "D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-23__Demod\\Demod_2",
              "D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-23__Demod\\Demod_3"]
for path in base_paths:
    make_folder(path)

# The settings to be iterated through
voltages_and_biases = [(1, 0), (2, 0), (3, 0), (3, 1), (4, 0)]

# The program will run until the shell window is closed, the device turns off
# (causing it to crash), the computer is turned off, or the shell is restarted
# (by pressing ctrl + f6)
sweep_number = 0
while True:
    # Progress indicator
    sweep_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Sweep number: {sweep_number:03d}, {sweep_time}")

    # Subscribing to all the demodulators
    sweeper.subscribe('/dev6641/demods/0/sample')
    sweeper.subscribe('/dev6641/demods/1/sample')
    sweeper.subscribe('/dev6641/demods/2/sample')
    sweeper.subscribe('/dev6641/demods/3/sample')
    
    # Set voltages and biases
    drive_voltage, bias_voltage = voltages_and_biases[sweep_number % len(voltages_and_biases)]
    daq.setDouble('/dev6641/imps/0/output/amplitude', drive_voltage) # Set voltage value
    daq.setDouble('/dev6641/imps/0/bias/value', bias_voltage) # Set bias voltage

    # Running a sweep
    sweeper.execute()
    while not sweeper.finished():
        time.sleep(0.1)
    time.sleep(0.1)
    sweeper.finish()
    sweeper.unsubscribe('*')

    # Extracting the results from the sweeper
    sweeper_results = sweeper.read()
    sweeper_results = sweeper_results["dev6641"]["demods"]
    sweeper_results = [sweeper_results[str(demod_number)]["sample"][0][0]
                       for demod_number in range(4)]

    # Processing which data will be recorded
    params = ["frequency", "r", "phase", "x", "y",
              "rstddev", "phasestddev", "xstddev", "ystddev", "nexttimestamp"]
    results = [{key: demod_results[key] for key in params}
               for demod_results in sweeper_results]
    parameters = [{key: demod_results[key] for key in list(demod_results.keys())
                   if key not in params}
                  for demod_results in sweeper_results]

    # Saving the parameters to files
    if sweep_number == 0:
        for demod_index, parameter_results in enumerate(parameters):
            path = os.path.join(base_paths[demod_index], f"Parameters_0__Demod_{demod_index}.txt")
            with open(path, "w") as file:
                for key, value in parameter_results.items():
                    file.writelines(f"{key}\t{value}\n")

    # Saving the results to files
    trial_number = math.floor(sweep_number / len(voltages_and_biases))
    for demod_index, demod_results in enumerate(results):
        file_name = get_file_name({"sweep number": sweep_number,
                                   "drive voltage": drive_voltage,
                                   "bias voltage": bias_voltage,
                                   "trial number": trial_number + 1,
                                   "demod": demod_index},
                                  timestamp=False)
        path = os.path.join(base_paths[demod_index], file_name)
        save_to_path(path, demod_results)
        
    sweep_number += 1
