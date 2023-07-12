import hgutilities.plotting as plotting

base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal\\Raw Data\\"
             "2023_07_06\\Voltage_10_V")
plotting.quick(base_path, file_blacklist="Parameter", subplots=1)
