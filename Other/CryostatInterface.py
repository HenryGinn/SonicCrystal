"""
from tools.getpeak import get_peak

peak = get_peak(start=10**5, end=10**6, plot_results=True)
"""

from tools.runexperiment import run_experiment

folder_structure = {"voltage": [0.5, 1, 1.5, 2],
                    "bias_voltage": [0, 0.25, 0.5, 0.75, 1]}

trial_number = 1
while True:
    run_experiment(folder_structure, trial_number)
    trial_number += 1
