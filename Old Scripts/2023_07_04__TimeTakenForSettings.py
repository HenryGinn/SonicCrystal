import time
import datetime
import math

import zhinst.core
from hgutilities import plotting
import numpy as np


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

# Sweeper bandwidth and other settings
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

def get_time_taken(sample_count=100, max_bandwidth=100):

    # Setting all settings
    sweeper.set('start', 1e6)
    sweeper.set('stop', 5e6)
    sweeper.set('samplecount', sample_count)
    sweeper.set('maxbandwidth', max_bandwidth)
    
    # Subscribing to all the demodulators
    subscribe()

    # Running a sweep
    start_time = time.time()
    sweeper.execute()
    while not sweeper.finished():
        time.sleep(0.001)
    sweeper.finish()
    sweeper.unsubscribe('*')
    end_time = time.time()

    time_taken = end_time - start_time
    print(f"sample count: {sample_count}, max bandwidth: {max_bandwidth}, time taken: {time_taken}")
    return time_taken

def subscribe():
    if oscillator:
        subscribe_oscillator()
    if demodulators:
        subscribe_demodulators()

def subscribe_oscillator():
    sweeper.subscribe('/dev6641/imps/0/sample')

def subscribe_demodulators():
    sweeper.subscribe('/dev6641/demods/0/sample')
    sweeper.subscribe('/dev6641/demods/1/sample')
    sweeper.subscribe('/dev6641/demods/2/sample')
    sweeper.subscribe('/dev6641/demods/3/sample')

sample_counts = [50000]
max_bandwidths = [1]

oscillator = True
demodulators = True

data = [get_time_taken(sample_count, max_bandwidth)
        for sample_count in sample_counts
        for max_bandwidth in max_bandwidths]
print(data)
