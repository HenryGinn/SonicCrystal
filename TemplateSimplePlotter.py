import hgutilities.plotting as plotting

# Folder names are of the form "yyyy_mm_dd__Description"
year = "2023"
month = "07"
day =
description =

# Impedance parameters
# 0: frequency,
# 1: absz, 2: abszstddev
# 3: realz, 4: imagz, 5: realzstddev, 6: imagzstd
# 7: param0, 8: param0stddev
# 9: param1, 10: param1stddev
# 11: phasez, 12: phasezstddev
# 13: nexttimestamp

# Demod parameters
# 0: frequency,
# 1: r, 2: phase, 3: x, 4: y,
# 5: rstddev, 6: phasestddev,
# 7: xstddev, 8: ystddev,
# 9: nexttimestamp

column_index = 1

base_path = ("D:\\Documents\\Experiments Data\\SonicCrystal2\\Processed Data"
             f"\\{year}_{month}_{day}__{description}\\Data\\")

plotting.quick(base_path, subplots=1, y=column_index)

