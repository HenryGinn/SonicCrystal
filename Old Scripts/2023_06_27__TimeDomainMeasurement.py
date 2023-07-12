import os
import time

import zhinst.core
from hgutilities import plotting
import numpy as np

# Setting up the device and sweeper
daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs
daq.setInt('/dev6641/imps/0/enable', 1) # Enable the MFIA. 0: disabled, 1: enabled

# Set voltage range
daq.setInt('/dev6641/system/impedance/filter', 1)
daq.setDouble('/dev6641/imps/0/output/range', 1) # Set range

# Set drive voltage
daq.setInt('/dev6641/imps/0/auto/output', 0) # Set manual mode
daq.setDouble('/dev6641/imps/0/output/amplitude', 1) # Set voltage value

# Starting module dataAcquisitionModule on 2023/06/27 11:32:51
daq_module = daq.dataAcquisitionModule()
daq_module.set('triggernode', '/dev6641/demods/0/sample.R')
daq_module.set('preview', 1)
daq_module.set('device', 'dev6641')
daq_module.set('historylength', 100)
daq_module.set('bandwidth', 0)
daq_module.set('hysteresis', 0.01)
daq_module.set('level', 0.1)
daq_module.set('save/directory', 'D:\\Documents\\Zurich Instruments\\LabOne\\WebServer')
daq_module.set('clearhistory', 1)
daq_module.set('bandwidth', 0)
daq_module.set('endless', 0)
daq_module.set('grid/rowrepetition', 0)
daq_module.set('grid/cols', 100) # Each column is 74.6667 microseconds
daq_module.set('grid/mode', 4) # 1: linear, 2: nearest, 4: on grid (3 is unknown)
daq_module.set('type', 0)
daq_module.set('bandwidth', 0)

daq_module.set('endless', 1)
daq_module.subscribe('/dev6641/imps/0/sample.Param1.avg')
daq_module.execute()
while not daq_module.finished():
    print(daq_module.progress())
    time.sleep(0.01)
time.sleep(0.1)
result = daq_module.read()
print(result)
daq_module.finish()
daq_module.unsubscribe('*')
