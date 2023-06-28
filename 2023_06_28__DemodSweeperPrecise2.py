import time
import os
import datetime
import math

import zhinst.core
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
import numpy as np

from tools import *


# Making the folders where the settings will be saved
base_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-28__BackgroundFrequencySweep"

base_paths = [os.path.join(base_path, f"Demod_{demod_index}")
                           for demod_index in range(1, 5)]
for path in base_paths:
    make_folder(path)


# Setting up the MFIA
daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6) # Connect API to device
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs

# Setting up the device
daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs
daq.setDouble('/dev6641/imps/0/maxbandwidth', 1)

# Setting up the sweeper
sweeper = daq.sweep()
sweeper.set('device', 'dev6641') # The MFIA device
sweeper.set('xmapping', 0) # x axis mode: 0: linear, 1: log

# Set voltage settings
daq.setInt('/dev6641/system/impedance/filter', 1)
daq.setDouble('/dev6641/imps/0/output/range', 10) # Set range
daq.setInt('/dev6641/imps/0/auto/output', 0) # Set manual mode
daq.setDouble('/dev6641/imps/0/output/amplitude', 4) # Set drive voltage
daq.setDouble('/dev6641/imps/0/bias/value', 0) # Set bias voltage

# Frequency settings
sweeper.set('samplecount', 50001) # The number of points in a sweep


# Sweeper bandwidth and other settings
sweeper.set('bandwidth', 1)
sweeper.set('maxbandwidth', 100)
sweeper.set('bandwidthoverlap', 1)
sweeper.set('order', 8)
sweeper.set('omegasuppression', 80)

# Sweep settling
sweeper.set('settling/time', 0) # Min time
sweeper.set('settling/inaccuracy', 0.01) # Inaccuracy

# Sweep statistics
sweeper.set('averaging/sample', 1) # Number of samples per point to average
sweeper.set('averaging/time', 0.001)
sweeper.set('averaging/tc', 15)


# Settings I do not understand
sweeper.set('gridnode', '/dev6641/oscs/0/freq')

for sweep_number in range(5, 40):

    # Start and stop frequency
    start_frequency = 50000*sweep_number
    stop_frequency = 50000*(sweep_number + 1)
    sweeper.set('start', start_frequency)
    sweeper.set('stop', stop_frequency)

    # Progress indicator
    sweep_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Sweep number: {sweep_number:04d}, {sweep_time}, ({start_frequency}, {stop_frequency})")
    
    # Subscribing to all the demodulators
    sweeper.subscribe('/dev6641/demods/0/sample')
    sweeper.subscribe('/dev6641/demods/1/sample')
    sweeper.subscribe('/dev6641/demods/2/sample')
    sweeper.subscribe('/dev6641/demods/3/sample')

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
    if sweep_number == 5:
        for demod_index, parameter_results in enumerate(parameters):
            path = os.path.join(base_paths[demod_index], f"Parameters_0__Demod_{demod_index + 1}.txt")
            with open(path, "w") as file:
                for key, value in parameter_results.items():
                    file.writelines(f"{key}\t{value}\n")
    
    # Saving the results to files
    for demod_index, demod_results in enumerate(results):
        file_name = get_file_name({"start frequency": start_frequency,
                                   "stop frequency": stop_frequency,
                                   "sweep number": sweep_number,
                                   "demod": demod_index + 1})
        path = os.path.join(base_paths[demod_index], file_name)
        save_to_path(path, demod_results)
