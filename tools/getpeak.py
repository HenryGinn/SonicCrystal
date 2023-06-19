"""
This will take in some sweeper settings, run the sweep
find the approximate peak, and then run a finer sweep
around that point. This process is then repeated until
the desired resolution is reached
"""

import os
import time

from hgutilities import defaults
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
import numpy as np
import matplotlib.pyplot as plt
import zhinst.core

from .files import save_to_path

class GetPeak():

    def __init__(self, **kwargs):
        defaults.kwargs(self, kwargs)
        self.update_window_attributes()
        self.lines_objects = []
        self.create_folder()

    def find_peak(self):
        self.attempt_counter = 0
        while self.run_find_peak_loop():
            self.iterate()
        self.plot()
        return self.peak_frequency

    def update_window_attributes(self):
        self.sweep_width = self.end - self.start
        self.sweep_resolution = self.sweep_width / self.sweep_points

    def create_folder(self):
        if self.save_results:
            self.path = os.path.join(self.base_path, "FindingPeak")
            make_folder(self.path)

    def run_find_peak_loop(self):
        if self.attempt_counter == 0:
            return True
        elif self.attempt_counter < self.attempt_count_limit:
            return self.sweep_resolution > self.target_resolution
        else:
            return False

    def iterate(self):
        self.frequencies, self.values = self.run_sweep()
        self.update_peak_window()
        self.add_lines_obj()
        self.save()
        self.attempt_counter += 1

    def run_sweep(self):
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
        sweeper.set('start', self.start)
        sweeper.set('stop', self.end)
        sweeper.set('maxbandwidth', 100)
        sweeper.set('omegasuppression', 80)
        sweeper.set('order', 8)
        sweeper.set('samplecount', self.sweep_points)

        sweeper.subscribe('/dev6641/imps/0/sample')
        sweeper.execute()
        while not sweeper.finished():
            time.sleep(0.1)
        time.sleep(0.1)
        sweeper.finish()
        sweeper.unsubscribe('*')

        results = sweeper.read()
        results = results["dev6641"]["imps"]["0"]["sample"][0][0]
        frequencies = results["frequency"]
        values = results["param1"]
        return frequencies, values

    def update_peak_window(self):
        peak_index = np.argmax(self.values)
        self.peak_value = self.values[peak_index]
        self.peak_frequency = self.frequencies[peak_index]
        half_width = self.sweep_width * self.contraction_ratio / 2
        self.start = self.peak_frequency - half_width
        self.end = self.peak_frequency + half_width
        self.update_window_attributes()

    def add_lines_obj(self):
        if self.plot_results:
            line_obj = plotting.line(self.frequencies, self.values)
            peak_point = plotting.line(self.peak_frequency, self.peak_value, marker="*", color="r")
            kwargs = self.get_kwargs()
            lines_obj = plotting.lines([line_obj, peak_point], **kwargs)
            self.lines_objects.append(lines_obj)

    def get_kwargs(self):
        title = self.get_title()
        kwargs = {"title": title, "x_label": "Frequency", "y_label": "Amplitude"}
        return kwargs

    def get_title(self):
        title = (f"Sweep {self.attempt_counter + 1}, "
                 f"Range = {round(self.start)} - {round(self.end)}, "
                 f"Width = {round(self.end - self.start)}")
        return title

    def plot(self):
        if self.plot_results:
            plotting.create_figures(self.lines_objects, title="Finding Peak",
                                    aspect_ratio=self.aspect_ratio)

    def save(self):
        if self.save_results:
            results = {"frequency (Hz)": self.frequencies,
                       "Amplitude": self.values}
            path = os.path.join(self.path, f"Sweep_{self.attempt_counter + 1}.txt")
            save_to_path(path, results)

defaults.load(GetPeak)

def get_peak(**kwargs):
    get_peak_obj = GetPeak(**kwargs)
    get_peak_obj.find_peak()
    return get_peak_obj.peak_frequency
