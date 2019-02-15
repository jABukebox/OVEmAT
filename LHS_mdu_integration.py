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
def lhs_dimension():                  # Dynamic dimension of LHS - depending on no. of Vars saved as "dimension" -> Muss so lang sein wie die anzahl der Range werte!!
    dim = (len(all_range))  # Length of Variable list # TODO: len(range_variablen)
    return dim

def LatinHype(dimension, n):  # n = number of samples
    points = pyDOE.lhs(dimension, samples=n)
    return points  # output.type = array


# =============================================================================
# Choose Vehicle Class
# =============================================================================
def vehClassSel():              # saved as "class_sel"
    # veh_class = ['compact', 'suv', 'ldv']
    veh_class = int(input("1: Compact - 2: suv - 3: ldv \n"))
    return veh_class


# =============================================================================
# Verrechnen der LHS Ergebnisse mit Eingangsvariablen -> var_final entstehen      LHS!
# =============================================================================
def varFinal():
    propType = ['BEV','FCEV','PHEV','ICEV']
    var_all = []
    for vehicle in range(len(propType)):                                         # Durchlauf jedes propTypes
        gV = getVariables(class_sel, vehicle)                                      # holt die Values aus getVariables
        lhs_items = 0                                                            # TODO: muss bei PHEV evtl verändert werden
        var_array = []
        if vehicle ==2:                 # PHEV #
            for r in range(n):
                var_list = []
                m = 0
                t = 1
                dual = 0                                  # Changes getVariable from BEV to ICEV
                while dual < 4:                           # 0 ^= BEV
                    gV = getVariables(class_sel, dual)
                    for k in range(dimension):  # alle Range-Werte mit reihe des LHS multiplizieren
                        var_max = gV.iloc[m][t]  # bestimmung des max Wertes der eingegebenen Range
                        t -= 1
                        var_min = gV.iloc[m][t]  # bestimmung des min Wertes der eingegebenen Range
                        t += 1
                        var = (p.item(lhs_items) * (
                                    var_max - var_min)) + var_min  # Verrechnung der Variablen mit LHS Ergebnissen in var
                        var_list.append(var)  # Anhängen der Parameter an liste
                        lhs_items += 1
                        m += 1
                    dual += 3           # Erhöhung um 3 (3 ^= ICEV)
                var_array.append(var_list)
            var_array = np.around(var_array, decimals = 4)

        else:
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
    if class_sel == 1:                                  # compact car #   cc = changed compact
        if vehicle == 0:    # BEV
            cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                               axis='rows')  # must stay here (in getinput.py) for LHS-Dimension / S_ren!!!
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            range_vals = pd.concat([cc_bev, cg_bev])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS TODO: gin.default_general() vor varFinal


        elif vehicle == 1: # FCEV
            cc_fcev = gin.changed_compact().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            range_vals = pd.concat([cc_fcev, cg_fcev])

        # elif vehicle == 2:  # PHEV                                    #vehicle in getVariable never gets 2!! (see var Final dual loop)
        #     cc_phev = gin.changed_compact().reindex(
        #         ['C3_batt', 'FE_batt', 'C3_synth', 'FE_synth', 'cd', 'E_elGer', 'C5_icev', 'C5_empty', 'cd', 'E_elCh',
        #          'E_batt', 'L', 'D', 'C_fuelEl', 'r', 'C_batt', 'S_renSmall'], axis='rows')

        elif vehicle == 3:  # ICEV
            cc_icev = gin.changed_compact().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'],
                                                    axis='rows')
            cg_icev = gin.changed_general().reindex(
                ['C3_synth', 'C5_icev', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                 'C_fcEmpty'], axis='rows')
            range_vals = pd.concat([cc_icev, cg_icev])

        else:
            pass

    elif class_sel == 2:                              # midsize SUV #       cs = changed suv
        if vehicle == 0:    # BEV
            cs_bev = gin.changed_suv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            range_vals = pd.concat([cs_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cs_fcev = gin.changed_suv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_h2', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            range_vals = pd.concat([cs_fcev, cg_fcev])

        elif vehicle == 3:  # ICEV
            cs_icev = gin.changed_suv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(
                ['C3_synth', 'C5_icev', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                 'C_fcEmpty'], axis='rows')
            range_vals = pd.concat([cs_icev, cg_icev])

        else:
            pass

    elif class_sel == 3:                              # Light Duty Vehicle #       cl = changed ldv
        if vehicle == 0:    # BEV
            cl_bev = gin.changed_ldv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            range_vals = pd.concat([cl_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cl_fcev = gin.changed_ldv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_h2', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            range_vals = pd.concat([cl_fcev, cg_fcev])

        elif vehicle == 3:  # ICEV
            cl_icev = gin.changed_ldv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(
                ['C3_synth', 'C5_icev', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                 'C_fcEmpty'], axis='rows')
            range_vals = pd.concat([cl_icev, cg_icev])

        else:
            pass

    else:
        print('Wrong Input! \n')
        vehClassSel()                               # Erneute Eingabe der Fahrzeugklasse

    return range_vals


#################################################################################
# ============================================================================= #
# Definition of Classes (Calculations)                                          #
# ============================================================================= #
#################################################################################
class Vehicles():
    # @classmethod
    # def generalVals(cls,):
    #     static = get_valsfrom_df
    #     return static

    def __init__ (self, C3, C5, FE, E_elGer, w, cd, E_elCh, P_batt, E_batt, P_fc, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, m_curb, C_msrp, CF, C_batt, C_fc, P_fcSet, P_battSet, E_battSet, L, D, r, C_fuel, C_main, S_ren)
        self.C3 = C3
        self.C5 = C5
        self.FE = FE
        self.E_elGer = E_elGer
        self.__w = w
        self.cd = cd
        self.__X1 = X1
        self.__X2 = X2
        self.__X3 = X3
        self.__X4 = X4
        self.__X5 = X5
        self.__X6 = X6
        self.__X7 = X7
        self.__X8 = X8
        self.__X9 = X9
        self.__X10 = X10
        self.__X11 = X11
        self.__X12 = X12
        self.__X13 = X13
        self.__X14 = X14
        self.E_elGer = E_elGer
        self.E_elCh = E_elCh
        self.P_batt = P_batt
        self.C_batt = C_batt
        self.E_batt = E_batt
        self.P_fc = P_fc
        self.m_curb = m_curb
        self.C_msrp = C_msrp
        self.__CF = CF
        self.C_fc = C_fc
        self.__P_fcSet = P_fcSet
        self.__P_battSet = P_battSet
        self.__E_battSet=E_battSet
        self.L = L
        self.D = D
        self.r = r
        self.C_fuel = C_fuel
        self.C_main = C_main
        self.S_ren = S_ren

class LCE(Vehicles):
    #def __init__(self,):
    def calcFuelCycle(self):
        if vehicle == 0 or vehicle == 1 or vehicle == 3:              # trennung von PHEV. Calculation andere
            try:
                E_fc = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE
                return E_fc
            except:
                print("An error has occured! Please try again!")
        elif vehicle == 2:                                          # PHEV
            try:
                if class_sel == 1:              # Compact
                    C3 = # Hier müssen werte aus LHS verrechnung rein
                    c_v = gin.default_compact()  # bv = bev_vals

                elif class_sel == 2:            # SUV


                elif class_sel == 3:            # LDV
                    C3 =
                cs = 1 - self.cd/100
                E_fc_cs = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE # Hier werte für ICEV
                E_fc_cd = ... # Hier werte für BEV
                E_fc = (E_fc_cs * cs + E_fc_cd * self.cd)/100
                return E_fc
            except:
                print("An error has occured! Please try again!")


    def calcVehicleCycle(self):
        try:
            m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.E_batt - self.X12 * self.P_fc
            E_vc = self.X2 + self.X3 * self.E_elGer + m_scal * (self.X4 + self.X5 * self.E_elGer) + self.P_batt * (
                        self.X7 + self.X8 * self.E_elCh) + self.E_batt * (
                               self.X10 + self.X11 * self.E_elCh) + self.P_fc * (self.X13 + self.X14 * self.E_elGer)
            return E_vc
        except:
            print("An error has occured! Please try again!")


    def calcLCE(self):
        try:
            E_lce = (self.E_vc / (self.L * self.D) + self.E_fc)
            return E_lce
        except:
            print("An error has occured! Please try again!")


class TCO(Vehicles):
    def calcTCO(self):
        try:
            #L = self.L
            #y = 1
            sum_tco = 0
            for y in range(1, self.L+1):  # Bildung der Summe                   TODO: Schleife testen! L+1  ???
                Eq = ((self.C_fuel * self.FE) + (self.C_main / self.D)) / (1 + self.r) ** (y - 1)
                sum_tco += Eq

            C_veh = self.C_msrp + (self.C_batt * self.P_batt - self.C_battSet * self.P_battSet) * self.CF + (self.C_batt * self.E_batt - self.C_battSet * self.E_battSet) + (self.C_fc * self.P_fc - self.C_fcSet * self.P_fcSet)-self.S_ren

            C_tco = (C_veh / (self.L * self.D)) + sum_tco
            return C_tco
        except:
            print("An error has occured! Please try again!")



# # =============================================================================
# # Data Input & Print
# # =============================================================================
# # print("Please type in the fuel_cycle values: \n")
# print('\n\n\n')  # toyota ...
#
# # fuel_val = (0,0,13.814,0,0,0,28.06,489)
# # FCEV1 = fuel_cycle(fuel_val)
#
#
#
# FCEV1 = FuelCycle(0, 0, 13.814, 0, 0, 0, 28.06, 489)
# # print(FCEV1)
# FCEV2 = VehicleCycle(335.25, 1.124, 1.074, 2.41, 2.43, 1.25, 5.01, 6.22, 0, 0, 0, 5, 56.48, 40.89, 24.3, 489, 40, 0, 90,
#                      1850)
# # print(FCEV2)
# FCEV3 = TCO(0, 20000, 10000, 15000, 0, 3000, 0, 0, 14, 20000, 1.5, 7.4, 66, 150, 0, 0, 0,
#             0)  # hier darf 13. eintrag nicht 0 sein!! fehler ABFANGEN!
# # print(FCEV3)
# FCEV4 = LCE(VehicleCycle.calcVehicleCycle(FCEV2), FuelCycle.calcFuelCycle(FCEV1), 15, 10000)
# # FCEV4 = LCE(self.E_vc, self.E_fc, 15, 10000)
# # print(FCEV4)
#
# # emp_2 = Employee('Test', 'User', '12315')
#
# # =============================================================================
# # Output in Terminal
# # =============================================================================
#
# print("Fuel Cycle:\t\t\t"         + str(FuelCycle.calcFuelCycle(FCEV1))       + ' ' + "gCO_2eq / km")
# print("\nVehicle Cycle:\t\t"    + str(VehicleCycle.calcVehicleCycle(FCEV2)) + ' ' + "gCO_2eq")
# print("\n\nTotal Cost per km:\t"  + str(TCO.calcTCO(FCEV3))                   + ' ' + "€ / km")
# print("\nGesamte LCE:\t\t"    + str(LCE.calcLCE(FCEV4))                   + ' ' + "gCO_2 / km")
#
#
# #################################################################################



# =============================================================================
# Berechnung des results mit varFinal variablen
# =============================================================================
def resultCalc():
    propType = ['BEV','FCEV','PHEV','ICEV']
    for vehicle in range(len(propType)):
        pass
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
        for z in range(dimension):
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
        i = 0

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
        self.pos = [{'pos': res[i, :]} for i in range(n)]
        self.now = pg.ptime.time()
        self.plot.setData(self.pos)

        print('plot time: {} sec'.format(pg.ptime.time() - self.now))


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    n = 10  # Number of repeats (test it!)



    # Call Functions
    gen_def = gin.changed_general()  # Einlesen der general defaults

    all_range = pd.concat([gin.cc_bev, gin.cg_bev]) #für dimension length
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
