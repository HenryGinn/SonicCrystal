import time
import os
import datetime
import math

import zhinst.core
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
import numpy as np

from tools import save_to_path, get_file_name


# Making the folders where the settings will be saved
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\"
             "Raw Data\\2023_07_04__DemodAndCapacitance")


# Setting up the MFIA
daq = zhinst.core.ziDAQServer('127.0.0.1', 8004, 6) # Connect API to device
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs

# Setting the demods to be on the first oscillator      # Added on 2023_07_04
daq.setInt('/dev6641/demods/0/oscselect', 0)
daq.setInt('/dev6641/demods/1/oscselect', 0)
daq.setInt('/dev6641/demods/2/oscselect', 0)
daq.setInt('/dev6641/demods/3/oscselect', 0)

# Setting the harmonics                                 # Added on 2023_07_04
daq.setInt('/dev6641/demods/1/harmonic', 2)
daq.setInt('/dev6641/demods/2/harmonic', 3)
daq.setInt('/dev6641/demods/3/harmonic', 4)

# Enabling the devices
daq.setInt('/dev6641/imps/0/enable', 1)
daq.setInt('/dev6641/demods/0/enable', 1)
daq.setInt('/dev6641/demods/1/enable', 1)
daq.setInt('/dev6641/demods/2/enable', 1)
daq.setInt('/dev6641/demods/3/enable', 1)

daq.setDouble('/dev6641/imps/0/maxbandwidth', 1)

# Turning off sinc filters.
daq.setInt('/dev6641/demods/0/sinc', 0) # Demodulator 1
daq.setInt('/dev6641/demods/1/sinc', 0) # Demodulator 2
daq.setInt('/dev6641/demods/2/sinc', 0) # Demodulator 3
daq.setInt('/dev6641/demods/3/sinc', 0) # Demodulator 4

# Setting up the sweeper
sweeper = daq.sweep()
sweeper.set('device', 'dev6641') # The MFIA device
sweeper.set('bandwidth', 1)
sweeper.set('bandwidthcontrol', 2)
sweeper.set('xmapping', 0) # x axis mode: 0: linear, 1: log

# Settings I do not understand
sweeper.set('gridnode', '/dev6641/oscs/0/freq')

# Set voltage settings
daq.setInt('/dev6641/system/impedance/filter', 1)
daq.setDouble('/dev6641/imps/0/output/range', 10) # Set range
daq.setInt('/dev6641/imps/0/auto/output', 0) # Set manual mode
daq.setDouble('/dev6641/imps/0/output/amplitude', 1) # Set drive voltage
daq.setDouble('/dev6641/imps/0/bias/value', 0) # Set bias voltage

# Frequency settings
#sweeper.set('samplecount', 11)
sweeper.set('samplecount', 2001) # The number of points in a sweep

# Sweeper bandwidth and other settings
sweeper.set('maxbandwidth', 75)
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

# Parameters to be recorded
impedance_parameters = ["frequency", "absz", "abszstddev", "realz", "imagz",
                        "realzstddev", "imagzstddev", "param0", "param0stddev", "param1",
                        "param1stddev", "phasez", "phasezstddev", "nexttimestamp"]

demod_parameters = ["frequency", "r", "phase", "x", "y",
                    "rstddev", "phasestddev", "xstddev", "ystddev", "nexttimestamp"]

first_loop = True

def run_sweep(sweeper):
    sweeper.execute()
    while not sweeper.finished():
        time.sleep(0.1)
    time.sleep(0.1)
    sweeper.finish()
    sweeper.unsubscribe('*')

def subscribe(sweeper):
    sweeper.subscribe('/dev6641/imps/0/sample')
    sweeper.subscribe('/dev6641/demods/0/sample')
    sweeper.subscribe('/dev6641/demods/1/sample')
    sweeper.subscribe('/dev6641/demods/2/sample')
    sweeper.subscribe('/dev6641/demods/3/sample')

# THIS IS CURRENTLY SET UP TO DO A SWEEP FROM 250K TO 2M WITH A RESOLUTION OF 1 HZ
# WITH A BANDWIDTH OF 10 AND A VOLTAGE OF 1.



for voltage in [4]:# IF YOU WANT TO DO MULTIPLE TRIALS, UNCOMMENT THIS BIT AND INDENT THE FOR LOOP
    daq.setDouble('/dev6641/imps/0/output/amplitude', voltage)
    for sweep_number in range(29, 40):

        # Start and stop frequency
        start_frequency = 50000*sweep_number
        stop_frequency = 50000*(sweep_number + 1)
        sweeper.set('start', start_frequency)
        sweeper.set('stop', stop_frequency)

        # Progress indicator
        sweep_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{sweep_time}, ({start_frequency}, {stop_frequency})")
        
        subscribe(sweeper)
        run_sweep(sweeper)
        sweeper_results = sweeper.read()

        # Extracting demod data
        demod_results = sweeper_results["dev6641"]["demods"]
        demod_results = [demod_results[str(demod_number)]["sample"][0][0]
                         for demod_number in range(4)]
        demod_results = [{key: demod_result[key] for key in demod_parameters}
                         for demod_result in demod_results]
        demods_meta_data = [{key: demod_result[key] for key in list(demod_result.keys())
                             if key not in demod_parameters}
                            for demod_result in demod_results]

        # Extracting impedance data
        impedance_results = sweeper_results["dev6641"]["imps"]["0"]["sample"][0][0]
        results = {key: impedance_results[key] for key in impedance_parameters}
        impedance_meta_data = {key: impedance_results[key] for key in list(impedance_results.keys())
                               if key not in impedance_parameters}

        # Making the folders for each trial
        impedance_path = os.path.join(base_path, f"Voltage_{voltage}_V", "Impedance")
        demod_paths = [os.path.join(base_path, f"voltage_{voltage}_V", f"Demod_{demod_index}")            #IF YOU WANT TO DO MULTIPLE TRIALS, UNCOMMENT THIS BIT
                       for demod_index in range(1, 5)]
        make_folder(impedance_path)
        for path in demod_paths:
            make_folder(path)

        # Saving the impedance parameters to a file
        if first_loop:
            path = os.path.join(base_path, "Parameters__Impedance.txt")
            with open(path, "w") as file:
                for key, value in impedance_meta_data.items():
                    file.writelines(f"{key}\t{value}\n")

        # Saving the demod parameters to files
        if first_loop:
            for demod_index, demod_meta_data in enumerate(demods_meta_data):
                path = os.path.join(demod_paths[demod_index], f"Parameters__Demod_{demod_index + 1}.txt")
                with open(path, "w") as file:
                    for key, value in demod_meta_data.items():
                        file.writelines(f"{key}\t{value}\n")

        # Saving the impedance results to files
        impedance_file_name = get_file_name({"start frequency": start_frequency,
                                   "stop frequency": stop_frequency})
        path = os.path.join(impedance_path, impedance_file_name)
        save_to_path(path, results)
        
        # Saving the demod results to files
        for demod_index, demod_results in enumerate(demod_results):
            file_name = get_file_name({"start frequency": start_frequency,
                                       "stop frequency": stop_frequency,
                                       "demod": demod_index + 1})
            path = os.path.join(demod_paths[demod_index], file_name)
            save_to_path(path, demod_results)

        first_loop = False
