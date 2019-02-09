import numpy as np

def varFinal():
    propType = ['BEV','FCEV','PHEV','ICEV']
    var_all = []
    for vehicle in range(len(propType)):                                         # Durchlauf jedes propTypes
        gV = getVariables(veh_sel, vehicle)                                      # holt die
        lhs_items = 0
        var_array = []

        for r in range(n):                                                       # Anzahl der LHS Durchläufe
            var_list = []                                                        # initiieren var_list: hier sollen pro 'n' alle verrechneten parameter in eine Liste gespeichert werden
            m = 1
            t = 0
            for k in range(dimension):                                           # alle Range-Werte mit reihe des LHS multiplizieren
                var_max = gV.iloc[m][t]
                m -= 1
                var_min = gV.iloc[m][t]
                m += 1
                var = (p.item(lhs_items) * (var_max - var_min)) + var_min        # Verrechnung der Variablen mit LHS Ergebnissen in var
                var_list.append(var)                                             # Anhängen der Paramter an liste
                lhs_items += 1
                t += 1

            var_array.append(var_list)                                           # Var_list gets appended to var_array
        var_array = np.around(var_array, decimals=4)                             # round numbers
    var_all.append(var_array)                                                    # Abspeicherung aller verrechneten
    print(var_all)                                                               # propType Variablen
    return var_all



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