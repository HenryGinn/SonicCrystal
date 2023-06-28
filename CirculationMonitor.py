import time
import os
import datetime

import zhinst.core
from hgutilities import plotting
import numpy as np

from tools import *

# Setting up the device and sweeper
daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs
sweeper = daq.sweep()
sweeper.set('device', 'dev6641') # The MFIA device
sweeper.set('xmapping', 0) # x axis mode: 0: linear, 1: log

# Set voltage range
daq.setInt('/dev6641/system/impedance/filter', 1)
daq.setDouble('/dev6641/imps/0/output/range', 10) # Set range

# Set drive voltage
daq.setInt('/dev6641/imps/0/auto/output', 0) # Set manual mode
daq.setDouble('/dev6641/imps/0/output/amplitude', 1) # Set voltage value

# Start and stop frequency
sweeper.set('start', 1e3)
sweeper.set('stop', 5e6)
sweeper.set('samplecount', 2500) # The number of points in a sweep

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

# Preparing for sweeping
base_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\CapacitativeDirectMeasurement\\2023-06-16"
sweep_number = 0

voltages_and_biases = [(0.5, 0), (0.5, 0.5), (0.5, 1), (0.5, 1.5),
                       (1, 0), (1, 0.5), (1, 1),
                       (1.5, 0), (1.5, 0.5),
                       (2, 0)]

# The program will run until the shell window is closed, the device turns off
# (causing it to crash), the computer is turned off, or the shell is restarted
# (by pressing ctrl + f6)
while True:
    # Progress indicator
    sweep_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Sweep number: {sweep_number:04d}, {sweep_time}")

    voltage, bias_voltage = voltages_and_biases[sweep_number % len(voltages_and_biases)]
    daq.setDouble('/dev6641/imps/0/output/amplitude', voltage) # Set voltage value
    daq.setDouble('/dev6641/imps/0/bias/value', bias_voltage)

    # Running a sweep
    sweeper.subscribe('/dev6641/imps/0/sample')
    sweeper.execute()
    while not sweeper.finished():
        time.sleep(0.1)
    time.sleep(0.1)
    sweeper.finish()
    sweeper.unsubscribe('*')

    # Extracting the results from the sweeper
    sweeper_results = sweeper.read()
    sweeper_results = sweeper_results["dev6641"]["imps"]["0"]["sample"][0][0]
    params = ["frequency", "absz", "abszstddev", "realz", "imagz",
              "realzstddev", "imagzstddev", "param0", "param0stddev", "param1",
              "param1stddev", "phasez", "phasezstddev", "nexttimestamp"]
    results = {key: sweeper_results[key] for key in params}
    parameters = {key: sweeper_results[key] for key in list(sweeper_results.keys())
                  if key not in params}

    # Saving the parameters to a file
    if sweep_number == 0:
        path = os.path.join(base_path, "Parameters.txt")
        with open(path, "w") as file:
            for key, value in parameters.items():
                file.writelines(f"{key}\t{value}\n")

    # Saving the results to a file
    file_name = get_file_name({"sweep number": sweep_number,
                               "drive voltage": voltage,
                               "bias voltage": bias_voltage})
    path = os.path.join(base_path, file_name)
    save_to_path(path, results)
    sweep_number += 1
