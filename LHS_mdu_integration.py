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
    cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                       axis='rows')  # must stay here (in getinput.py) for LHS-Dimension / S_ren!!!
    cg_bev = gin.changed_general().reindex(
        ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],
        axis='rows')
    range_length = pd.concat([cc_bev, cg_bev])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS
    dim = (len(range_length))  # Length of Variable list # TODO: len(range_variablen)
    print(dim)
    return dim

def LatinHype(dimension, n):  # n = number of samples
    points = pyDOE.lhs(dimension*4, samples=n)
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
        print('\n VEHICLE Top {}'.format(vehicle))
        #print('gV: {}'.format(gV))

        if vehicle == 2:                 # PHEV #
            for r in range(n):
                var_list = []
                #m = 0
                #t = 1
                dual = 0                                  # Changes getVariable from BEV to ICEV
                while dual <= 3:                           # 0 ^= BEV
                    print('LHS: {}'.format(lhs_items))
                    gV_alt = getVariables(class_sel, dual)
                    print(gV_alt)
                    m = 0
                    t = 1
                    for k in range(dimension):  # alle Range-Werte mit reihe des LHS multiplizieren
                        var_max = gV_alt.iloc[m][t]  # bestimmung des max Wertes der eingegebenen Range
                        print(var_max)
                        t -= 1
                        print(m)
                        var_min = gV_alt.iloc[m][t]  # bestimmung des min Wertes der eingegebenen Range
                        t += 1
                        var = (p.item(lhs_items) * (
                                    var_max - var_min)) + var_min  # Verrechnung der Variablen mit LHS Ergebnissen in var
                        var_list.append(var)  # Anhängen der Parameter an liste
                        lhs_items += 1
                        m += 1
                        #print(var)
                    dual += 3           # Erhöhung um 3 (3 ^= ICEV)
                var_array.append(var_list)
                print(var_array)
            var_array = np.around(var_array, decimals = 4)

        else:                           # BEV, FCEV, ICEV #
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
        print('\n VEHICLE bottom {}'.format(vehicle))
    print(var_all)                                                               # propType Variablen
    return var_all


def getVariables(class_sel, vehicle):
    global lhs_vals
    if class_sel == 1:                                  # compact car #   cc = changed compact
        if vehicle == 0:    # BEV
            cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                               axis='rows')  # must stay here (in getinput.py) for LHS-Dimension / S_ren!!!
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cc_bev, cg_bev])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS TODO: gin.default_general() vor varFinal


        elif vehicle == 1: # FCEV
            cc_fcev = gin.changed_compact().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            lhs_vals = pd.concat([cc_fcev, cg_fcev])

        elif vehicle == 2:
            pass

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
            lhs_vals = pd.concat([cc_icev, cg_icev])

        #else:
        #    pass

    elif class_sel == 2:                              # midsize SUV #       cs = changed suv
        if vehicle == 0:    # BEV
            cs_bev = gin.changed_suv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cs_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cs_fcev = gin.changed_suv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_h2', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            lhs_vals = pd.concat([cs_fcev, cg_fcev])

        elif vehicle == 2:
            pass

        elif vehicle == 3:  # ICEV
            cs_icev = gin.changed_suv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(
                ['C3_synth', 'C5_icev', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                 'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cs_icev, cg_icev])

        #else:
        #    pass

    elif class_sel == 3:                              # Light Duty Vehicle #       cl = changed ldv
        if vehicle == 0:    # BEV
            cl_bev = gin.changed_ldv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cl_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cl_fcev = gin.changed_ldv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_h2', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            lhs_vals = pd.concat([cl_fcev, cg_fcev])

        elif vehicle == 2:
            pass

        elif vehicle == 3:  # ICEV
            cl_icev = gin.changed_ldv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(
                ['C3_synth', 'C5_icev', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                 'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cl_icev, cg_icev])

        #else:
        #    pass

    else:
        print('Wrong Input! \n')
        vehClassSel()                               # Erneute Eingabe der Fahrzeugklasse
    #print(lhs_vals)
    return lhs_vals


#################################################################################
# ============================================================================= #
# Definition of Classes (Calculations)                                          #
# ============================================================================= #
#################################################################################
# class Vehicles:
    # @classmethod
    # def generalVals(cls,):
    #     static = get_valsfrom_df
    #     return static

    # def __init__ (self, C3, C5, FE, E_elGer, w, cd, E_elCh, P_batt, E_batt, P_fc, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, m_curb, C_msrp, CF, C_batt, C_fc, P_fcSet, P_battSet, E_battSet, L, D, r, C_fuel, C_main, S_ren):
    #     self.C3 = C3
    #     self.C5 = C5
    #     self.FE = FE
    #     self.E_elGer = E_elGer
    #     self.__w = w
    #     self.cd = cd
    #     self.__X1 = X1
    #     self.__X2 = X2
    #     self.__X3 = X3
    #     self.__X4 = X4
    #     self.__X5 = X5
    #     self.__X6 = X6
    #     self.__X7 = X7
    #     self.__X8 = X8
    #     self.__X9 = X9
    #     self.__X10 = X10
    #     self.__X11 = X11
    #     self.__X12 = X12
    #     self.__X13 = X13
    #     self.__X14 = X14
    #     self.E_elGer = E_elGer
    #     self.E_elCh = E_elCh
    #     self.P_batt = P_batt
    #     self.C_batt = C_batt
    #     self.E_batt = E_batt
    #     self.P_fc = P_fc
    #     self.m_curb = m_curb
    #     self.C_msrp = C_msrp
    #     self.__CF = CF
    #     self.C_fc = C_fc
    #     self.__P_fcSet = P_fcSet
    #     self.__P_battSet = P_battSet
    #     self.__E_battSet=E_battSet
    #     self.L = L
    #     self.D = D
    #     self.r = r
    #     self.C_fuel = C_fuel
    #     self.C_main = C_main
    #     self.S_ren = S_ren

class LCE():
    def __init__(self, C3, C5, FE, E_elGer, w, cd, E_elCh, P_batt, E_batt, P_fc, X1, X2, X3, X4, X5, X6, X7, X8, X9,
                 X10, X11, X12, X13, X14, m_curb, C_msrp, CF, C_batt, C_fc, P_fcSet, P_battSet, E_battSet, L, D, r,
                 C_fuel, C_main, S_ren):
        self.C3 = C3
        self.C5 = C5
        self.FE = FE
        self.E_elGer = E_elGer
        self.w = w
        self.cd = cd
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
        self.E_elGer = E_elGer
        self.E_elCh = E_elCh
        self.P_batt = P_batt
        self.C_batt = C_batt
        self.E_batt = E_batt
        self.P_fc = P_fc
        self.m_curb = m_curb
        self.C_msrp = C_msrp
        self.CF = CF
        self.C_fc = C_fc
        self.P_fcSet = P_fcSet
        self.P_battSet = P_battSet
        self.E_battSet = E_battSet
        self.L = L
        self.D = D
        self.r = r
        self.C_fuel = C_fuel
        self.C_main = C_main
        self.S_ren = S_ren
    def calcFuelCycle(self):
        if vehicle == 0 or vehicle == 1 or vehicle == 3:              # trennung von PHEV. Calculation andere
            try:
                e_fc = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE
                return e_fc
            except:
                print("An error has occured! Please try again!")
        elif vehicle == 2:                                          # PHEV
            pass # test!! pass danach entfernen
            # try:
            #     if class_sel == 1:              # Compact
            #         C3 = # Hier müssen werte aus LHS verrechnung rein
            #         c_v = gin.default_compact()  # bv = bev_vals
            #
            #     elif class_sel == 2:            # SUV
            #
            #
            #     elif class_sel == 3:            # LDV
            #         C3 =
            #     cs = 1 - self.cd/100
            #     e_fc_cs = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE # Hier werte für ICEV
            #     e_fc_cd = ... # Hier werte für BEV
            #     e_fc = (e_fc_cs * cs + e_fc_cd * self.cd)/100
            #     return e_fc
            # except:
            #     print("An error has occured! Please try again!")


    def calcVehicleCycle(self):
        try:
            m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.E_batt - self.X12 * self.P_fc
            e_vc = self.X2 + self.X3 * self.E_elGer + m_scal * (self.X4 + self.X5 * self.E_elGer) + self.P_batt * (
                        self.X7 + self.X8 * self.E_elCh) + self.E_batt * (
                               self.X10 + self.X11 * self.E_elCh) + self.P_fc * (self.X13 + self.X14 * self.E_elGer)
            return e_vc
        except:
            print("An error has occured! Please try again!")


    def calcLCE(self):
        try:
            e_lce = (self.e_vc / (self.L * self.D) + self.e_fc)
            print (e_lce)
            return e_lce
        except:
            print("An error has occured! Please try again!")


class TCO():
    def __init__(self, C3, C5, FE, E_elGer, w, cd, E_elCh, P_batt, E_batt, P_fc, X1, X2, X3, X4, X5, X6, X7, X8, X9,
                 X10, X11, X12, X13, X14, m_curb, C_msrp, CF, C_batt, C_fc, P_fcSet, P_battSet, E_battSet, L, D, r,
                 C_fuel, C_main, S_ren):
        self.C3 = C3
        self.C5 = C5
        self.FE = FE
        self.E_elGer = E_elGer
        self.w = w
        self.cd = cd
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
        self.E_elGer = E_elGer
        self.E_elCh = E_elCh
        self.P_batt = P_batt
        self.C_batt = C_batt
        self.E_batt = E_batt
        self.P_fc = P_fc
        self.m_curb = m_curb
        self.C_msrp = C_msrp
        self.CF = CF
        self.C_fc = C_fc
        self.P_fcSet = P_fcSet
        self.P_battSet = P_battSet
        self.E_battSet = E_battSet
        self.L = L
        self.D = D
        self.r = r
        self.C_fuel = C_fuel
        self.C_main = C_main
        self.S_ren = S_ren
    def calcTCO(self):
        try:
            #L = self.L
            #y = 1
            sum_tco = 0
            for y in range(1, self.L+1):  # Bildung der Summe                   TODO: Schleife testen! L+1  ???
                Eq = ((self.C_fuel * self.FE) + (self.C_main / self.D)) / (1 + self.r) ** (y - 1)
                sum_tco += Eq

            c_veh = self.C_msrp + (self.C_batt * self.P_batt - self.C_battSet * self.P_battSet) * self.CF + (self.C_batt * self.E_batt - self.C_battSet * self.E_battSet) + (self.C_fc * self.P_fc - self.C_fcSet * self.P_fcSet)-self.S_ren

            c_tco = (c_veh / (self.L * self.D)) + sum_tco
            return c_tco
        except:
            print("An error has occured! Please try again!")



# =============================================================================
# Berechnung des results mit varFinal variablen
# =============================================================================

def resultCalc():
    propType = ['BEV','FCEV','PHEV','ICEV']

    #for vehicle in range(len(propType)): # get LHS vals
        #lhs_lists = var[vehicle]                        # hier sind die berechneten lhs-listen je propType
    result = np.zeros(shape=(n*4, 2))
    single_res = np.zeros(shape=(n,2))
    vehicle = 0
    if class_sel == 1:            # Compact
        countType = 0

    elif class_sel ==2:           # SUV
        countType = 1

    elif class_sel == 3:          # LDV
        countType = 2

    while countType < len(gin.x_vals()):            # zähler durch fix vals (bev, fcev, phev, icev)
        lhs_lists = var[vehicle]                    # alle ergebnis listen von einem propType
        x_vals = list(gin.x_vals().iloc[countType])
        print(x_vals)
        spec_vals = list(gin.spec_vals().iloc[countType])
        print(spec_vals)
        x_vals.extend(spec_vals)          # hier sind alle fix vals
        # all_fix = x_vals.extend(spec_vals)          # hier sind alle fix vals
        print('all fix:{}\n'.format(x_vals))
        r=0
        t=0

        for list_num in range(len(lhs_lists)):          # TODO: lhs_lists müsste =n sein! TEST
            lhs_values = list(lhs_lists[list_num])  # should be one single list of lhs_variable_results
            #FCEV4 = LCE(VehicleCycle.calcVehicleCycle(FCEV2)
            print('lhs_values:{}'.format(lhs_values))
            lhs_values.extend(x_vals)        # ALL NEEDED VARS ARE HERE NOW
            print('lhs_values:{}'.format(lhs_values))
            e_fc = LCE.calcLCE(lhs_values)     #??
            c_tco = TCO.calcTCO(lhs_values)
            # result[r][t] = e_fc
            # t+=1
            # result[r][t] = c_tco
            # t-=1
            # r+=1
            single_res[list_num] = [e_fc, c_tco]     # Hier alle ergebnisse von BEV bzw. FCEV etc
        result[vehicle] = single_res                # Hier gesamtergebnis (Muss bei Print gesplittet werden mit n/4 !??)
        # append to a longer list
        countType+=3            # Sprung von compact_bev auf compact_fcev auf compact_phev ...
        vehicle +=1                                 # erhöhung -> lhs_lists bev -> fcev
    result = np.around(result, decimals=4)
    print(result)
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

    n = 4  # Number of repeats (test it!)



    # Call Functions
    #gen_def = gin.changed_general()  # Einlesen der general defaults

    class_sel = vehClassSel()
    dimension = lhs_dimension()  # Dimension, bzw. Zahl der Variablen
    p = LatinHype(dimension, n)
    #gV = getVariables()             # TODO: Check gV in varFinal! doppelung?
    var = varFinal()
    #print(var)
    res = resultCalc()

    # Make App
    app = pg.mkQApp()  # main application instance
    w = PlotClass()
    sys.exit(app.exec_())
