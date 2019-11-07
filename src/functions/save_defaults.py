# ###########################################################
# SAVE DEFAULT TO CSV
# ###########################################################

# FE = Fuel Economy (km/l) ---------------- var             #
# Em_el = Electric Energy Use (gCO_2 / kWh) var             #
# C3 = Well to tank eff. (kWh / l) -------- var             #
# C5 = Fuel Factor Combustion (gGHG / l) -- var             #
# cs = charge sust. mode (%) -------------- fix (fct)
# cd = charge deplet. mode (%) ------------ var             #
# m_scal = scaling mass (kg) -------------- fix (fct)
# P_batt = Power of Power Batt (kW) ------- var             #
# E_batt = Energy of Energy Batt (kWh) ---- var             #
# P_fc = Fuel Cell Power (Pnenn (kW) ------ var             #
# X2 = Fixed Parts Scaling (gGHG) --------- fix
# X3 = Fixed Parts Energy (kWh) ----------- fix
# X4 - X12                      ----------- fix
# m_curb = avarage curbweight ------------- fix
# r = discount rate ()
# C_batt = Cost Battery
# C_main = maintenance costs


import pandas as pd
import os

vehicle = 'BEV'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def default_general():              # All values that stay the same in all classes and prop_types
    default_val = pd.DataFrame({'vars': ['C3_batt', 'C3_h2', 'C3_synth', 'Em_elFC', 'C5_icev', 'C5_empty', 'Em_elVC',
                                         'cd', 'cd_empty', 'Em_elBatt', 'L', 'D', 'C_fuelH2', 'C_fuelEl', 'C_fuelSynth',
                                         'r', 'C_batt', 'C_battEmpty', 'C_fc', 'C_fcEmpty'],

                                'min': [81.23, 56.43, 41.04, 450.0, 0.0, 0.0, 575,
                                        50, 0.0, 723, 10.8, 12000, 8.84, 0.26, 3.14,
                                        1.26, 127.0, 0.0, 83.0, 0.0],                 # CURRENT !
                                'max': [89.78, 62.37, 45.36, 500, 0.0, 0.0, 625,
                                        80, 0.0, 800, 13.2, 18000, 9.77, 0.29, 3.47,
                                        1.54, 176, 0.0, 225.0, 0.0]


                                # 'min': [81.23, 56.43, 41.04, 450.0, 0.0, 0.0, 575,
                                #        50, 0.0, 723, 15, 20000, 8.84, 0.26, 3.14,
                                #        1.26, 127.0, 0.0, 83.0, 0.0],                     # CURRENT High L + D
                                # 'max': [89.78, 62.37, 45.36, 500, 0.0, 0.0, 625,
                                #        80, 0.0, 800, 20, 30000, 9.77, 0.29, 3.47,
                                #        1.54, 176, 0.0, 225.0, 0.0]


                                # 'min': [225, 56.43, 41.04, 450.0, 0.0, 0.0, 450,
                                #         50, 0.0, 450, 10.8, 12000, 8.84, 0.26, 3.14,
                                #         1.26, 127.0, 0.0, 83.0, 0.0],                       # Autarchy
                                # 'max': [300, 62.37, 45.36, 500, 0.0, 0.0, 500,
                                #         80, 0.0, 450, 13.2, 18000, 9.77, 0.29, 3.47,
                                #         1.54, 176, 0.0, 225.0, 0.0]

                                # 'min': [81.23, 56.43, 41.04, 311.0, 0.0, 0.0, 300,
                                #         60, 0.0, 311, 10.8, 12000, 4.55, 0.63, 1.1,
                                #         1.26, 70.0, 0.0, 32.0, 0.0],
                                #                                                             # Geo Shift!
                                # 'max': [89.78, 62.37, 45.36, 381, 0.0, 0.0, 600,
                                #         90, 0.0, 381, 13.2, 18000, 8.72, 0.77, 2.6,
                                #         1.54, 80, 0.0, 53.0, 0.0]

                                # 'min': [81.23,  56.43,   41.04,  80.0, 0.0, 0.0, 90,
                                #         70, 0.0,   120, 10.8,  12000,  2.73, 0.9, 0.7,
                                #         0.8,  58.0, 0.0,   28.0,  0.0],
                                #                                                             # 2050!
                                # 'max': [89.78,  62.37,   45.36,   170,   0.0,   0.0, 190,
                                #         90, 0.0,   200,   13.2,    16000,  7.05,  1.0, 1.8,
                                #         1.2,  71,  0.0,   53.0,  0.0]


                                # 'min': [81.23, 56.43, 41.04, 311.0, 0.0, 0.0, 300,
                                #        60, 0.0, 500, 10.8, 12000, 4.55, 0.63, 1.1,
                                #        1.26, 62.0, 0.0, 32.0, 0.0],
                                #                                                           # 2030 !
                                # 'max': [89.78, 62.37, 45.36, 381, 0.0, 0.0, 600,
                                #        90, 0.0, 600, 13.2, 18000, 8.72, 0.77, 2.6,
                                #        1.54, 75, 0.0, 53.0, 0.0]


                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_general():              # Calculation is getting Input from here ('changed')
    changed_vals = default_general()

    return changed_vals


# COMPACT
def default_compact():  #  TODO: min - max werte festlegen
    default_val = pd.DataFrame({'vars': ['FE_batt', 'FE_h2', 'FE_synth', 'P_batt', 'P_battEmpty', 'E_batt', 'E_battPHEV',
                                        'E_battEmpty', 'E_battEmptyPHEV', 'P_fc', 'P_fcEmpty', 's_ren_big', 's_ren_small',
                                        's_ren_empty', 'c_main_bev', 'c_main_fcev', 'c_main_phev', 'c_main_icev'],

                                'min': [17.28, 0.9, 6.03, 36.0, 0.0, 39.6, 7.8,
                                        0.0, 0.0, 102.6, 0.0, 0.0, 0.0,
                                        0.0, 0.0351, 0.0423, 0.0414, 0.0423],
                                'max': [21.12, 1.1, 7.37, 44.0, 0.0, 48.4, 9.68,  # CURRENT
                                        0.0, 0.0, 125.4, 0.0, 0, 0,
                                        0.0, 0.0429, 0.0473, 0.0506, 0.0517]


                                # 'min': [17.28, 0.9, 6.03, 36.0, 0.0, 39.6, 7.8,
                                #         0.0, 0.0, 102.6, 0.0, 0.0, 0.0,
                                #         0.0, 0.0351, 0.0423, 0.0414, 0.0423],
                                # 'max': [21.12, 1.1, 7.37, 44.0, 0.0, 48.4, 9.68,            # Autarchy
                                #         0.0, 0.0, 125.4, 0.0, 0, 0,
                                #         0.0, 0.0429, 0.0473, 0.0506, 0.0517]

                                # 'min': [16.7, 0.85, 5, 40.0, 0.0, 50, 10,
                                #        0.0, 0.0, 102.6, 0.0, 0.0, 0.0,
                                #        0.0, 0.0351, 0.0423, 0.0414, 0.0423],            # Geo Shift
                                # 'max': [20.35, 1.05, 6.5, 77.0, 0.0, 90, 20,
                                #        0.0, 0.0, 125.4, 0.0, 0, 0,
                                #        0.0, 0.0429, 0.0473, 0.0506, 0.0517]

                                # 'min': [14.4, 0.77, 4.1, 50.0, 0.0, 60, 15,
                                #         0.0, 0.0, 114, 0.0, 0.0, 0.0,
                                #         0.0, 0.0351, 0.0423, 0.0414, 0.0423],           # 2050
                                # 'max': [17.6, 0.94, 5.1, 80.0, 0.0, 100, 25,
                                #         0.0, 0.0, 136.8, 0.0, 0, 0,
                                #         0.0, 0.0429, 0.0473, 0.0506, 0.0517]

                                # 'min': [16.7, 0.85, 5, 40.0, 0.0, 50, 10,
                                #        0.0, 0.0, 102.6, 0.0, 0.0, 0.0,
                                #        0.0, 0.0351, 0.0423, 0.0414, 0.0423],             # 2030
                                # 'max': [20.35, 1.05, 6.5, 77.0, 0.0, 90, 20,
                                #        0.0, 0.0, 125.4, 0.0, 0, 0,
                                #        0.0, 0.0429, 0.0473, 0.0506, 0.0517]


                                # 'min': [16.7, 0.9, 5, 40.0, 0.0, 50, 10,
                                #         0.0, 0.0, 102.6, 0.0, 0.0, 0.0,
                                #         0.0, 550, 550, 660, 770],
                                # 'max': [20.35, 1.1, 6.5, 77.0, 0.0, 90, 20,           # SAVE 2030 (C_main)
                                #         0.0, 0.0, 125.4, 0.0, 0, 0,
                                #         0.0, 571, 570, 680, 790]

                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_compact():
    changed_vals = default_compact()
    return changed_vals


# SUV
def default_suv():  # TODO: Werte anpassen für suv
    default_val = pd.DataFrame({'vars': ['FE_batt', 'FE_h2', 'FE_synth', 'P_batt', 'P_battEmpty', 'E_batt', 'E_battPHEV',
                                         'E_battEmpty', 'E_battEmptyPHEV', 'P_fc', 'P_fcEmpty', 's_ren_big', 's_ren_small',
                                         's_ren_empty', 'c_main_bev', 'c_main_fcev', 'c_main_phev', 'c_main_icev'],
                                'min': [18, 1, 9.2, 36.0, 0.0, 58.23, 11.7,
                                        0.0, 0.0, 84.6, 0.0, 0.0, 0.0,
                                        0.0, 0.0558, 0.0612, 0.0657, 0.0675],
                                'max': [22, 1.2, 11.2, 44.0, 0.0, 71.17, 14.3,
                                        0.0, 0.0, 103.4, 0.0, 0.0, 0.0,
                                        0.0, 0.0682, 0.0748, 0.0803, 0.0825]


                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_suv():
    changed_vals = default_suv()

    return changed_vals


# LDV
def default_ldv():  # TODO: Werte anpassen
    default_val = pd.DataFrame({'vars': ['FE_batt', 'FE_h2', 'FE_synth', 'P_batt', 'P_battEmpty', 'E_batt', 'E_battPHEV',
                                         'E_battEmpty', 'E_battEmptyPHEV', 'P_fc', 'P_fcEmpty', 's_ren_big', 's_ren_small',
                                         's_ren_empty', 'c_main_bev', 'c_main_fcev', 'c_main_phev', 'c_main_icev'],
                                'min': [19.08, 1, 9.54, 36.0, 0.0, 35.0, 12.24,
                                        0.0, 0.0, 24.0, 0.0, 0.0, 0.0,
                                        0.0, 0.045, 0.0504, 0.0531, 0.0549],                # CURRENT
                                'max': [23.32, 1.2, 11.66, 44.0, 0.0, 41.8, 14.96,
                                        0.0, 0.0, 28.6, 0.0, 0.0, 0.0,
                                        0.0, 0.055, 0.0616, 0.0649, 0.0671]



                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_ldv():
    changed_vals = default_ldv()
    return changed_vals


# ############################################ #
# Following Values stay unchanged - fix values #
# ############################################ #

# Changing values 'Future Scenario': X7, X10
# Constant Values 'Future Scenario': X8, X11

def x_vals():           # vehicle cycle - all values are fix set
    vehicle_cycle_default = pd.DataFrame({'Class': ['compact(bev)',  'suv(bev)',  'ldv(bev)',
                                                    'compact(fcev)', 'suv(fcev)', 'ldv(fcev)',
                                                    'compact(phev)', 'suv(phev)', 'ldv(phev)',
                                                    'compact(icev)', 'suv(icev)', 'ldv(icev)'],
                                          'X1': [35.25, 50.30, 50.30,       # Fixed Parts Mass (kg)
                                                 35.25, 50.30, 50.30,
                                                 42.39, 59.38, 59.38,
                                                 58.76, 80.51, 80.51],

                                          'X2': [1140, 1471, 1471,       # Emissions Fixed Parts (gGHG)
                                                 1124, 1455, 1455,
                                                 1656, 2219, 2219,
                                                 1716, 2301, 2301],

                                          'X3': [1141, 1246, 1246,       # Energy Need Fixed Parts (kWh)
                                                 1074, 1179, 1179,
                                                 1174, 1294, 1294,
                                                 1120, 1244, 1244],

                                          'X4': [2.40, 2.38, 2.37,       # Scaling mass Emissions (gGHG/kg)
                                                2.41, 2.39, 2.38,
                                                2.41, 2.40, 2.40,
                                                2.40, 2.36, 2.38],

                                          'X5': [2.41, 2.39, 2.40,       # Scaling mass Energy Need (kWh/kg)
                                                2.43, 2.42, 2.43,
                                                2.38, 2.37, 2.39,
                                                2.25, 2.25, 2.24],

                                          'X6': [0, 0, 0,               # Power Battery Mass (kg/kW)
                                                 1.25, 1.25, 1.25,
                                                 0, 0, 0,
                                                 0, 0, 0],

                                          'X7': [0, 0, 0,               # Power Battery Emissions (gGHG/kW)
                                                 5.01, 5.01, 5.01,
                                                 0, 0, 0,
                                                 0, 0, 0],  # PRÜFEN

                                          'X8': [0, 0, 0,               # Power Battery Energy Need (kWh/kW)
                                                 6.22, 6.22, 6.22,
                                                 0, 0, 0,
                                                 0, 0, 0], # PRÜFEN

                                          'X9': [7.52, 7.52, 7.52,      # Energy Battery Mass (kg/kWh)
                                                 0, 0, 0,
                                                 9.43, 9.43, 9.43,
                                                 0, 0, 0],

                                          'X10': [24.50, 24.50, 24.50,  # Energy Battery Emissions (gGHG/kWh)
                                                  0, 0, 0,
                                                  33.62, 33.62, 33.62,
                                                  0, 0, 0],

                                          'X11': [250, 250, 250,        # Energy Battery Energy Need (kWh/kWh)
                                                  0, 0, 0,
                                                  250, 250, 250,
                                                  0, 0, 0],

                                          'X12': [0, 0, 0,              # Fuel Cell Mass (kg/kW)
                                                  5.0, 5.0, 5.0,
                                                  0, 0, 0,
                                                  0, 0, 0],

                                          'X13': [0, 0, 0,              # Fuel Cell Emissions (gGHG/kW)
                                                  56.48, 56.48, 56.48,
                                                  0, 0, 0,
                                                  0, 0, 0],

                                          'X14': [0, 0, 0,              # Fuel Cell Energy Need (kWh/kW)
                                                  40.89, 40.89, 40.89,
                                                  0, 0, 0,
                                                  0, 0, 0]
                                        })


    vehicle_cycle_default = vehicle_cycle_default.set_index('Class')
    return vehicle_cycle_default


def spec_vals():           # all values are fix set
    spec_vals_default = pd.DataFrame({'Class': ['compact(bev)',  'suv(bev)',  'ldv(bev)',
                                                'compact(fcev)', 'suv(fcev)', 'ldv(fcev)',
                                                'compact(phev)', 'suv(phev)', 'ldv(phev)',
                                                'compact(icev)', 'suv(icev)', 'ldv(icev)'
                                                ],
                                          'm_curb':     [1499, 2184, 1932,
                                                         1657, 1950, 3000,
                                                         1795, 1725, 2500,
                                                         1375, 1943, 2035],  # averaged weights (researched)

                                        # --------------- Vehicle Price MSRP (€) --------------- #
                                          'C_msrp':     [36900, 73096, 48446,
                                                         78600, 68600, 65000,
                                                         30366, 36395, 35000,   # Current
                                                         24302, 39037, 21564],

                                          # 'C_msrp':     [36900, 73096, 48446,
                                          #                40000, 68600, 65000,
                                          #                30366, 36395, 35000,   # Current Cheap FCEV
                                          #                24302, 39037, 21564],
                                          #
                                          # 'C_msrp':     [30900, 73096, 48446,
                                          #                53600, 68600, 65000,
                                          #                27366, 36395, 35000,       # 2030 (only compact changed)
                                          #                24302, 39037, 21564],

                                          # 'C_msrp':     [26900, 73096, 48446,
                                          #                43600, 68600, 65000,
                                          #                24366, 36395, 35000,  # 2050 (only compact changed)
                                          #                24302, 39037, 21564],

                                      # --------------- Standard Power of Power Battery (kW)--------------- #
                                              'P_battSet': [0.0, 0.0, 0.0,
                                                             40,  40,  40,      # Current
                                                            0.0, 0.0, 0.0,
                                                            0.0, 0.0, 0.0],

                                              # 'P_battSet': [0.0, 0.0, 0.0,
                                              #               55, 55, 55,         # 2030
                                              #               0.0, 0.0, 0.0,
                                              #               0.0, 0.0, 0.0],

                                              # 'P_battSet': [0.0, 0.0, 0.0,
                                              #               65, 65, 65,         # 2050
                                              #               0.0, 0.0, 0.0,
                                              #               0.0, 0.0, 0.0],

                                      # --------------- Standard Capacity of Energy Battery (kWh) --------------- #
                                              'E_battSet': [44.0, 64.7,   38,
                                                             0.0,  0.0,  0.0,    # Current
                                                             8.8,   13, 13.6,
                                                             0.0,  0.0,  0.0],

                                              # 'E_battSet': [70.0, 90, 70,
                                              #               0.0, 0.0, 0.0,      # 2030
                                              #               15, 20, 15,
                                              #               0.0, 0.0, 0.0],

                                              # 'E_battSet': [80.0, 100, 80,
                                              #               0.0, 0.0, 0.0,      # 2050
                                              #               20, 25, 20,
                                              #               0.0, 0.0, 0.0],

                                      # --------------- Standard Power of Fuel Cell (kW) --------------- #
                                              'P_fcSet': [0.0, 0.0, 0.0,
                                                          114,  94,  26,        # Current
                                                          0.0, 0.0, 0.0,
                                                          0.0, 0.0, 0.0],

                                              # 'P_fcSet': [0.0, 0.0, 0.0,
                                              #             114, 114, 114,          # 2030
                                              #             0.0, 0.0, 0.0,
                                              #             0.0, 0.0, 0.0],

                                              # 'P_fcSet': [0.0, 0.0, 0.0,
                                              #             125, 125, 125,          # 2050
                                              #             0.0, 0.0, 0.0,
                                              #             0.0, 0.0, 0.0],

                                      # --------------- Standard Price of Battery (€/kWh) --------------- #
                                              'C_battSet': [150, 150, 150,
                                                            150, 150, 150,      # Current
                                                            150, 150, 150,
                                                            0.0, 0.0, 0.0],

                                              # 'C_battSet': [68.5,68.5,68.5,
                                              #               68.5,68.5,68.5,     # 2030
                                              #               68.5,68.5,68.5,
                                              #               0.0, 0.0, 0.0],

                                              # 'C_battSet': [65, 65, 65,
                                              #               65, 65, 65,      # 2050
                                              #               65, 65, 65,
                                              #               0.0, 0.0, 0.0],

                                      # --------------- Standard Price of Fuel Cell (€/kW) --------------- #
                                              'C_fcSet': [0.0, 0.0, 0.0,
                                                          154,  154,  154,      # Current
                                                          0.0, 0.0, 0.0,
                                                          0.0, 0.0, 0.0],

                                              # 'C_fcSet': [0.0, 0.0, 0.0,
                                              #             42.5,42.5,42.5,  # 2030
                                              #             0.0, 0.0, 0.0,
                                              #             0.0, 0.0, 0.0],

                                              # 'C_fcSet': [0.0, 0.0, 0.0,
                                              #             40.5, 40.5, 40.5,  # 2050
                                              #             0.0, 0.0, 0.0,
                                              #             0.0, 0.0, 0.0],

                                      # --------------- FIX VALUES --------------- #
                                              'CF_Pbatt': [1.0, 1.0, 1.0,       # CONVERSION FAKTOR FOR FCEV Pbatt
                                                           25, 25, 25,
                                                           1.0, 1.0, 1.0,
                                                           1.0, 1.0, 1.0],

                                              'w_h2':  [1.0,  1.0,  1.0,        # Energy Density H2 (kWh(kg)
                                                       33.3, 33.3, 33.3,
                                                        1.0,  1.0,  1.0,
                                                        1.0,  1.0,  1.0],

                                              'w_synth':  [1.0,  1.0,  1.0,     # Energy Density Synthetic Fuels
                                                           1.0,  1.0,  1.0,
                                                          11.6, 11.6, 11.6,
                                                          11.6, 11.6, 11.6]


                                      })
    spec_vals_default = spec_vals_default.set_index('Class')
    return spec_vals_default



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir('../inputfiles/')
default_general().to_csv('_default_general.csv', index='vars', sep=';')
default_compact().to_csv('_default_compact.csv', index='vars', sep=';')
default_suv().to_csv('_default_suv.csv', index='vars', sep=';')
default_ldv().to_csv('_default_ldv.csv', index='vars', sep=';')
x_vals().to_csv('_x_vals.csv', index='Class', sep=';')
spec_vals().to_csv('_spec_vals.csv', index='Class', sep=';')


os.chdir(BASE_DIR)
