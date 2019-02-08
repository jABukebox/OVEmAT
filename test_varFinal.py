def varFinal():
    propType = ['BEV','FCEV','PHEV','ICEV']
    var_all = []
    for vehicle in range(len(propType)):                                                        # Durchlauf jedes propTypes

        lhs_items = 0
        var_array = []

        for r in range(n):      # Anzahl der Durchläufe
            var_list = []
            m = 1
            t = 0
            for k in range(dimension):      # alle Range-Werte mit reihe des LHS multiplizieren
                var_max = gV.iloc[m][t]
                m -= 1
                var_min = gV.iloc[m][t]
                m += 1
                var = (p.item(lhs_items) * (var_max - var_min)) + var_min
                var_list.append(var)
                lhs_items += 1
                t += 1

            var_array.append(var_list)  # Var_list gets appended to var_array
        var_array = np.around(var_array, decimals=4)  # round numbers
    var_all.append(var_array)                                                                   # Abspeicherung aller verrechneten
    print(var_all)                                                                              # propType Variablen
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