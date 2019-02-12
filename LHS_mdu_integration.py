#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Latin Hypercube Sampling (LHS) Loop with hard coded variables
# Umschreiben: Fct returns und Parameterübergabe!
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pyDOE as pyDOE
import pandas as pd
import pyqtgraph as pg
import getinput as gin
import os
import sys
import csv
# import pyqtgraph.opengl as gl


# =============================================================================
# Latin Hypercube Calculation TODO: check pyDOE "criterion and samples"!!
# =============================================================================
def LatinHype(dimension, n):  # n = number of samples
    points = pyDOE.lhs(dimension, samples=n)
    return points  # output.type = array


def lhs_dimension():                  # Dynamic dimension of LHS - depending on no. of Vars saved as "dimension" -> Muss so lang sein wie die anzahl der Range werte!!
    dim = (len())  # Length of Variable list # TODO: len(range_variablen)
    return dim


# =============================================================================
# Choose Vehicle Class
# =============================================================================
def vehClassSel():              # saved as "class_sel"
    # veh_class = ['compact', 'suv', 'ldv']
    veh_class = int(input("1: Compact - 2: suv - 3: ldv \n"))
    return veh_class


    # if veh_class == 1:       # spezifische Werte für compact class (fix & var)
    #     class_val = []       # compact here
    #
    # elif veh_class == 2:     # suv
    #     class_val = []
    #
    # elif veh_class == 3:     # ldv
    #     class_val = []


# # =============================================================================
# # Einlesen der Variablen aus getinput.py
# # =============================================================================
# def getVariables():
#     #propType = ['FCEV', 'BEV', 'ICEV', 'PHEV']
#     if veh_sel==1:                                  # compact car #
#
#         if vehicle == 'BEV':                        # Hier alle Vals (Var + fix)
#             var_vals = pd.DataFrame({''})
#             fix_vals =
#             default_vals = pd.DataFrame({''})
#
#
#         elif vehicle == 'FCEV':
#             default_vals = pd.DataFrame({''})
#
#         elif vehicle == 'PHEV':
#             default_vals = pd.DataFrame({''})
#
#         elif vehicle == 'FCEV':
#             default_vals = pd.DataFrame({''})
#
#         else:
#             pass
#
#     elif veh_sel == 2:                              # midsize SUV #
#
#         if vehicle == 'BEV':
#             default_vals = pd.DataFrame({''})   # Hier alle Vals (Var + fix)
#
#         elif vehicle == 'FCEV':
#             default_vals = pd.DataFrame({''})
#
#         elif vehicle == 'PHEV':
#             default_vals = pd.DataFrame({''})
#
#         elif vehicle == 'FCEV':
#             default_vals = pd.DataFrame({''})
#
#         else:
#             pass
#
#     elif veh_sel == 3:                              # Light Duty Vehicle #
#
#         if vehicle == 'BEV':
#             default_vals = pd.DataFrame({''})   # Hier alle Vals (Var + fix)
#
#         elif vehicle == 'FCEV':
#             default_vals = pd.DataFrame({''})
#
#         elif vehicle == 'PHEV':
#             default_vals = pd.DataFrame({''})
#
#         elif vehicle == 'FCEV':
#             default_vals = pd.DataFrame({''})
#
#         else:
#             pass
#
#         dimension = ((default_vals.size) / 2)  # Length of Variable list
#
#     else:
#         print('Wrong Input! \n')
#         vehClassSel()                               # Erneute Eingabe der Fahrzeugklasse
#
#     return default_vals


    # # print(var_range_sort_df.iloc[1][0]) # Zeile * Spalte
    # # print(p.item(0))
    # return var_range_sort_df


#################################################################################
# ============================================================================= #
# Definition of Classes (Calculations)                                          #
# ============================================================================= #
#################################################################################

class FuelCycle():
    def __init__(self, C3, C5, FE, E_elGer, w, cd):
        self.C3 = C3
        self.C5 = C5
        self.C6 = C6
        self.FE = FE
        self.E_elGer = E_elGer
        self.w = w
        self.cd = cd
        #self.calcFuelCycle

    def calcFuelCycle(self):
        if vehicle == 'BEV' or vehicle == 'FCEV' or vehicle == 'ICEV':              # trennung von PHEV. Calculation andere
            try:
                E_fc = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE
                return E_fc
            except:
                print("An error has occured! Please try again!")
        elif vehicle == 'PHEV':
            try:
                if class_sel == 1:
                    C3 = # Hier müssen werte aus LHS verrechnung rein
                    c_v = gin.default_compact()  # bv = bev_vals

                elif class_sel == 2:

                elif class_sel == 3:

                cs = 100 - self.cd
                E_fc_cs = C3 *self.FE * self.E_elGer + self.C5 * self.FE # Hier werte für ICEV
                E_fc_cd = # Hier werte für BEV
                E_fc = (E_fc_cs * cs + E_fc_cd * cd)/100
                return E_fc
            except:
                print("An error has occured! Please try again!")

class VehicleCycle():
    # FCEV2 = vehicle_cycle(35.25, 1.124, 1.074, 2.41, 2.43, 1.25, 5.01, 6.22, 0, 0, 0, 5, 56.48, 40.89(x14), 24.3, 489, 40, 0, 90, 1850)
    def __init__(self, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14,
                 E_elec, m_scal, P_batt, C_batt, P_fc, m_curb):
        self.X1 = X1
        self.X2 = X2
        self.X3 = X3
        self.X4 = X4
        self.X5 = X5
        self.X6 = X6
        self.X7 = X7
        self.X8 = X8
        self.X9 = X9
        self.X10 = X10
        self.X11 = X11
        self.X12 = X12
        self.X13 = X13
        self.X14 = X14
        self.E_elec = E_elec
        self.m_scal = m_scal
        self.P_batt = P_batt
        self.C_batt = C_batt
        self.P_fc = P_fc
        self.m_curb = m_curb
        #self.calcVehicleCycle

    def calcVehicleCycle(self):
        try:
            m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.C_batt - self.X12 * self.P_fc
            E_vc = self.X2 + self.X3 * self.E_elec + m_scal * (self.X4 + self.X5 * self.E_elec) + self.P_batt * (
                        self.X7 + self.X8 * self.E_elec) + self.C_batt * (
                               self.X10 + self.X11 * self.E_elec) + self.P_fc * (self.X13 + self.X14 * self.E_elec)
            return E_vc
        except:
            print("An error has occured! Please try again!")


class TCO():  # FE may not be '0' - (ZeroDevisionError)
    def __init__(self, C_msrp, C_aV, C_EM, C_Pbatt, C_Ebatt, C_FC, C_CM, C_TM, L, D, r, C_fuel,
                 FE, C_maint, C_BEV, C_FCEV, C_ICEV, C_PHEV, S_ren):
        # Beispiel Values FCEV): 0, 20000, 10000, 15000, 0, 3000, 0, 0, 14, 20000, 1.5, 7.4, 66, 150, 0, 0, 0, 0
        self.C_msrp = C_msrp
        self.C_aV = C_aV
        self.C_EM = C_EM
        self.C_Pbatt = C_Pbatt
        self.C_Ebatt = C_Ebatt
        self.C_FC = C_FC
        self.C_CM = C_CM
        self.C_TM = C_TM
        self.L = L
        self.D = D
        self.r = r
        self.C_fuel = C_fuel
        self.FE = FE
        self.C_maint = C_maint
        self.C_BEV = C_BEV
        self.C_FCEV = C_FCEV
        self.C_ICEV = C_ICEV
        self.C_PHEV = C_PHEV
        self.S_ren = S_ren
        #self.calcTCO

    def calcTCO(self):
        try:
            # Hier C_BEV, C_FCEV berechnen mit C_BEV = self.C_aV + self.C_EM, self.C_Pbatt, Cself._Ebatt, self.C_FC, self.C_CM, self.C_Tm
            L = self.L + 1
            #y = 1
            SUMME = 0
            for y in range(1, L):  # Bildung der Summe
                Eq = ((self.C_fuel / self.FE) + (self.C_maint / self.D)) / (1 + self.r) ** (y - 1)
                SUMME = SUMME + Eq
                # y = +1
            #if boolean Checkbox = 0:
            C_msrp = self.C_aV + self.C_BEV + self.C_FCEV + self.C_ICEV + self.C_PHEV
            #else:
                #C_msrp = self.C_aV + self.C_BEV + self.C_FCEV + self.C_ICEV + self.C_PHEV - self.S_ren
            C_tco = C_msrp / (self.L * self.D) + SUMME
            return C_tco
        except:
            print("An error has occured! Please try again!")


class LCE():
    def __init__(self, E_vc, E_fc, L, D):
        self.E_vc = E_vc
        self.E_fc = E_fc
        self.L = L
        self.D = D
        #self.calcLCE

    def calcLCE(self):
        try:
            E_lce = (self.E_vc / (self.L * self.D) + self.E_fc)
            return E_lce
        except:
            print("An error has occured! Please try again!")


# =============================================================================
# Data Input & Print
# =============================================================================
# print("Please type in the fuel_cycle values: \n")
print('\n\n\n')  # toyota ...

# fuel_val = (0,0,13.814,0,0,0,28.06,489)
# FCEV1 = fuel_cycle(fuel_val)

FCEV1 = FuelCycle(0, 0, 13.814, 0, 0, 0, 28.06, 489)
# print(FCEV1)
FCEV2 = VehicleCycle(335.25, 1.124, 1.074, 2.41, 2.43, 1.25, 5.01, 6.22, 0, 0, 0, 5, 56.48, 40.89, 24.3, 489, 40, 0, 90,
                     1850)
# print(FCEV2)
FCEV3 = TCO(0, 20000, 10000, 15000, 0, 3000, 0, 0, 14, 20000, 1.5, 7.4, 66, 150, 0, 0, 0,
            0)  # hier darf 13. eintrag nicht 0 sein!! fehler ABFANGEN!
# print(FCEV3)
FCEV4 = LCE(VehicleCycle.calcVehicleCycle(FCEV2), FuelCycle.calcFuelCycle(FCEV1), 15, 10000)
# FCEV4 = LCE(self.E_vc, self.E_fc, 15, 10000)
# print(FCEV4)

# emp_2 = Employee('Test', 'User', '12315')

# =============================================================================
# Output in Terminal
# =============================================================================

print("Fuel Cycle:\t\t\t"         + str(FuelCycle.calcFuelCycle(FCEV1))       + ' ' + "gCO_2eq / km")
print("\nVehicle Cycle:\t\t"    + str(VehicleCycle.calcVehicleCycle(FCEV2)) + ' ' + "gCO_2eq")
print("\n\nTotal Cost per km:\t"  + str(TCO.calcTCO(FCEV3))                   + ' ' + "€ / km")
print("\nGesamte LCE:\t\t"    + str(LCE.calcLCE(FCEV4))                   + ' ' + "gCO_2 / km")


#################################################################################


# =============================================================================
# Verrechnen der LHS Ergebnisse mit Eingangsvariablen -> var_final entstehen      LHS!
# =============================================================================
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


# =============================================================================
# Berechnung des results mit varFinal variablen
# =============================================================================
def resultCalc():

    # Put all values together
    X_vals = list(gin.x_vals().loc['compact(bev)']) # get X_vals Todo: schleife für compact, suv etc ->

    FuelVals = ...          # Todo: Hier alle Listen zusammenfügen. die jeweiligen werte aus LHS + X_vals + constant_vals + spec_vals
    E_fc = FuelCycle(FuelVals)                    # Hier wird

    ### erstellen eines mit Nullen gefüllten arrays
    result = np.zeros(shape=(n, 2))  # m * n Matrix = zeile * Spalte
    # r = 0                                                          # laufvar. für schleife "LHS-Durchläufe"
    m = 0

    for r in range(n):
        t = 0
        for z in range(dimension)
            x = var[r][t]
            t += 1

        x2 = var[r][t]
        x = np.around(x1 + x2, decimals=4)
        t += 1
        y1 = var[r][t]
        t += 1
        y2 = var[r][t]
        y = np.around(y1 + y2, decimals=4)
        # print(r)
        # print(x,y)
        m += 1
        result[r] = [x, y]
        # print(result[r])
        # r+=1

    result = np.around(result, decimals=4)
    # print("Result Values")
    # print(result)
    return result


# =============================================================================
# Plot results
# =============================================================================
class PlotClass():
    def __init__(self, parent=None):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.save_csv()

    def save_csv(self):  # create folder & file and write results
        if not os.path.exists('results/'):
            os.makedirs('results/')

        with open("results/result.csv", 'w') as fp:
            a = csv.writer(fp, delimiter=";")
            a.writerows(map(lambda t: ("%.4f" % t[0], "%.4f" % t[1]), res))
            self.plotting()

    def plotting(self):
        self.i = 0

        # create the view
        self.view = pg.PlotWidget()
        self.view.resize(800, 600)
        self.view.setWindowTitle('scatter plot using pyqtgraph - test')
        self.view.setAspectLocked(True)
        self.view.showGrid(True, True, alpha=.5)
        self.view.show()

        # Create Scatter Plot and add it to view
        self.plot = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol='x', size=1)
        # self.plot = pg.gl.GLSurfacePlotItem(pen=pg.mkPen(width=5, color='r'), symbol = 'x', size=1)
        self.view.addItem(self.plot)

        # Convert data array into a list of dictionaries with the x,y-coordinates
        self.pos = [{'pos': res[self.i, :]} for self.i in range(n)]
        self.now = pg.ptime.time()
        self.plot.setData(self.pos)

        print('plot time: {} sec'.format(pg.ptime.time() - self.now))


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    n = 1000  # Number of repeats (test it!)



    # Call Functions
    gen_def = gin.default_general()  # Einlesen der general defaults
    all_range = pd.concat([gin.cc_bev, gen_def]) #für dimension length
    dimension = lhs_dimension()  # Dimension, bzw. Zahl der Variablen

    class_sel = vehClassSel()
    p = LatinHype(dimension, n)
    #gV = getVariables()             # TODO: Check gV in varFinal! doppelung?
    var = varFinal()
    res = resultCalc()

    # Make App
    app = pg.mkQApp()  # main application instance
    w = PlotClass()
    sys.exit(app.exec_())

# =============================================================================
# ### Create figure
# plt.figure(figsize=[5,5])
# x_max,y_max = result.max(axis=0)
# #print(x_max,y_max)
#
# x_min,y_min = result.min(axis=0)
#
# ### relative achsen
# #plt.xlim([(x_min-x_max/5),(x_max+x_max/5)]) # Anpassen der Achsen xmin / xmax +- 20%
# #plt.ylim([(y_min-y_max/5),(y_max+y_max/5)])
#
# ### absolute Achsen
# plt.xlim([0,(x_max+x_max/5)]) # Anpassen der Achsen xmin / xmax +- 20%
# plt.ylim([0,(y_max+y_max/5)])
#
# ### Plot result
# plt.scatter(result[:,0],result[:,1], c='r')     # scatter plot result
# plt.grid(True)                                  # activate grid
#
# # =============================================================================
# # i=0
# # step = (x_max+x_max/5) - (x_min-x_min/5)
# # for i in np.arange((x_min-x_min/5),(x_max+x_max/5)+1,step/n):
# #     plt.axvline(i)
# #     plt.axhline(i)
# # =============================================================================
#
#
# plt.show()
#
#
# =============================================================================

