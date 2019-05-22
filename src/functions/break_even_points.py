###### Calculate Break Even Points from Json results ######

# IMPORTS
import json
import os
import statistics
import pandas as pd
import matplotlib as mpl
mpl.use("Qt5Agg")
from matplotlib import pyplot as plt


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ----------- JSON READ AND MID VALUES --------------- #

# - GET FUEL CYCLE EMISSION VALUES FROM Results AND CALC THE MEDIAN - #
def get_lce_fc(data_all):
    bev_data = data_all[data_all['Vehicle'] == 'BEV']
    fc_list_bev = bev_data['Em_fc']

    fcev_data = data_all[data_all['Vehicle'] == 'FCEV']
    fc_list_fcev = fcev_data['Em_fc']

    phev_data = data_all[data_all['Vehicle'] == 'PHEV']
    fc_list_phev = phev_data['Em_fc']

    icev_data = data_all[data_all['Vehicle'] == 'ICEV']
    fc_list_icev = icev_data['Em_fc']

    median_bev = statistics.median(fc_list_bev)
    median_fcev = statistics.median(fc_list_fcev)
    median_phev = statistics.median(fc_list_phev)
    median_icev = statistics.median(fc_list_icev)

    return median_bev, median_fcev, median_phev, median_icev

def get_lce_vc(data_all):

    bev_data = data_all[data_all['Vehicle'] == 'BEV']
    vc_list_bev = bev_data['Em_vc']

    fcev_data = data_all[data_all['Vehicle'] == 'FCEV']
    vc_list_fcev = fcev_data['Em_vc']

    phev_data = data_all[data_all['Vehicle'] == 'PHEV']
    vc_list_phev = phev_data['Em_vc']

    icev_data = data_all[data_all['Vehicle'] == 'ICEV']
    vc_list_icev = icev_data['Em_vc']


    median_bev = statistics.median(vc_list_bev)
    median_fcev = statistics.median(vc_list_fcev)
    median_phev = statistics.median(vc_list_phev)
    median_icev = statistics.median(vc_list_icev)

    return median_bev, median_fcev, median_phev, median_icev

def break_calc(data_all):
    #global data_all

    # ----- SETTINGS FOR CALCULATION ----- #
    distance = 100000  # total distance
    range_gaps = 20000  # iter gaps
    divisor = 1000   # change emission dimension (original in gramms CO2 (division = 1) /
                                                    # division = 1000 --> kg / division = 1000000 --> t )

    # -------------------- #

    range_emissions = {}

    keys = ['bev', 'fcev', 'phev', 'icev']

    for count in range(4):
        x_ranges = [0]
        range_gaps_iter = range_gaps
        fc_emission_raw = get_lce_fc(data_all)[count]
        vc_emission_raw = get_lce_vc(data_all)[count]
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

    window = df.plot(figsize=(10,4))
    man = plt.get_current_fig_manager()
    man.canvas.set_window_title("OVEmAT - Break Even Points")

    # Axes
    plt.xlabel('Distance [km]')
    if divisor == 1:
        plt.ylabel('Total Emissions [g CO2]')
    elif divisor == 1000:
        plt.ylabel('Total Emissions [kg CO2]')
    elif divisor == 1000000:
        plt.ylabel('Total Emissions [t CO2]')
    else:
        plt.ylabel('Total Emissions [## UNIT UNCLEAR ##]')
    plt.xticks(x_ranges)

    plt.grid(True)
    plt.title('Break Even Points of Drive Technologies')


    plt.show()
    #plt.savefig('filename.png', dpi=300)   #




if __name__ == '__main__':
    with open('../results/json/result_all.json') as f:
        data_all = json.load(f)
    break_calc(data_all)

else:
    with open('results/json/result_all.json') as f:
        data_all = json.load(f)