"""
import zhinst.core
import time

results_path = "D:\\Documents\\Python Scripts\\Scripts Henry\\CryostatInterface\\Results"

daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
daq.setDouble('/dev6641/imps/0/freq', 10000)

sweeper = daq.sweep()
sweeper.set('device', 'dev6641')
sweeper.subscribe('/dev6641/imps/0/sample')
sweeper.execute()
sweeper.unsubscribe("*")
#sweeper.set('save/directory', results_path)
sweeper.set("save/saveonread", True)
sweeper.save("bob")
a = sweeper.read()
print(a)
"""

from getpeak import get_peak
get_peak(plot_results=True)
