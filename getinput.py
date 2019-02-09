# ###########################################################
# Default Data
# ###########################################################

# FE = Fuel Economy (km/l) ---------------- var             #
# E_el = Electric Energy Use (gCO_2 / kWh)- var             #
# C1 = Fuel Factor 1 (gGHG / km) ---------- ????
# C2 = Fuel Factor 2 (gGHG / km) ---------- var ?           #
# C3 = Fuel Factor 3 (kWh / l) ------------ var             #
# C4 = Fuel Factor 4 (gGHG / km) ---------- ???
# C5 = Fuel Factor 5 (gGHG / l) ----------- var             #
# C6 = Fuel Factor 6 (kWh / l) ------------ fix
# cs = charge sust. mode (%) -------------- fix (f)
# cd = charge deplet. mode (%) ------------ var             #
# m_scal = scaling mass (kg) -------------- fix (f)
# P_batt = Power of Power Batt (kW) ------- var             #
# E_batt = Energy of Energy Batt (kWh) ---- var             #
# P_fc = Fuel Cell Power (Pnenn (kW) ------ var             #
# X2 = Fixed Parts Scaling (gGHG) --------- fix
# X3 = Fixed Parts Energy (kWh) ----------- fix
# X4 - X12                      ----------- fix
# m_curb = avarage curbweight ------------- fix
#

import pandas as pd


def default_general():
    default_val = pd.DataFrame({'Boundaries':['min','max'],  # Hier alle Vals (Var + fix)
                                'C3_batt': [0, 1.1],
                                'FE_batt':[90, 95],
                                'C3_h2': [0, 1.923],
                                'FE_h2': [43, 48],
                                'C3_synth': [0, 2.273],
                                'FE_synth': [28, 33],
                                'E_elGER': [500, 650],
                                'C5':[1600, 2000],
                                'cd':[45,60],
                                'E_elCh':[700, 800],
                                'P_batt':[0, 0],
                                'E_batt':[30, 80],
                                'P_fc': [0, 0],
                                'L':[13, 20],
                                'D':[10000, 20000],
                                'C_fuelH2':[0, 0],
                                'C_fuelEl':[0, 0],
                                'C_fuelSynth':[0, 0],
                                'r':[0, 3],
                                'C_batt':[150, 200],
                                'C_fc':[0, 0],
                                'S_ren':[0, 0]
                                })
    default_val = default_val.set_index('Bounderies')
    return default_val


def x_vals():           # alles fixwerte
    vehicle_cycle_default = pd.DataFrame({'Class':['compact(bev)','suv(bev)','ldv(bev)','compact(fcev)','suv(fcev)','ldv(fcev)','compact(phev)','suv(phev)','ldv(phev)','compact(icev)','suv(icev)','ldv(icev)'],
                                          'X1':[35.25, 50.30, 50.30, 35.25, 50.30, 50.30, 42.39, 59.38, 59.38, 58.76, 80.51, 80.51],

                                          'X2':[1.140, 1.471, 1.471, 1.124, 1.455, 1.455, 1.656, 2.219, 2.219, 1.716, 2.301, 2.301],

                                          'X3':[1.141, 1.246, 1.246, 1.074, 1.179, 1.179, 1.174, 1.294, 1.294, 1.120, 1.244, 1.244],

                                          'X4':[2.40, 2.38, 2.37, 2.41, 2.39, 2.38, 2.41, 2.40, 2.40, 2.40, 2.36, 2.38],

                                          'X5':[2.41, 2.39, 2.40, 2.43, 2.42, 2.43, 2.38, 2.37, 2.39, 2.25, 2.25, 2.24],

                                          'X6':[0, 0, 0, 1.25, 1.25, 1.25, 0, 0, 0, 0, 0, 0],

                                          'X7':[0, 0, 0, 5.01, 5.01, 5.01, 0, 0, 0, 0, 0, 0],

                                          'X8':[0, 0, 0, 6.22, 6.22, 6.22, 0, 0, 0, 0, 0, 0],

                                          'X9':[7.52, 7.52, 7.52, 0, 0, 0, 9.43, 9.43, 9.43, 0, 0, 0],

                                          'X10':[24.50, 24.50, 24.50, 0, 0, 0, 33.62, 33.62, 33.62, 0, 0, 0],

                                          'X11':[14.77, 14.77, 14.77, 0, 0, 0, 24.69, 24.69, 24.69, 0, 0, 0],

                                          'X12':[0, 0, 0, 5.0, 5.0, 5.0, 0, 0, 0, 0, 0, 0],

                                          'X13':[0, 0, 0, 56.48, 56.48, 56.48, 0, 0, 0, 0, 0, 0],

                                          'X14':[0, 0, 0, 40.89, 40.89, 40.89, 0, 0, 0, 0, 0, 0],

                                          'cost_main':[571, 648.5, 648.5, 570.8, 648.5, 648.5, 680.5, 771, 771, 790, 893.5, 893.5],
                                        })
    vehicle_cycle_default = vehicle_cycle_default.set_index('Class')
    return vehicle_cycle_default


