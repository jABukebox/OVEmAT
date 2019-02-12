import numpy as np
import getinput as gin
import pandas as pd

def varFinal():
    propType = ['BEV','FCEV','PHEV','ICEV']
    var_all = []
    for vehicle in range(len(propType)):                                         # Durchlauf jedes propTypes
        gV = getVariables(veh_sel, vehicle)                                      # holt die
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
            X_vals = list(gin.x_vals().loc['compact(bev)'])
            var_list.extend(X_vals)  # TODO: append X_vals, spec_fals & constant_vals ABER sehr rechenaufwändig .. lieber bei auslesen hinzufügen
            var_array.append(var_list)                                           # Var_list gets appended to var_array
        var_array = np.around(var_array, decimals=4)                             # round numbers
    var_all.append(var_array)                                                    # Abspeicherung aller verrechneten
    print(var_all)                                                               # propType Variablen
    return var_all


def getVariables(veh_sel, vehicle):
    #propType = ['FCEV', 'BEV', 'ICEV', 'PHEV']
    if veh_sel==1:                                  # compact car #
        if vehicle == 'BEV':
            # max = gin.default_compact().reindex(index=['C3_batt', 'FE_batt', 'E_elGer', 'C5', 'cd', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r','C_batt'], columns=['max'])
            # min = gin.default_compact().reindex(
            #     index=['C3_batt', 'FE_batt', 'E_elGER', 'C5', 'cd', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r',
            #            'C_batt'], columns=['min'])
            # dc_bev = gin.default_compact().reindex(
            #     ['C3_batt', 'FE_batt', 'E_elGer', 'C5_empty', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt',
            #      'S_renBig'], axis='rows')  # add energy density w and all X...

            cc_bev = gin.changed_compact().reindex(['C3_batt', 'FE_batt', 'E_elGer', 'C5_empty', 'E_elCh', 'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt',
                 'S_renBig'], axis='rows')  # add energy density w and all X...
            xc_bev = gin.x_vals().loc['compact(bev)']
            range_bev = pd.concat([cc_bev, gin.default_general()])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS
            return range_bev

        elif vehicle == 'FCEV':
            default_vals = pd.DataFrame({''})

        elif vehicle == 'PHEV':
            default_vals = pd.DataFrame({''})

        elif vehicle == 'FCEV':
            default_vals = pd.DataFrame({''})

        else:
            break

    elif veh_sel == 2:                              # midsize SUV #
        if vehicle == 'BEV':
            default_vals = pd.DataFrame({''})   # Hier alle Vals (Var + fix)

        elif vehicle == 'FCEV':
            default_vals = pd.DataFrame({''})

        elif vehicle == 'PHEV':
            default_vals = pd.DataFrame({''})

        elif vehicle == 'FCEV':
            default_vals = pd.DataFrame({''})

        else:
            break

    elif veh_sel == 3:                              # Light Duty Vehicle #
        if vehicle == 'BEV':
            default_vals = pd.DataFrame({''})   # Hier alle Vals (Var + fix)

        elif vehicle == 'FCEV':
            default_vals = pd.DataFrame({''})

        elif vehicle == 'PHEV':
            default_vals = pd.DataFrame({''})

        elif vehicle == 'FCEV':
            default_vals = pd.DataFrame({''})

        else:
            break

        dimension = ((default_vals.size) / 2)  # Length of Variable list

    else:
        print('Wrong Input! \n')
        vehClassSel()                               # Erneute Eingabe der Fahrzeugklasse

    return default_vals


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