# ###########################################################
# Default Data
# ###########################################################               Frage: PHEV: batt und synth?? wenn ja alles gut, sonst überprüfen

# FE = Fuel Economy (km/l) ---------------- var             #
# E_el = Electric Energy Use (gCO_2 / kWh)- var             #
#
#
# C3 = Well to tank eff. (kWh / l) -------- var             #
#
# C5 = Fuel Factor 5 (gGHG / l) ----------- var             #
#
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
#

import pandas as pd

# TODO: * Check welche default_vals immer gleich -> doppelung rausnehmen
#       * boolean Checkbox und vehicle bei test! kommt von django

vehicle = 'BEV'
booleanCheckbox = 1



def default_general():              # Hier alle werte die bei allen klassen und propTypes gleich bleiben
    default_val = pd.DataFrame({'vars': ['C3_batt', 'C3_h2', 'C3_synth', 'E_elGer','C5_icev', 'C5_empty', 'cd', 'cd_empty', 'E_elCh', 'L', 'D', 'C_fuelH2', 'C_fuelEl', 'C_fuelSynth', 'r', 'C_batt', 'C_fc'],  # Hier alle var Vals (Ranges)
                                'min': [1.0, 1.0, 1.0, 400.0, 8000.0, 0.0, 45.0, 0.0, 700.0, 13.0, 10000.0, 0.0, 0.0, 0.0, 0.0, 150.0, 0.0],
                                'max': [1.1, 1.923, 2.273, 650, 9000, 0, 60, 0.0, 800, 20, 20000, 0, 0, 0, 3, 200, 0]
                                })
    default_val = default_val.set_index('vars')
    return default_val

def changed_general():
    changed_vals = default_general()

    # TODO: Hier update durch user Input

    changed_vals = changed_vals.set_index('vars')
    return changed_vals


def emptys():
    empty_vals = pd.DataFrame({'vars': ['C5_empty', 'cd_empty', 'P_battEmpty', 'E_battEmpty', 'P_fcEmpty', 'S_renEmpty'],
                                # Hier alle var Vals (Ranges)
                                'min': [],
                                'max': []
                                })
    empty_vals = empty_vals.set_index('vars')
    return empty_vals


# COMPACT
def default_compact(): # mist!? cd muss wählbarer fixwert sein. ohne mit LHS verrechnet zu werden -> cd und alle einfachwert values in extra df!? TODO: min - max werte festlegen,
    default_val = pd.DataFrame({'vars':['FE_batt','FE_h2','FE_synth','P_batt', 'P_battEmpty','E_batt', 'E_battEmpty', 'P_fc', 'P_fcEmpty', 'S_renBig',
                                         'S_renSmall', 'S_renEmpty'],  # Hier alle var Vals (Ranges)
                                'min':[90.0, 43.0, 28.0, 0.0, 0.0, 30.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'max':[95.0, 48.0, 33.0, 0.0, 0.0, 80.0, 0.0, 0.0, 0.0, 0, 0, 0.0]
                                })
    default_val = default_val.set_index('vars')
    # füge default_general und default_compact(class) zusammen
    return default_val

def changed_compact():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_compact()
    # Subsidization Renewables Yes / No             #TODO: DEFAULT darf nicht veränderbar sein. Boolean Checkbox aus DJANGO
    if booleanCheckbox == 1 and (
            vehicle == "BEV" or vehicle == "FCEV"):  # Wenn S_ren selected, set S_ren -- > Für boolean muss get_val von checkbox hin !!!
        changed_vals.iat[changed_vals.index.get_loc('S_renBig'), changed_vals.columns.get_loc('max')] = 4000
    elif booleanCheckbox == 1 and (vehicle == "PHEV"):
        changed_vals.iat[changed_vals.index.get_loc('S_renSmall'), changed_vals.columns.get_loc('max')] = 3000
    else:
        pass
    return changed_vals


# SUV
def default_suv(): # muss noch angepasst werden TODO: Werte anpassen für suv
    default_val = pd.DataFrame({'vars':['FE_batt','FE_h2','FE_synth','P_batt', 'P_battEmpty','E_batt', 'E_battEmpty', 'P_fc', 'P_fcEmpty', 'S_renBig',
                                         'S_renSmall', 'S_renEmpty'],  # Hier alle var Vals (Ranges)
                                'min':[90.0, 43.0, 28.0, 0.0, 0.0, 30.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'max':[95.0, 48.0, 33.0, 0.0, 0.0, 80.0, 0.0, 0.0, 0.0, 0, 0, 0.0]
                                })
    default_val = default_val.set_index('vars')
    return default_val

def changed_suv():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_suv()
    # Subsidization Renewables Yes / No             #TODO: DEFAULT darf nicht veränderbar sein. Boolean Checkbox aus DJANGO
    if booleanCheckbox == 1 and (
            vehicle == "BEV" or vehicle == "FCEV"):  # Wenn S_ren selected, set S_ren -- > Für boolean muss get_val von checkbox hin !!!
        changed_vals.iat[changed_vals.index.get_loc('S_renBig'), changed_vals.columns.get_loc('max')] = 4000
    elif booleanCheckbox == 1 and (vehicle == "PHEV"):
        changed_vals.iat[changed_vals.index.get_loc('S_renSmall'), changed_vals.columns.get_loc('max')] = 3000
    else:
        pass
    return changed_vals


# LDV
def default_ldv(): # Werte müssen noch angepasst werden TODO: Werte anpassen
    default_val = pd.DataFrame({'vars':['FE_batt','FE_h2','FE_synth','P_batt', 'P_battEmpty','E_batt', 'E_battEmpty', 'P_fc', 'P_fcEmpty', 'S_renBig',
                                         'S_renSmall', 'S_renEmpty'],  # Hier alle var Vals (Ranges)
                                'min':[90.0, 43.0, 28.0, 0.0, 0.0, 30.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                'max':[95.0, 48.0, 33.0, 0.0, 0.0, 80.0, 0.0, 0.0, 0.0, 0, 0, 0.0]
                                })
    default_val = default_val.set_index('vars')
    return default_val


def changed_ldv():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_ldv()
    # Subsidization Renewables Yes / No             #TODO: DEFAULT darf nicht veränderbar sein. Boolean Checkbox aus DJANGO
    if booleanCheckbox == 1 and (
            vehicle == "BEV" or vehicle == "FCEV"):  # Wenn S_ren selected, set S_ren -- > Für boolean muss get_val von checkbox hin !!!
        changed_vals.iat[changed_vals.index.get_loc('S_renBig'), changed_vals.columns.get_loc('max')] = 4000
    elif booleanCheckbox == 1 and (vehicle == "PHEV"):
        changed_vals.iat[changed_vals.index.get_loc('S_renSmall'), changed_vals.columns.get_loc('max')] = 3000
    else:
        pass
    return changed_vals


def constant_vals():                        # constanten wie Energiedichte TODO: alle Konstanten eintragen
    constants = pd.DataFrame({'energy_densH2':33.33, 'energy_densSynth':12})  # kWh/l!! Druck benötigt??
    constants = constants.set_index('vars')
    return constants


# get default values for compact cars TODO: in get Variables einfügen
# HIER: spezifische Werte für jeweils klasse und propType

cc_bev =    changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty', 'S_renBig'], axis='rows') # must stay here for LHS-Dimension
#xc_bev =    gin.x_vals().loc['compact(bev)']
cg_bev = changed_general().reindex([])
range_vals = pd.concat([cc_bev, gin.changed_general()])   # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS

cc_fcev = gin.changed_compact().reindex(['FE_h2', 'P_batt', 'S_renBig'], axis='rows')
cc_phev = gin.changed_compact().reindex(['FE_batt', 'FE_synth', 'cd', 'E_elGer', 'C5_icev', 'C5_empty', 'cd', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt', 'S_renSmall'], axis='rows')
cc_icev = gin.changed_compact().reindex(['C3_synth','FE_synth', 'E_elGer', 'C5_icev','E_elCh', 'L', 'D', 'C_fuelSynth', 'r', 'S_renEmpty'])

cs_bev = gin.changed_suv().reindex(['C3_batt', 'FE_batt', 'E_elGer', 'C5_empty', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt','S_renBig'], axis='rows') # add energy density w and all X...
cs_fcev = gin.changed_suv().reindex(['C3_h2', 'FE_h2', 'E_elGer', 'C5_empty', 'E_elCh', 'P_batt', 'L', 'D', 'C_fuelH2', 'r', 'C_batt','S_renBig'], axis='rows')
cs_phev = gin.changed_suv().reindex(['C3_batt', 'FE_batt', 'C3_synth', 'FE_synth', 'cd', 'E_elGer', 'C5_icev', 'C5_empty', 'cd', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt', 'S_renSmall'], axis='rows')
cs_icev = gin.changed_suv().reindex(['C3_synth','FE_synth', 'E_elGer', 'C5_icev','E_elCh', 'L', 'D', 'C_fuelSynth', 'r', 'S_renEmpty'])

cl_bev = gin.changed_ldv().reindex(['C3_batt', 'FE_batt', 'E_elGer', 'C5_empty', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt','S_renBig'], axis='rows') # add energy density w and all X...
cl_fcev = gin.changed_ldv().reindex(['C3_h2', 'FE_h2', 'E_elGer', 'C5_empty', 'E_elCh', 'P_batt', 'L', 'D', 'C_fuelH2', 'r', 'C_batt','S_renBig'], axis='rows')
cl_phev = gin.changed_ldv().reindex(['C3_batt', 'FE_batt', 'C3_synth', 'FE_synth', 'cd', 'E_elGer', 'C5_icev', 'C5_empty', 'cd', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt', 'S_renSmall'], axis='rows')
cl_icev = gin.changed_ldv().reindex(['C3_synth','FE_synth', 'E_elGer', 'C5_icev','E_elCh', 'L', 'D', 'C_fuelSynth', 'r', 'S_renEmpty'])


# C3 = default_compact().('c3_batt')



# def c_vals():           # fuel cycle -
#     fuel_cycle_default = pd.DataFrame({'Class':['compact(bev)','suv(bev)','ldv(bev)','compact(fcev)','suv(fcev)','ldv(fcev)','compact(phev)','suv(phev)','ldv(phev)','compact(icev)','suv(icev)','ldv(icev)'],
#                                        'C3':[35.25, 50.30, 50.30, 35.25, 50.30, 50.30, 42.39, 59.38, 59.38, 58.76, 80.51, 80.51],
#                                        '':[]
#                                        })


# ############################################ #
# Following Values stay unchanged - fix values #
# ############################################ #
def x_vals():           # vehicle cycle - alles fixwerte
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

                                          'C_main':[571, 648.5, 648.5, 570.8, 648.5, 648.5, 680.5, 771, 771, 790, 893.5, 893.5]
                                        })
    vehicle_cycle_default = vehicle_cycle_default.set_index('Class')
    return vehicle_cycle_default


def spec_vals():           # specific vehicle vals - alles fixwerte
    spec_vals_default = pd.DataFrame({'Class':['compact(bev)','suv(bev)','ldv(bev)','compact(fcev)','suv(fcev)','ldv(fcev)','compact(phev)','suv(phev)','ldv(phev)','compact(icev)','suv(icev)','ldv(icev)'],
                                          'm_curb':[1395, 1943, 2100.5, 1395, 1943, 2100.5, 1395, 1943, 2100.5, 1395, 1943, 2100.5], # gemittelte gewichte (recherchiert)

                                          'C_msrp':[1.140, 1.471, 1.471, 1.124, 1.455, 1.455, 1.656, 2.219, 2.219, 1.716, 2.301, 2.301],

                                          'P_battSet':[0.0, 0.0, 0.0, x, x, x, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

                                          'E_battSet':[x, x, x, 0.0, 0.0, 0.0, x, x, x, 0.0, 0.0, 0.0],

                                          'P_fcSet':[0.0, 0.0, 0.0, x, x, x, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

                                          'C_battSet':[x, x, x, x, x, x, x, x, x, 0.0, 0.0, 0.0],

                                          'C_fcSet':[0.0, 0.0, 0.0, x, x, x, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

                                          'CF_Pbatt':[0.0, 0.0, 0.0, x, x, x, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                                        })
    spec_vals_default = spec_vals_default.set_index('Class')
    return spec_vals_default
