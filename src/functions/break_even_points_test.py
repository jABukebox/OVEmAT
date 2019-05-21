###### Calculate Break Even Points from Json results ######

# IMPORTS
import json
import statistics
import pandas as pd
# import matplotlib
# matplotlib.use('PS')
from matplotlib import pyplot as plt
#import matplotlib as plt

# ----------- JSON READ AND MID VALUES --------------- #
with open('../results/json/result_all.json') as f:
    data_all = json.load(f)

# - GET FUEL CYCLE EMISSION VALUES FROM JSON AND CALC THE MEDIAN - #
def get_lce_fc():
    length = len(data_all)
    fc_list_bev = []
    fc_list_fcev = []
    fc_list_phev = []
    fc_list_icev = []

    for index in range(length):
        if data_all[str(index)]['Vehicle'] == 'BEV':
            fc_list_bev.append(data_all[str(index)]['Em_fc'])
        if data_all[str(index)]['Vehicle'] == 'FCEV':
            fc_list_fcev.append(data_all[str(index)]['Em_fc'])
        if data_all[str(index)]['Vehicle'] == 'PHEV':
            fc_list_phev.append(data_all[str(index)]['Em_fc'])
        if data_all[str(index)]['Vehicle'] == 'ICEV':
            fc_list_icev.append(data_all[str(index)]['Em_fc'])

    median_bev = statistics.median(fc_list_bev)
    median_fcev = statistics.median(fc_list_fcev)
    median_phev = statistics.median(fc_list_phev)
    median_icev = statistics.median(fc_list_icev)

    return median_bev, median_fcev, median_phev, median_icev


# - GET VEHICLE CYCLE EMISSION VALUES FROM JSON AND CALC THE MEDIAN - #
def get_lce_vc():
    length = len(data_all)
    vc_list_bev = []
    vc_list_fcev = []
    vc_list_phev = []
    vc_list_icev = []

    for index in range(length):
        if data_all[str(index)]['Vehicle'] == 'BEV':
            vc_list_bev.append(data_all[str(index)]['Em_vc'])
        if data_all[str(index)]['Vehicle'] == 'FCEV':
            vc_list_fcev.append(data_all[str(index)]['Em_vc'])
        if data_all[str(index)]['Vehicle'] == 'PHEV':
            vc_list_phev.append(data_all[str(index)]['Em_vc'])
        if data_all[str(index)]['Vehicle'] == 'ICEV':
            vc_list_icev.append(data_all[str(index)]['Em_vc'])


    median_bev = statistics.median(vc_list_bev)
    median_fcev = statistics.median(vc_list_fcev)
    median_phev = statistics.median(vc_list_phev)
    median_icev = statistics.median(vc_list_icev)

    return median_bev, median_fcev, median_phev, median_icev


# ----- SETTINGS FOR CALCULATION ----- #
distance = 100000  # total distance
range_gaps = 20000  # iter gaps
divisor = 1000   # change emission dimension (original in gramms CO2 (division = 1) /
                                                # division = 1000 --> kg / division = 1000000 --> t )

# -------------------- #


median_bev_vc, median_fcev_vc, median_phev_vc, median_icev_vc = get_lce_vc()
median_bev_fc, median_fcev_fc, median_phev_fc, median_icev_fc = get_lce_fc()


range_emissions = {}

keys = ['bev', 'fcev', 'phev', 'icev']

for count in range(4):
    x_ranges = [0]
    range_gaps_iter = range_gaps
    fc_emission_raw = get_lce_fc()[count]
    vc_emission_raw = get_lce_vc()[count]
    fc_emission = fc_emission_raw / divisor
    vc_emission = vc_emission_raw / divisor
    emission_list = [vc_emission]

    while range_gaps_iter <= distance:
        calculation = (vc_emission + (range_gaps_iter * fc_emission))
        emission_list.append(calculation)
        x_ranges.append(range_gaps_iter)
        range_gaps_iter += range_gaps

    range_emissions['distance'] = x_ranges
    range_emissions[keys[count]] = emission_list

df = pd.DataFrame.from_dict(range_emissions)
df = df.set_index('distance')


# ----- PLOT ----- #
df.plot(figsize=(12,7))

# Axes
plt.xlabel('Distance [km]')
if divisor == 1:
    plt.ylabel('Emissions [g CO2]')
elif divisor == 1000:
    plt.ylabel('Emissions [kg CO2]')
elif divisor == 1000000:
    plt.ylabel('Emissions [t CO2]')
else:
    plt.ylabel('Emissions [## UNIT UNCLEAR ##]')
plt.xticks(x_ranges)

plt.grid(True)
plt.title('Break Even Points of Drive Technologies')
plt.show()
plt.savefig('filename.png', dpi=300)
