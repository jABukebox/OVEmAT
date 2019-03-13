# ###########################################################
# Data Handling - Get data from CSV and save changed Data
# ###########################################################

# FE = Fuel Economy (km/l) ---------------- var             #
# E_el = Electric Energy Use (gCO_2 / kWh)- var             #
# C3 = Well to tank eff. (kWh / l) -------- var             #
# C5 = Fuel Factor 5 (gGHG / l) ----------- var             #
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


import pandas as pd
import os

# TODO: * Check welche default_vals immer gleich -> doppelung rausnehmen
#       * boolean Checkbox und vehicle bei test! kommt von django

vehicle = 'BEV'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# GENERAL VALUES
def default_general():              # All values that stay the same in all classes and prop_types
    try:
        default_val = pd.read_csv('inputfiles/_default_general.csv', index_col='vars', delimiter=';')
    except:
        default_val = pd.read_csv('inputfiles/_default_general.csv', index_col='vars', delimiter=',')
    return default_val


def changed_general():              # Calculation is getting Input from here ('changed')
    changed_vals = default_general()
    # TODO: Hier update durch user Input
    # changed_vals = changed_vals.set_index('vars')          # switch on when changed
    return changed_vals


# COMPACT
def default_compact():                        # TODO: min - max werte festlegen,
    default_val = pd.read_csv('inputfiles/_default_compact.csv', index_col='vars', delimiter=';')
    return default_val


def changed_compact():
    changed_vals = default_compact()
    return changed_vals


# SUV
def default_suv():  # TODO: Werte anpassen für suv
    default_val = pd.read_csv('inputfiles/_default_suv.csv', index_col='vars', delimiter=';')
    return default_val


def changed_suv():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_suv()
    return changed_vals


# LDV
def default_ldv():  # TODO: Werte anpassen
    default_val = pd.read_csv('inputfiles/_default_ldv.csv', index_col='vars', delimiter=';')
    return default_val


def changed_ldv():                              # TODO: hier müssen auch value changes rein!!
    changed_vals = default_ldv()
    return changed_vals


# ############################################ #
# Following Values stay unchanged - fix values #
# ############################################ #
def x_vals():           # vehicle cycle - all values are fix set
    vehicle_cycle_default = pd.read_csv('inputfiles/_x_vals.csv', index_col='Class', delimiter=';')
    return vehicle_cycle_default


def spec_vals():           # specific vehicle vals - all values are fix set # TODO: WERTE ERSETZEN / fcev: cf = 1!?
    spec_vals_default = pd.read_csv('inputfiles/_spec_vals.csv', index_col='Class', delimiter=';')
    return spec_vals_default


def sub_big():          # Subsidy for BEVs and FCEVs
    s_ren = 4000
    return s_ren


def sub_small():        # Subsidy for PHEVs
    s_ren = 3000
    return s_ren

def fe_cd_x():         # Correction Factor for PHEV in cd mode
    fe_cd = 1.15
    return fe_cd

def fe_cs_x():         # Correction Factor for PHEV in cs mode
    fe_cs = 1.15
    return fe_cs