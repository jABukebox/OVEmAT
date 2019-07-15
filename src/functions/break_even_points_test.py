###### Calculate Break Even Points from Json results ######

# IMPORTS
import json
import os
import statistics
import pandas as pd
import matplotlib as mpl
mpl.use("Qt5Agg")
import matplotlib.gridspec as gridspec
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


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


# - GET TCO VALUES FROM Results AND CALC THE MEDIAN - #
def get_tco_capex(data_all):
    bev_data = data_all[data_all['Vehicle'] == 'BEV']
    capex_list_bev = bev_data['TCO_Capex']

    fcev_data = data_all[data_all['Vehicle'] == 'FCEV']
    capex_list_fcev = fcev_data['TCO_Capex']

    phev_data = data_all[data_all['Vehicle'] == 'PHEV']
    capex_list_phev = phev_data['TCO_Capex']

    icev_data = data_all[data_all['Vehicle'] == 'ICEV']
    capex_list_icev = icev_data['TCO_Capex']


    median_bev = statistics.median(capex_list_bev)
    median_fcev = statistics.median(capex_list_fcev)
    median_phev = statistics.median(capex_list_phev)
    median_icev = statistics.median(capex_list_icev)

    return median_bev, median_fcev, median_phev, median_icev

def get_tco_opex(data_all):
    bev_data = data_all[data_all['Vehicle'] == 'BEV']
    opex_list_bev = bev_data['TCO_Opex']
    print(opex_list_bev)

    fcev_data = data_all[data_all['Vehicle'] == 'FCEV']
    opex_list_fcev = fcev_data['TCO_Opex']

    phev_data = data_all[data_all['Vehicle'] == 'PHEV']
    opex_list_phev = phev_data['TCO_Opex']

    icev_data = data_all[data_all['Vehicle'] == 'ICEV']
    opex_list_icev = icev_data['TCO_Opex']


    median_bev = statistics.median(opex_list_bev)
    median_fcev = statistics.median(opex_list_fcev)
    median_phev = statistics.median(opex_list_phev)
    median_icev = statistics.median(opex_list_icev)

    return median_bev, median_fcev, median_phev, median_icev

def break_calc(data_all, ghg_tax):

    # ----- SETTINGS FOR CALCULATION ----- #
    distance = 100000  # total distance
    range_gaps = 20000  # iter gaps
    divisor = 1000000   # change emission dimension (original in gramms CO2 (division = 1) /
                                                    # division = 1000 --> kg / division = 1000000 --> t )
    #ghg_tax = 60
    if divisor == 1:
        ghg_tax = ghg_tax/1000000
    elif divisor == 1000:
        ghg_tax = ghg_tax/ 1000
    elif divisor == 1000000:
        pass

    else:
        plt.ylabel('Total Emissions [## UNIT UNCLEAR ##]')

    # -------------------- #

    range_emissions_dict = {}
    range_tco_dict = {}


    keys = ['BEV', 'FCEV', 'PHEV', 'ICEV']
    fc_emission_raw_list = []
    opex_raw_list = []

    for count in range(len(keys)):
        x_ranges = [0]
        range_gaps_iter = range_gaps

        # ------- LCE
        fc_emission_raw = get_lce_fc(data_all)[count]
        vc_emission_raw = get_lce_vc(data_all)[count]

        fc_emission_raw_list.append(fc_emission_raw)

        fc_emission = fc_emission_raw / divisor
        vc_emission = vc_emission_raw / divisor
        emission_list = [vc_emission]

        # ------- TCO
        opex_raw = get_tco_opex(data_all)[count]
        capex_raw = get_tco_capex(data_all)[count]

        opex_raw_list.append(opex_raw)

        capex = capex_raw #+ (fc_emission * ghg_tax) #/ divisor_capex           ??
        opex = opex_raw #+ (vc_emission * ghg_tax) #/ divisor_capex             ??
        capex_start = capex + (ghg_tax * vc_emission)
        tco_list = [capex_start]



        while range_gaps_iter <= distance:
            # -- LCE
            calculation_lce = (vc_emission + (range_gaps_iter * fc_emission))
            emission_list.append(calculation_lce)

            # -- TCO
            calculation_tco = (capex_start + (range_gaps_iter * opex) + (ghg_tax * range_gaps_iter * fc_emission))
            tco_list.append(calculation_tco)

            x_ranges.append(range_gaps_iter)
            range_gaps_iter += range_gaps

        range_emissions_dict['distance'] = x_ranges
        range_emissions_dict[keys[count]] = emission_list

        range_tco_dict['distance'] = x_ranges
        range_tco_dict[keys[count]] = tco_list

    lce_df = pd.DataFrame.from_dict(range_emissions_dict)
    lce_df = lce_df.set_index('distance')

    tco_df = pd.DataFrame.from_dict(range_tco_dict)
    tco_df = tco_df.set_index('distance')
    #print(tco_df.head())



    # ----- LCE PLOT ----- #
    fig = plt.figure(1, figsize=(10,7))

    plt.subplot(211)
    plt.plot(lce_df)

    window = plt.get_current_fig_manager()
    window.canvas.set_window_title("OVEmAT - Break Even Points")

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
    plt.title('Break Even Points Emissions')
    legend = plt.legend(['BEV', 'FCEV', 'PHEV', 'ICEV'], loc='upper left')
    legend1 = plt.legend(['EM_FC_BEV = ' + str(round(fc_emission_raw_list[0], 2)) + ' g CO2 / km',
                          'EM_FC_FCEV = ' + str(round(fc_emission_raw_list[1], 2)) + ' g CO2 / km',
                          'EM_FC_PHEV = ' + str(round(fc_emission_raw_list[2], 2)) + ' g CO2 / km',
                          'EM_FC_ICEV = ' + str(round(fc_emission_raw_list[3], 2)) + ' g CO2 / km'], loc='lower right')

    plt.gca().add_artist(legend)


    # ---- TCO PLOT ---- #
    plt.subplot(212)
    plt.plot(tco_df)

    legend_tco = plt.legend(['OPEX_BEV = ' + str(round(opex_raw_list[0], 3)) + ' € / km',
                            'OPEX_FCEV = ' + str(round(opex_raw_list[1], 3)) + ' € / km',
                            'OPEX_PHEV = ' + str(round(opex_raw_list[2], 3)) + ' € / km',
                            'OPEX_ICEV = ' + str(round(opex_raw_list[3], 3)) + ' € / km'], loc='lower right')
    plt.title('Break Even Points Costs')
    plt.xlabel('Distance [km]')
    plt.ylabel('Total Costs [€]')
    plt.xticks(x_ranges)
    plt.grid(True)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    plt.show()


if __name__ == '__main__':
    with open('../results/json/result_all.json') as f:
        data_all = json.load(f)
    break_calc(data_all)

else:
    with open('results/json/result_all.json') as f:
        data_all = json.load(f)
