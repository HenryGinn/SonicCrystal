"""
import csv
import urllib.request
import codecs

url = "http://127.0.0.1:8006/netlink?id=c0p1t6p1cfplotmath&ziSessionId=2"
webpage = urllib.request.urlopen(url)
datareader = csv.reader(codecs.iterdecode(webpage, 'utf-8'))
data = []

for row in datareader:
    data.append(row)
print(data)
"""

import time
import zhinst.core
from hgutilities import plotting
import numpy as np

daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
daq.setInt('/dev6641/imps/0/mode', 1) # 0: 4 terminal, 1: 2 terminal
daq.setInt('/dev6641/imps/0/model', 1) # The representation. 0: Rp || Cp, 1: Rs + Cs
sweeper = daq.sweep()
sweeper.set('device', 'dev6641') # The MFIA device
sweeper.set('xmapping', 0) # x axis mode: 0: linear, 1: log
sweeper.set('historylength', 100)
sweeper.set('settling/inaccuracy', 0.01)
sweeper.set('averaging/sample', 20)
sweeper.set('averaging/tc', 15)
sweeper.set('averaging/time', 0.1)
sweeper.set('bandwidth', 10)
sweeper.set('maxbandwidth', 100)
sweeper.set('bandwidthoverlap', 1)
sweeper.set('omegasuppression', 80)
sweeper.set('order', 8)
sweeper.set('gridnode', '/dev6641/oscs/0/freq')
sweeper.set('save/directory', 'D:\\Documents\\Zurich Instruments\\LabOne\\WebServer')
sweeper.set('averaging/sample', 20)
sweeper.set('averaging/tc', 15)
sweeper.set('averaging/time', 0.1)
sweeper.set('bandwidth', 10)
sweeper.set('bandwidthoverlap', 1)
sweeper.set('start', 1000)
sweeper.set('stop', 1000000)
sweeper.set('maxbandwidth', 100)
sweeper.set('omegasuppression', 80)
sweeper.set('order', 8)

sweeper.subscribe('/dev6641/imps/0/sample')
sweeper.execute()
while not sweeper.finished():
    time.sleep(0.1)
time.sleep(0.1)
sweeper.finish()
sweeper.unsubscribe('*')

results = sweeper.read()
results = results["dev6641"]["imps"]["0"]["sample"][0][0]

frequency = results["frequency"]

lines_objects = []
for key, value in results.items():
    if isinstance(value, np.ndarray):
        if key != "frequency":
            line_obj = plotting.line(frequency, value)
            lines_obj = plotting.lines(line_obj, title=key)
            lines_objects.append(lines_obj)

figures_obj = plotting.create_figures(lines_objects, subplots=8)
