import numpy as np
import getinput as gin
import pandas as pd

def varFinal():
    propType = ['BEV','FCEV','PHEV','ICEV']
    var_all = []
    for vehicle in range(len(propType)):                                         # Durchlauf jedes propTypes
        gV = getVariables(class_sel, vehicle)                                      # holt die
        lhs_items = 0
        var_array = []

        for r in range(n):                                                       # Anzahl der LHS Durchläufe
            var_list = []                                                        # initiieren var_list: hier sollen pro 'n' alle verrechneten parameter in eine Liste gespeichert werden
            m = 0               # row / zeile
            t = 1               # column / spalte
            for k in range(dimension):                                           # alle Range-Werte mit reihe des LHS multiplizieren
                var_max = gV.iloc[m][t]                                          # bestimmung des max Wertes der eingegebenen Range
                t -= 1
                var_min = gV.iloc[m][t]                                          # bestimmung des min Wertes der eingegebenen Range
                t += 1
                var = (p.item(lhs_items) * (var_max - var_min)) + var_min        # Verrechnung der Variablen mit LHS Ergebnissen in var
                var_list.append(var)                                             # Anhängen der Parameter an liste
                lhs_items += 1
                m += 1
            var_array.append(var_list)                                           # Var_list gets appended to var_array
        var_array = np.around(var_array, decimals=4)                             # round numbers
    var_all.append(var_array)                                                    # Abspeicherung aller verrechneten
    print(var_all)                                                               # propType Variablen
    return var_all


def getVariables(class_sel, vehicle):
    if class_sel == 1:                                  # compact car #
        if vehicle == 0:    # BEV
            cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'S_renBig'], axis='rows')
              # add energy density w and all X...
            range_vals = pd.concat([cc_bev, gen_def])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS TODO: gin.default_general() vor varFinal

        elif vehicle == 1: # FCEV
            cc_fcev = gin.changed_compact().reindex(
                ['FE_h2', 'P_batt', 'S_renBig'], axis='rows')
            range_vals = pd.concat([cc_fcev, gin.changed_general()])

        elif vehicle == 2:  # PHEV
            cc_phev = gin.changed_compact().reindex(
                ['C3_batt', 'FE_batt', 'C3_synth', 'FE_synth', 'cd', 'Em_elFC', 'C5_icev', 'C5_empty', 'cd', 'Em_elBatt',
                 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt', 'S_renSmall'], axis='rows')

        elif vehicle == 3:  # ICEV
            default_vals = pd.DataFrame({''})

        else:
            pass

    elif class_sel == 2:                              # midsize SUV #
        if vehicle == 0:    # BEV
            default_vals = pd.DataFrame({''})   # Hier alle Vals (Var + fix)

        elif vehicle == 1:  # FCEV
            default_vals = pd.DataFrame({''})

        elif vehicle == 2:  # PHEV
            default_vals = pd.DataFrame({''})

        elif vehicle == 3:  # ICEV
            default_vals = pd.DataFrame({''})

        else:
            pass

    elif class_sel == 3:                              # Light Duty Vehicle #
        if vehicle == 0:    # BEV
            default_vals = pd.DataFrame({''})   # Hier alle Vals (Var + fix)

        elif vehicle == 1:  # FCEV
            default_vals = pd.DataFrame({''})

        elif vehicle == 2:  # PHEV
            default_vals = pd.DataFrame({''})

        elif vehicle == 3:  # ICEV
            default_vals = pd.DataFrame({''})

        else:
            pass

        dimension = ((default_vals.size) / 2)  # Length of Variable list

    else:
        print('Wrong Input! \n')
        vehClassSel()                               # Erneute Eingabe der Fahrzeugklasse

    return range_vals


# import numpy as np

# dimension = 10
# n = 5

# def varFinal():
#     propType = ['BEV','FCEV','PHEV','ICEV']
#     var_array = []
#     for vehicle in range(len(propType)):
#         print('vehicle no:' + str(vehicle))
#         var_list = []
#         for r in range(n):      # Anzahl der Durchläufe
#             a = r
#             var_list.append(a)
#         var_array.append(var_list)  # Var_list gets appended to var_array
#
#     print('\n')
#     print(var_array)
#     return var_array
#
#
# #print(varFinal)
#
# varFinal()