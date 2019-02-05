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



var_get = {'Bounderies': ['min', 'max'],  # 'Dictionary' -> Values have to be set from user or default
           'FE':            [val_min, val_max],
           'E_el':          [val_min, val_max],
           'C2':            [val_min, val_max],
           'C3':            [val_min, val_max],
           'C5':            [val_min, val_max],
           'cd':            [val_min, val_max],
           'P_batt':        [val_min, val_max],
           'E_batt':        [val_min, val_max],
           'P_fc':          [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           'var5': [val_min, val_max],
           }

