"""
This will take in some sweeper settings, run the sweep
find the approximate peak, and then run a finer sweep
around that point. This process is then repeated until
the desired resolution is reached
"""

import os

from hgutilities import defaults
from hgutilities import plotting
from hgutilities.utils.paths import make_folder
import numpy as np
from matplotlib.pyplot import get_current_fig_manager
import matplotlib.pyplot as plt

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
        frequencies = np.arange(self.start, self.end, self.sweep_resolution)
        a, b, c = 10**9, 10**6, 2.5*10**6
        function_values = a / (b**2 + 4*(frequencies - c)**2)
        noise = np.random.rand(self.sweep_points) * function_values / 20
        function_values += noise
        return frequencies, function_values

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
                                    maximise=False, output=False)
            self.set_figure_size()

    def set_figure_size(self):
        mng = get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()

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
