"""
This script is meant to be copy and pasted into a new script for
each new experiment. Do not tailor this script for a specific experiment.
If you want a template that fits the new experiment, make a new template.

This script is based off TemplateMeasurementScript and is very similar.
It does the same thing but it has been prepared to iterate through several
settings. Due to the large variability in its intended use, more of the
structure has deliberately been omitted.
"""

import time
import os
from datetime import datetime
import math

import zhinst.core
from hgutilities.utils.paths import make_folder
from hgutilities.utils.printiterable import get_iterable_string
from hgutilities.utils import save_to_path, get_file_name
import numpy as np


################### THESE ARE THE SETTINGS TO CHANGE ###################

# Use pascal case for experiment description
# ThisIsAnExampleOfPascalCase
description = 
date = datetime.now().strftime("%Y_%m_%d")

start_frequency = 250000
stop_frequency = 2000000
resolution = 5
measurements_per_sweep = 50000

bias_voltage = 0
voltage = 4
max_bandwidth = 30

#########################################################################


# Output folder
base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal3\\"
             f"Raw Data\\{date}__{description}")
impedance_path = os.path.join(base_path, "Impedance")
demod_paths = [os.path.join(base_path, f"Demod {i+1}") for i in range(4)]
make_folder(base_path)
print(f"Output folder: {base_path}\n")

# Setting up the MFIA
daq = zhinst.core.ziDAQServer('127.0.0.1', 8004, 6) # Connect API to device
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs

# Setting the demods to be on the first oscillator
daq.setInt('/dev6641/demods/0/oscselect', 0)
daq.setInt('/dev6641/demods/1/oscselect', 0)
daq.setInt('/dev6641/demods/2/oscselect', 0)
daq.setInt('/dev6641/demods/3/oscselect', 0)

# Setting the harmonics
daq.setInt('/dev6641/demods/1/harmonic', 1)
daq.setInt('/dev6641/demods/2/harmonic', 2)
daq.setInt('/dev6641/demods/3/harmonic', 3)

# Set the bandwidths/time constants
daq.setDouble('/dev6641/imps/0/maxbandwidth', 1)
daq.setDouble('/dev6641/demods/0/timeconstant', 0.0611506689)
daq.setDouble('/dev6641/demods/1/timeconstant', 0.0611506689)
daq.setDouble('/dev6641/demods/2/timeconstant', 0.0611506689)
daq.setDouble('/dev6641/demods/3/timeconstant', 0.0611506689)

# Set the demod sample rates
daq.setDouble('/dev6641/demods/0/rate', 13393)
daq.setDouble('/dev6641/demods/1/rate', 13393)
daq.setDouble('/dev6641/demods/2/rate', 13393)
daq.setDouble('/dev6641/demods/3/rate', 13393)

# Enabling the devices
daq.setInt('/dev6641/imps/0/enable', 1)
daq.setInt('/dev6641/demods/0/enable', 1)
daq.setInt('/dev6641/demods/1/enable', 1)
daq.setInt('/dev6641/demods/2/enable', 1)
daq.setInt('/dev6641/demods/3/enable', 1)

# Turning off sinc filters.
daq.setInt('/dev6641/demods/0/sinc', 0) # Demodulator 1
daq.setInt('/dev6641/demods/1/sinc', 0) # Demodulator 2
daq.setInt('/dev6641/demods/2/sinc', 0) # Demodulator 3
daq.setInt('/dev6641/demods/3/sinc', 0) # Demodulator 4

# Setting the input signal for the demods
daq.setInt('/dev6641/demods/1/adcselect', 1) # Demodulator 2
daq.setInt('/dev6641/demods/2/adcselect', 1) # Demodulator 3
daq.setInt('/dev6641/demods/3/adcselect', 1) # Demodulator 4

# Setting up the sweeper
sweeper = daq.sweep()
sweeper.set('device', 'dev6641') # The MFIA device
sweeper.set('bandwidth', 1)
sweeper.set('bandwidthcontrol', 2)
sweeper.set('xmapping', 0) # x axis mode: 0: linear, 1: log

# Set voltage settings
daq.setInt('/dev6641/system/impedance/filter', 1)
daq.setDouble('/dev6641/imps/0/output/range', 10) # Set range
daq.setInt('/dev6641/imps/0/auto/output', 0) # Set manual mode

# Sweeper bandwidth and other settings
sweeper.set('bandwidthoverlap', 1)
sweeper.set('omegasuppression', 80)

# Set orders
sweeper.set('order', 8)
daq.setInt('/dev6641/demods/0/order', 8)
daq.setInt('/dev6641/demods/1/order', 8)
daq.setInt('/dev6641/demods/2/order', 8)
daq.setInt('/dev6641/demods/3/order', 8)

# Sweep settling
sweeper.set('settling/time', 0) # Min time
sweeper.set('settling/inaccuracy', 0.01) # Inaccuracy

# Sweep statistics
sweeper.set('averaging/sample', 1) # Number of samples per point to average
sweeper.set('averaging/time', 0.001)
sweeper.set('averaging/tc', 15)

# Sigins
daq.setInt('/dev6641/sigins/0/ac', 1)
daq.setInt('/dev6641/sigins/0/imp50', 1)
daq.setInt('/dev6641/sigins/0/diff', 0)

# Settings I do not understand
sweeper.set('gridnode', '/dev6641/oscs/0/freq')


# Data about sweep size and time

def get_sweep_frequencies():
    update_start_stop_frequencies()
    total_measurements = (stop_frequency - start_frequency)/resolution
    full_batches = math.floor(total_measurements / measurements_per_sweep)
    frequencies = get_frequencies_initial(full_batches)
    frequencies = get_frequencies_final(frequencies, total_measurements)
    return frequencies

def update_start_stop_frequencies():
    global start_frequency, stop_frequency
    start_frequency = start_frequency - (start_frequency % resolution)
    stop_frequency = stop_frequency + (stop_frequency % resolution)

def get_frequencies_initial(full_batches):
    sweep_width = measurements_per_sweep*resolution
    frequencies = [[start_frequency + index*sweep_width,
                    start_frequency + (index + 1)*sweep_width - resolution]
                   for index in range(full_batches)]
    return frequencies

def get_frequencies_final(frequencies, total_measurements):
    measurements = len(frequencies) * measurements_per_sweep
    leftover_measurements = total_measurements - measurements
    add_to_frequencies_initial(frequencies, leftover_measurements)
    return frequencies

def add_to_frequencies_initial(frequencies, leftover_measurements):
    if leftover_measurements == 0:
        frequencies[-1][1] += resolution
    else:
        frequencies += [[stop_frequency - leftover_measurements*resolution, stop_frequency]]

def sweeps_to_be_taken_message():
    print(f"{len(sweep_frequencies)} sweep{'s'*(len(sweep_frequencies) != 1)} to be taken:")
    for start_sweep_frequency, stop_sweep_frequency in sweep_frequencies:
        print(f"Start: {start_sweep_frequency}, stop: {stop_sweep_frequency}")
    print("")

def time_taken_message():
    first_sweep = time.time() + get_sweep_time(sweep_frequencies[0])
    time_taken = get_time_taken()
    finish_time = time.time() + time_taken
    print_time_taken_message(first_sweep, time_taken, finish_time)

def get_time_taken():
    time_taken = sum([get_sweep_time(frequency_limits)
                      for frequency_limits in sweep_frequencies])
    time_taken = max(1, time_taken)
    return time_taken

def get_sweep_time(frequency_limits):
    points_per_sweep = (frequency_limits[1] - frequency_limits[0])/resolution + 1
    return ((0.6 - 1/40*math.sqrt(points_per_sweep) + 7/216*points_per_sweep)
            * (1 + 57/max_bandwidth - 626/5*1/max_bandwidth**2
               + 595/max_bandwidth**3 - 878/max_bandwidth**4 + 410/max_bandwidth**5))

def print_time_taken_message(first_sweep, time_taken, finish_time):
    first_sweep_finish_string = datetime.fromtimestamp(first_sweep).strftime('%H:%M:%S')
    time_taken_string = datetime.fromtimestamp(time_taken).strftime('%H:%M:%S')
    finish_time_string = datetime.fromtimestamp(finish_time).strftime("%Y_%m_%d %H:%M:%S")
    print(f"First sweep finish: {first_sweep_finish_string}\n"
          f"Time until finish:  {time_taken_string}\n"
          f"Finish time:        {finish_time_string}\n")

def get_finish_time(sweep_index):
    time_taken = get_sweep_time(sweep_frequencies[sweep_index])
    finish_time = time.time() + time_taken
    return datetime.fromtimestamp(finish_time).strftime("%Y_%m_%d %H:%M:%S")


# Running the sweeper

def set_frequencies(sweep_number):
    sweep_start_frequency, sweep_stop_frequency = sweep_frequencies[sweep_number]
    sweeper.set('start', sweep_start_frequency)
    sweeper.set('stop', sweep_stop_frequency)
    sample_count = (sweep_stop_frequency - sweep_start_frequency)/resolution + 1
    sweeper.set('samplecount', sample_count)

def progress_indicator(sweep_number):
    sweep_time = datetime.now().strftime("%Y_%m_%d %H:%M:%S")
    finish_time = get_finish_time(sweep_number)
    print(f"Sweep started: {sweep_time}, ({start_frequency}, {stop_frequency}), "
          f"Finish time: {finish_time}")

def subscribe():
    sweeper.subscribe('/dev6641/imps/0/sample')
    subscripe_to_demods()

def subscripe_to_demods():
    sweeper.subscribe('/dev6641/demods/0/sample')
    sweeper.subscribe('/dev6641/demods/1/sample')
    sweeper.subscribe('/dev6641/demods/2/sample')
    sweeper.subscribe('/dev6641/demods/3/sample')

def run_sweep():
    sweeper.execute()
    while not sweeper.finished():
        time.sleep(0.1)
    time.sleep(0.1)
    sweeper.finish()
    sweeper.unsubscribe('*')


# Getting data from the sweeper

def save_metadata():
    print("Collecting and saving metadata")
    sweeper.set('samplecount', 3)
    subscribe()
    run_sweep()
    sweeper_results = sweeper.read()
    save_metadata_to_file(sweeper_results)

def save_metadata_to_file(sweeper_results):
    sweeper_results_string = get_iterable_string(sweeper_results)
    metadata_path = os.path.join(base_path, "Metadata.txt")
    with open(metadata_path, "w") as file:
        file.writelines(sweeper_results_string)

def get_impedance_results(sweeper_results):
    impedance_results = sweeper_results["dev6641"]["imps"]["0"]["sample"][0][0]
    impedance_results = results = {key: impedance_results[key]
                                   for key in impedance_parameters}
    return impedance_results

def get_demod_results(sweeper_results):
    demod_results = sweeper_results["dev6641"]["demods"]
    demod_results = [demod_results[str(demod_number)]["sample"][0][0]
                     for demod_number in range(4)]
    demod_results = [{key: demod_result[key] for key in demod_parameters}
                     for demod_result in demod_results]
    return demod_results


# Saving results to files

def save_impedance_results(impedance_results, sweep_number):
    impedance_file_name = get_impedance_file_name(sweep_number)
    path = os.path.join(impedance_path, impedance_file_name)
    save_to_path(path, impedance_results)

def get_impedance_file_name(sweep_number):
    sweep_start_frequency, sweep_stop_frequency = sweep_frequencies[sweep_number]
    impedance_file_name = get_file_name({"start frequency": sweep_start_frequency,
                                         "stop frequency": sweep_stop_frequency})
    return impedance_file_name

def save_demod_results(demod_results, sweep_number):
    for demod_index, demod_results in enumerate(demod_results):
        file_name = get_demod_file_name(demod_index, sweep_number)
        path = os.path.join(demod_paths[demod_index], file_name)
        save_to_path(path, demod_results)

def get_demod_file_name(demod_index, sweep_number):
    sweep_start_frequency, sweep_stop_frequency = sweep_frequencies[sweep_number]
    file_name = get_file_name({"start frequency": sweep_start_frequency,
                               "stop frequency": sweep_stop_frequency,
                               "demod": demod_index + 1})
    return file_name


# Parameters to be recorded
impedance_parameters = ["frequency", "absz", "abszstddev", "realz", "imagz",
                        "realzstddev", "imagzstddev", "param0", "param0stddev", "param1",
                        "param1stddev", "phasez", "phasezstddev", "nexttimestamp"]

demod_parameters = ["frequency", "r", "phase", "x", "y",
                    "rstddev", "phasestddev", "xstddev", "ystddev", "nexttimestamp"]

sweep_frequencies = get_sweep_frequencies()
sweeps_to_be_taken_message()
time_taken_message()

# Running a small sweep to record the metadata
daq.setDouble('/dev6641/imps/0/bias/value', ) # Bias voltage
daq.setDouble('/dev6641/imps/0/output/amplitude', ) # Drive voltage
sweeper.set('maxbandwidth', max_bandwidth) # Max bandwidth
save_metadata()
sweeper.set('samplecount', points_per_batch)

for SETTING in SETTINGS:
    
    daq.setDouble('/dev6641/imps/0/bias/value', bias_voltage)
    daq.setDouble('/dev6641/imps/0/output/amplitude', voltage)

    for sweep_number in range(len(sweep_frequencies)):

        # Running sweep
        set_frequencies(sweep_number)
        progress_indicator(sweep_number)
        subscribe()
        run_sweep()

        # Extracting results
        sweeper_results = sweeper.read()
        impedance_results = get_impedance_results(sweeper_results)
        demod_results = get_demod_results(sweeper_results)

        # Saving results to files
        save_impedance_results(impedance_results)
        save_demod_results(demod_results)
