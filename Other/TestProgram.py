import hgutilities.plotting as plotting

base_path = "D:\\Documents\\Experiments Data\\SonicCrystal\\2023_06_28__BackgroundFrequencySweep"
plotting.quick(base_path, file_blacklist="Parameter", y=1, subplots=4, color="blue")
