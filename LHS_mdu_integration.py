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
from pyqtgraph.Qt import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget
import getinput as gin
import os
import sys
import csv
# import pyqtgraph.opengl as gl

# Todo: boolean muss durch checkbox ersetzt werden
global booleanCheckbox
booleanCheckbox = 0

# =============================================================================
# Latin Hypercube Calculation TODO: check pyDOE "criterion and samples"!!
# =============================================================================
def lhs_dimension():                  # Dynamic dimension of LHS - depending on no. of Vars saved as "dimension"
    cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                       axis='rows')  # must stay here (in getinput.py) for LHS-Dimension / S_ren!!!
    cg_bev = gin.changed_general().reindex(
        ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],
        axis='rows')
    range_length = pd.concat([cc_bev, cg_bev])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS
    dim = (len(range_length))  # Length of Variable list # TODO: len(range_variablen)
    #print(dim)
    return dim

def LatinHype(dimension, n):  # n = number of samples
    points = pyDOE.lhs(dimension, samples=n*4)
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
    global vehicle
    for vehicle in range(len(propType)):                               # Durchlauf jedes propTypes
        gV = getVariables(class_sel, vehicle)                          # holt die Values aus getVariables
        lhs_items = 0                                                  # TODO: muss bei PHEV evtl verändert werden
        var_array = []
        #print('\n VEHICLE Top {}'.format(vehicle))
        #print('gV: {}'.format(gV))

        if vehicle == 2:                 # PHEV #
            for r in range(n):
                var_list = []
                #m = 0
                #t = 1
                dual = 0                                  # Changes getVariable from BEV to ICEV
                while dual <= 3:                           # 0 ^= BEV
                    #print('LHS: {}'.format(lhs_items))
                    gV_alt = getVariables(class_sel, dual)
                    #print(gV_alt)
                    m = 0
                    t = 1
                    for k in range(dimension):  # alle Range-Werte mit reihe des LHS multiplizieren
                        var_max = gV_alt.iloc[m][t]  # bestimmung des max Wertes der eingegebenen Range
                        #print(var_max)
                        t -= 1
                        #print(m)
                        var_min = gV_alt.iloc[m][t]  # bestimmung des min Wertes der eingegebenen Range
                        t += 1
                        var = (p.item(lhs_items) * (
                                    var_max - var_min)) + var_min # Verrechnung der Variablen mit LHS Ergebnissen in var
                        var_list.append(var)  # Anhängen der Parameter an liste
                        lhs_items += 1
                        m += 1
                        #print(var)
                    dual += 3           # Erhöhung um 3 (3 ^= ICEV)
                var_array.append(var_list)
                #print(var_array)
            var_array = np.around(var_array, decimals = 4)

        else:                           # BEV, FCEV, ICEV #
            for r in range(n):                                      # Anzahl der LHS Durchläufe
                var_list = []                                       # initiieren var_list:
                                                                    # hier sollen pro 'n' alle verrechneten parameter
                                                                    # in eine Liste gespeichert werden
                m = 0               # row / zeile
                t = 1               # column / spalte
                for k in range(dimension):                          # alle Range-Werte mit reihe des LHS multiplizieren
                    var_max = gV.iloc[m][t]                         # bestimmung des max Wertes der eingegebenen Range
                    t -= 1
                    var_min = gV.iloc[m][t]                         # bestimmung des min Wertes der eingegebenen Range
                    t += 1
                    var = (p.item(lhs_items) * (var_max - var_min)) + var_min   # Verrechnung der Variablen
                                                                                # mit LHS Ergebnissen in var
                    var_list.append(var)                                        # Anhängen der Parameter an liste
                    lhs_items += 1
                    m += 1
                var_array.append(var_list)                                      # Var_list gets appended to var_array
            var_array = np.around(var_array, decimals=4)                        # round numbers
        var_all.append(var_array)                                               # Abspeicherung aller verrechneten
    #print(var_all)                                                             # propType Variablen
    return var_all


def getVariables(class_sel, vehicle):
    global lhs_vals
    if class_sel == 1:                                  # compact car #   cc = changed compact
        if vehicle == 0:    # BEV
            cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                               axis='rows') # must stay here (in getinput.py) for LHS-Dimension / S_ren
            cg_bev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelEl', 'C_batt',
                 'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cc_bev, cg_bev])


        elif vehicle == 1: # FCEV
            cc_fcev = gin.changed_compact().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(
                ['C3_batt', 'C5_empty', 'E_elGer', 'cd_empty', 'E_elCh', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                axis='rows')
            lhs_vals = pd.concat([cc_fcev, cg_fcev])

        elif vehicle == 2:              # Todo: PHEV mit S_renSmall etc!
            pass

        # elif vehicle == 2:  # PHEV                    #vehicle in getVariable never gets 2!! (see var Final dual loop)
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
            cs_icev = gin.changed_suv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'],
                                                axis='rows')
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
    print(lhs_vals)
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


class LCE:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)
    # def calcFuelCycle(self):
    #     global e_fc         # Todo: auch löschen
    #     #vehicle = 0 # TODO: UNBEDINGT LÖSCHEN.. MUSS SELBST LAUFEN
    #     if vehicle == 0 or vehicle == 1 or vehicle == 3:              # trennung von PHEV. Calculation andere
    #         e_fc = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE
    #         print(e_fc)
    #         #return e_fc
    #
    #     elif vehicle == 2:                                          # PHEV
    #         pass # test!! pass danach entfernen
    #         # try:
    #         #     if class_sel == 1:              # Compact
    #         #         C3 = # Hier müssen werte aus LHS verrechnung rein
    #         #         c_v = gin.default_compact()  # bv = bev_vals
    #         #
    #         #     elif class_sel == 2:            # SUV
    #         #
    #         #
    #         #     elif class_sel == 3:            # LDV
    #         #         C3 =
    #         #     cs = 1 - self.cd/100
    #         #     e_fc_cs = self.C3 *self.FE * self.E_elGer + self.C5 * self.FE # Hier werte für ICEV
    #         #     e_fc_cd = ... # Hier werte für BEV
    #         #     e_fc = (e_fc_cs * cs + e_fc_cd * self.cd)/100
    #         #     return e_fc
    #         # except:
    #         #     print("An error has occured! Please try again!")


    # def calcVehicleCycle(self):
    #     #try:
    #     global e_vc # todo: auch löschen.. an calcLCE übergeben
    #     # m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.E_batt - self.X12 * self.P_fc
    #     # e_vc = self.X2 + self.X3 * self.E_elGer + m_scal * (self.X4 + self.X5 * self.E_elGer) + self.P_batt * (
    #     #             self.X7 + self.X8 * self.E_elCh) + self.E_batt * (
    #     #                    self.X10 + self.X11 * self.E_elCh) + self.P_fc * (self.X13 + self.X14 * self.E_elGer)
    #     #return e_vc
    #     #except:
    #     #    print("Calc Vehicle: An error has occured! Please try again!")


    def calcLCE(self):
        # FuelCycle Emissions
        if vehicle == 0 or vehicle == 1 or vehicle == 3:  # trennung von PHEV. Calculation andere
            e_fc = self.C3 * self.FE * self.E_elGer * self.w_h2 * self.w_synth + self.C5 * self.FE
        elif vehicle == 2:  # PHEV
            cd = 60
            C3_icev = 2.5
            FE_icev = 0.03
            C5_icev = 2000
            C3_bev = 1.1
            FE_bev = 0.12
            C5_bev = 0

            # if class_sel == 1:  # Compact
            #     cd =
            #
            # elif class_sel == 2:  # SUV
            #     ..
            # elif class_sel == 3:  # LDV

            cs = 100 - self.cd
            e_fc_cs = C3_icev * FE_icev * self.E_elGer + C5_icev * FE_icev  # Hier werte für ICEV
            e_fc_cd = C3_bev * FE_bev * self.E_elGer + C5_bev * FE_bev  # Hier werte für BEV
            e_fc = ((e_fc_cs * cs) + (e_fc_cd * self.cd))/100

        # Vehicle Cycle Emissions
        m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.E_batt - self.X12 * self.P_fc
        e_vc = self.X2 + self.X3 * self.E_elGer + m_scal * (self.X4 + self.X5 * self.E_elGer) + self.P_batt * (
                self.X7 + self.X8 * self.E_elCh) + self.E_batt * (
                       self.X10 + self.X11 * self.E_elCh) + self.P_fc * (self.X13 + self.X14 * self.E_elGer)

        e_lce = (e_vc / (self.L * self.D) + e_fc)
        print('e_lce: {} g/km'.format(e_lce))
        return e_lce
        #except:
        #    print("Calc LCE: An error has occured! Please try again!")


class TCO:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def calcTCO(self):
        sum_tco = 0
        for years in range(1, int(round(self.L+1))):  # Bildung der Summe               TODO: Schleife testen! L+1  ???
            Eq = ((self.C_fuel * self.FE) + (self.C_main / self.D)) / (1 + self.r) ** (years - 1)
            sum_tco += Eq
        print(self.CF)
        c_veh = self.C_msrp + ((self.C_batt * self.P_batt) - (self.C_battSet * self.P_battSet)) * (1/self.CF) + \
                ((self.C_batt * self.E_batt) - (self.C_battSet * self.E_battSet)) + \
                ((self.C_fc * self.P_fc) - (self.C_fcSet * self.P_fcSet))-self.S_ren
        print('c_veh: {} €'.format(c_veh))
        print('sum_tco: {} €/km\n'.format(sum_tco))
        c_tco = (c_veh / (self.L * self.D)) + sum_tco
        return c_tco




# =============================================================================
# Berechnung des results mit varFinal variablen
# =============================================================================

def resultCalc():
    propType = ['BEV','FCEV','PHEV','ICEV']
    all_para_keys = ['FE', 'E_batt', 'P_batt','P_fc','C3','C5','E_elGer','cd','E_elCh', 'L', 'D', 'r', 'C_fuel',
                    'C_batt', 'C_fc', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10','X11', 'X12',
                    'X13', 'X14', 'C_main', 'm_curb', 'C_msrp', 'P_battSet', 'E_battSet', 'P_fcSet', 'C_battSet',
                    'C_fcSet', 'CF', 'w_h2', 'w_synth','S_ren']

    #for vehicle in range(len(propType)): # get LHS vals
        #lhs_lists = var[vehicle]                        # hier sind die berechneten lhs-listen je propType
    #result = np.zeros(shape=(n*4, 2))
    result = np.zeros(shape=(0, 2))
    #print(result)
    #single_res = np.zeros(shape=(n,2))
    #single_res = np.zeros(shape=(n, 2))
    vehicle = 0
    res_row = 0
    if class_sel == 1:            # Compact
        countType = 0

    elif class_sel ==2:           # SUV
        countType = 1

    elif class_sel == 3:          # LDV
        countType = 2

    #for r in range(n):
    while countType < len(gin.x_vals()):            # zähler durch fix vals of class (bev, fcev, phev, icev)
        lhs_lists = var[vehicle]                    # alle ergebnis listen von einem propType
        #print('lhs_LISTS: {}'.format(lhs_lists))
        x_vals = list(gin.x_vals().iloc[countType])
        #print('x_vals: {}'.format(x_vals))
        spec_vals = list(gin.spec_vals().iloc[countType])
        #print('Spec_vals: {} '.format(spec_vals))
        x_vals.extend(spec_vals)          # hier sind alle fix vals
        #print('x_vals_extended: {}'.format(x_vals))
        r=0
        t=0
        single_res = np.zeros(shape=(n, 2))
        for list_num in range(len(lhs_lists)):          # TODO: lhs_lists müsste =n sein! TEST
            #print(list_num)
            #S_ren = 0
            if vehicle == 2:
                all_phev_lhs = list(lhs_lists[list_num])
                if booleanCheckbox == 1 and (vehicle == 0 or vehicle == 1):  # Check if theres a Subsituization
                    S_ren = 4000
                elif booleanCheckbox == 1 and (vehicle == 2):
                    S_ren = 3000
                else:
                    S_ren = 0.0
                all_cd = all_phev_lhs[:dimension]
                all_cs = all_phev_lhs[dimension:(dimension*2)]

                all_cd.extend(x_vals)
                all_cs.extend(x_vals)

                all_cd.append(S_ren)
                all_cs.append(S_ren)

                lhs_dict_cd = dict(zip(all_para_keys, all_cd))  # Hier liegen Dicts von lhs_vals
                lhs_dict_cs = dict(zip(all_para_keys, all_cs))

                lce_inst_cd = LCE(**lhs_dict_cd)
                lce_inst_cs = LCE(**lhs_dict_cs)



                tco_inst_cd = TCO(**lhs_dict_cd)
                tco_inst_cs = TCO(**lhs_dict_cs)


            elif vehicle == 0 or vehicle == 1 or vehicle == 3:

                print('Lhs_list[list_nums:\n {}'.format(lhs_lists[list_num]))
                all_values = list(lhs_lists[list_num])  # should be one single list of lhs_variable_results
                print('lhs_vals:{}'.format(all_values))
                all_values.extend(x_vals)        # ALL NEEDED VARS ARE HERE NOW
                if booleanCheckbox == 1 and (vehicle == 0 or vehicle == 1):             # Check if theres a Subsituization
                    S_ren = 4000
                elif booleanCheckbox == 1 and (vehicle == 2):
                    S_ren = 3000
                else:
                    S_ren = 0.0

                all_values.append(S_ren)
                #print('all_vals: {}'.format(all_values))
                lhs_dict = dict(zip(all_para_keys, all_values))
            #print('lhs_values:{}'.format(lhs_dict))
            lce_inst = LCE(**lhs_dict)
            tco_inst = TCO(**lhs_dict)
            e_lce_res = lce_inst.calcLCE()     #??
            #print('E_fc:{}'.format(e_fc_res))
            c_tco_res = tco_inst.calcTCO()
            # result[r][t] = e_fc
            # t+=1
            # result[r][t] = c_tco
            # t-=1
            # r+=1
            single_res[list_num] = [np.around(c_tco_res, decimals = 4), np.around(e_lce_res, decimals = 4)]     # Hier alle ergebnisse von BEV bzw. FCEV etc
            #print('Single res:\n{}\n'.format(single_res))
            #result[res_row] = [np.around(e_fc_res, decimals = 4), np.around(c_tco_res, decimals = 4)]
            #res_row += 1
        result = np.append(result, single_res, axis=0)    # Hier gesamtergebnis
        print('The result is: \n{}'.format(result))
        #print('\n')
        # append to a longer list
        countType+=3            # Sprung von compact_bev auf compact_fcev auf compact_phev ...
        vehicle +=1                                 # erhöhung -> lhs_lists bev -> fcev
    result = np.around(result, decimals=4)
    #print('Result:\n {}\n'.format(result))

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
        # create the view
        # view = pg.PlotWidget()

        app = QtGui.QApplication(sys.argv)
        mw = QtGui.QMainWindow()
        mw.resize(1000, 800)
        view = pg.GraphicsLayoutWidget()
        mw.setCentralWidget(view)
        mw.setWindowTitle('OVEmAt - Open Vehicle Emission Analysis Tool')
        #aim_2020 = addLine(x=None, y=95, z=None) # Ziel 2020: 95 gGHG/km


        # mw.setAspectLocked(True)
        #mw.showGrid(True, True, alpha=.5)

        # X Axis Settings
        #mw.xlabel.setTitleText('Total Cost of Ownership (€ / km)')

        # Y Axis Settings
        #mw.ylabel.setTitleText('Lifecycle Emissions (gGHG / km)')

        w1 = view.addPlot()

        w1.addLine(x=None, y=300, z=None)  # Ziel 2020: 95 gGHG/km
        w1.addLine(x=None, y=200, z=None)  # Aim 2030: 60 gGHG/km
        # Convert data array into a list of dictionaries with the x,y-coordinates

        x = res[:,0]
        print(x)
        y = res[:,1]
        print(y)
        fcev_points = [{'pos': res[(i+n):n*2, :]} for i in range(n)]
        phev_points = [{'pos': res[(i+2*n):n*3, :]} for i in range(n)]
        icev_points = [{'pos': res[(i+3*n):n*4, :]} for i in range(n)]
        #self.plot.setData(self.pos)
        now = pg.ptime.time()


        #point_size = 2
        color = QtGui.QColor("#0000FF")
        # Create Scatter Plot and add it to view
        # BEV
        plot = pg.ScatterPlotItem(x[:n], y[:n], size=8, pen=pg.mkPen(None),
                                  symbol = 'd', brush='cd5c5c')                                 # red
        w1.addItem(plot)

        # FCEV
        plot = pg.ScatterPlotItem(x[n:n * 2], y[n:n * 2], size=8, pen=pg.mkPen(None),
                                  symbol = 'd', brush='87cefa')                                 # blue
        w1.addItem(plot)

        # PHEV
        plot = pg.ScatterPlotItem(x[n * 2:n * 3], y[n * 2:n * 3], size=8, pen=pg.mkPen(None),
                                  symbol = 'd', brush='cd853f')                                 # orange
        w1.addItem(plot)

        # ICEV
        plot = pg.ScatterPlotItem(x[n * 3:n * 4], y[n * 3:n * 4], size=8, pen=pg.mkPen(None),
                                  symbol = 'd', brush='bdb76b')                                 # green
        w1.addItem(plot)

        print('plot time: {} sec'.format(pg.ptime.time() - now))

        mw.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    n = 5  # Number of repeats (test it!)

    # Call Functions
    class_sel = vehClassSel()
    dimension = lhs_dimension()  # Dimension, bzw. Zahl der Variablen
    p = LatinHype(dimension, n)
    var = varFinal()
    res = resultCalc()

    # Make App
    #app = pg.mkQApp()  # main application instance
    #app = QApplication(sys.argv)
    w = PlotClass()
    #w.show()
    #sys.exit(app.exec_())
