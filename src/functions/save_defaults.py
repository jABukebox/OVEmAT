# ###########################################################
# SAVE DEFAULT TO CSV
# ###########################################################


import pandas as pd
import os

# TODO: * boolean Checkbox und vehicle bei test! kommt von django

vehicle = 'BEV'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Todo: reziproken wert ändern

def default_general():              # All values that stay the same in all classes and prop_types
    default_val = pd.DataFrame({'vars': ['C3_batt', 'C3_h2', 'C3_synth', 'Em_elFC', 'C5_icev', 'C5_empty', 'Em_elVC',
                                         'cd', 'cd_empty', 'Em_elBatt', 'L', 'D', 'C_fuelH2', 'C_fuelEl', 'C_fuelSynth',
                                         'r', 'C_batt', 'C_battEmpty', 'C_fc', 'C_fcEmpty'],

                                'min': [93,  50,   42,  400.0, 0.0, 0.0, 550,
                                        50.0, 0.0,   850.0, 15.0,  15000,  8.5, 0.20, 1.3,
                                        1.5,  160.0, 0.0,   30.0,  0.0],

                                'max': [96,  54,   46,   550,   0.0,   0.0, 600,
                                        51.0, 0.0,   900,   20,    30000,  10,  0.50, 1.9,
                                        3.0,  200,  0.0,   60.0,  0.0]
                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_general():              # Calculation is getting Input from here ('changed')
    changed_vals = default_general()

    # TODO: Here update by user Input

    #changed_vals = changed_vals.set_index('vars')          # switch on when changed
    return changed_vals


# COMPACT
def default_compact():  #  TODO: min - max werte festlegen
    default_val = pd.DataFrame({'vars': ['FE_batt', 'FE_h2', 'FE_synth', 'P_batt', 'P_battEmpty', 'E_batt',
                                        'E_battEmpty', 'P_fc', 'P_fcEmpty', 's_ren_big', 's_ren_small',
                                        's_ren_empty'],
                                'min': [15, 1, 3, 30.0, 0.0, 30.0, 0.0, 60.0, 0.0, 0.0, 0.0, 0.0],
                                'max': [17, 1.6, 6, 50.0, 0.0, 50.0, 0.0, 80.0, 0.0, 0, 0, 0.0]
                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_compact():
    changed_vals = default_compact()
    return changed_vals


# SUV
def default_suv():  # TODO: Werte anpassen für suv
    default_val = pd.DataFrame({'vars': ['FE_batt', 'FE_h2', 'FE_synth', 'P_batt', 'P_battEmpty', 'E_batt',
                                         'E_battEmpty', 'P_fc', 'P_fcEmpty', 's_ren_big', 's_ren_small',
                                         's_ren_empty'],
                                'min': [18, 1.3, 6, 40.0, 0.0, 60.0, 0.0, 70.0, 0.0, 0.0, 0.0, 0.0],
                                'max': [23, 2, 13, 60.0, 0.0, 90.0, 0.0, 100.0, 0.0, 0, 0, 0.0]
                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_suv():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_suv()

    return changed_vals


# LDV
def default_ldv():  # TODO: Werte anpassen
    default_val = pd.DataFrame({'vars': ['FE_batt', 'FE_h2', 'FE_synth', 'P_batt', 'P_battEmpty', 'E_batt',
                                         'E_battEmpty', 'P_fc', 'P_fcEmpty', 's_ren_big', 's_ren_small',
                                         's_ren_empty'],
                                'min': [20, 1.5, 8, 50.0, 0.0, 70.0, 0.0, 70.0, 0.0, 0.0, 0.0, 0.0],
                                'max': [25, 2.5, 18, 70.0, 0.0, 100.0, 0.0, 100.0, 0.0, 0, 0, 0.0]
                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_ldv():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_ldv()
    return changed_vals


# ############################################ #
# Following Values stay unchanged - fix values #
# ############################################ #
def x_vals():           # vehicle cycle - all values are fix set
    vehicle_cycle_default = pd.DataFrame({'Class': ['compact(bev)', 'suv(bev)', 'ldv(bev)', 'compact(fcev)',
                                                    'suv(fcev)', 'ldv(fcev)', 'compact(phev)', 'suv(phev)',
                                                    'ldv(phev)', 'compact(icev)', 'suv(icev)', 'ldv(icev)'],
                                          'X1': [35.25, 50.30, 50.30, 35.25, 50.30, 50.30, 42.39, 59.38, 59.38, 58.76,
                                                 80.51, 80.51],

                                          'X2': [1.140, 1.471, 1.471, 1.124, 1.455, 1.455, 1.656, 2.219, 2.219, 1.716,
                                                 2.301, 2.301],

                                          'X3': [1.141, 1.246, 1.246, 1.074, 1.179, 1.179, 1.174, 1.294, 1.294, 1.120,
                                                 1.244, 1.244],

                                          'X4':[2.40, 2.38, 2.37, 2.41, 2.39, 2.38, 2.41, 2.40, 2.40, 2.40, 2.36, 2.38],

                                          'X5':[2.41, 2.39, 2.40, 2.43, 2.42, 2.43, 2.38, 2.37, 2.39, 2.25, 2.25, 2.24],

                                          'X6': [0, 0, 0, 1.25, 1.25, 1.25, 0, 0, 0, 0, 0, 0],

                                          'X7': [0, 0, 0, 5.01, 5.01, 5.01, 0, 0, 0, 0, 0, 0],

                                          'X8': [0, 0, 0, 6.22, 6.22, 6.22, 0, 0, 0, 0, 0, 0],

                                          'X9': [7.52, 7.52, 7.52, 0, 0, 0, 9.43, 9.43, 9.43, 0, 0, 0],

                                          'X10': [24.50, 24.50, 24.50, 0, 0, 0, 33.62, 33.62, 33.62, 0, 0, 0],

                                          'X11': [14.77, 14.77, 14.77, 0, 0, 0, 24.69, 24.69, 24.69, 0, 0, 0],

                                          'X12': [0, 0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 0, 0],

                                          'X13': [0, 0, 0, 56.48, 56.48, 56.48, 0, 0, 0, 0, 0, 0],

                                          'X14': [0, 0, 0, 40.89, 40.89, 40.89, 0, 0, 0, 0, 0, 0],

                                          'C_main': [571, 648.5, 648.5, 570.8, 648.5, 648.5, 680.5, 771, 771, 790,
                                                     893.5, 893.5]
                                        })
    vehicle_cycle_default = vehicle_cycle_default.set_index('Class')
    return vehicle_cycle_default


def spec_vals():           # all values are fix set  TODO: WERTE ERSETZEN / fcev: cf = 1!?
    spec_vals_default = pd.DataFrame({'Class': ['compact(bev)', 'suv(bev)', 'ldv(bev)', 'compact(fcev)', 'suv(fcev)',
                                                'ldv(fcev)', 'compact(phev)', 'suv(phev)', 'ldv(phev)', 'compact(icev)',
                                                'suv(icev)', 'ldv(icev)'],
                                          'm_curb':     [1395, 1943, 2100.5, 1395, 1943, 2100.5, 1395, 1943, 2100.5,
                                                         1395, 1943, 2100.5],  # averaged weights (researched)

                                          'C_msrp':     [33465, 73096, 48446, 79000, 69000, 65000, 30366, 36395, 35000,
                                                         24302, 39037, 21564],

                                          'P_battSet':  [0.0, 0.0, 0.0, 20, 30, 40, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

                                          'E_battSet':  [40, 50, 60, 0.0, 0.0, 0.0, 10, 20, 30, 0.0, 0.0, 0.0],

                                          'P_fcSet':    [0.0, 0.0, 0.0, 40, 50, 60, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

                                          'C_battSet':  [150, 150, 150, 180, 180, 180, 150, 150, 150, 0.0, 0.0, 0.0],

                                          'C_fcSet':    [0.0, 0.0, 0.0, 45, 45, 45, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

                                          'CF_Pbatt':   [1.0, 1.0, 1.0, 25, 25, 25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],

                                          'w_h2':      [1.0, 1.0, 1.0, 33.3, 33.3, 33.3, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],

                                          'w_synth':    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 11.6, 11.6, 11.6, 11.6, 11.6, 11.6]
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


# DB Connection

# conn = psy.connect(
#     database="ovemat_db",
#     user="ovemat",
#     host="localhost",
#     password="ovemat"
# )
# curs = conn.cursor()
#
# out = pd.read_csv('_default_general.csv')
# curs.copy_from(out, '_default_general', null="")
# conn.commit()

os.chdir(BASE_DIR)
