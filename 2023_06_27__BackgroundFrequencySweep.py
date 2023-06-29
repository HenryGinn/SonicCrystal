import time
import os
import datetime

import zhinst.core

from tools import get_file_name, save_to_path

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
sweeper.set('maxbandwidth', 500)
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

# Preparing for sweeping
base_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\2023-06-27__BackgroundFrequencySweep"

for sweep_number in range(10, 40):
    # Progress indicator
    sweep_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Sweep number: {sweep_number:04d}, {sweep_time}")

    start_frequency = 50000*sweep_number
    stop_frequency = 50000*(sweep_number + 1)
    print(start_frequency, stop_frequency)
    sweeper.set('start', start_frequency)
    sweeper.set('stop', stop_frequency)

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
    if sweep_number == 1:
        path = os.path.join(base_path, "Parameters.txt")
        with open(path, "w") as file:
            for key, value in parameters.items():
                file.writelines(f"{key}\t{value}\n")

    # Saving the results to a file
    file_name = get_file_name({"start frequency": start_frequency,
                               "stop frequency": stop_frequency,
                               "sweep number": sweep_number - 8})
    path = os.path.join(base_path, file_name)
    save_to_path(path, results)
