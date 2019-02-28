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
from pyqtgraph import InfiniteLine as il
from pyqtgraph import SignalProxy as sp
import getinput as gin
import os
import sys
import csv
from PyQt5 import QtCore
# import pyqtgraph.opengl as gl
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget

# Todo: boolean muss durch checkbox ersetzt werden
global booleanCheckbox
booleanCheckbox = 0

# =============================================================================
# Latin Hypercube Calculation
# =============================================================================


def lhs_dimension():                  # Dynamic dimension of LHS - depending on no. of Vars saved as "dimension"
    cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                       axis='rows')  # must stay here (in getinput.py) for LHS-Dimension / S_ren!!!
    cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'cd_empty', 'Em_elBatt', 'Em_elVC', 'L',
                                            'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],axis='rows')
    range_length = pd.concat([cc_bev, cg_bev])  # ZUSAMMENFÜHREN NACH GLEICHEN COLUMNS
    dim = (len(range_length))  # Length of Variable list # TODO: len(range_variablen)
    return dim


def latin_hype(dimension, n):  # n = number of samples
    points = pyDOE.lhs(dimension, samples=n*4)
    return points  # output.type = array


# =============================================================================
# Choose Vehicle Class
# =============================================================================


def veh_class_sel():              # saved as "class_sel"
    veh_class = int(input("Select Vehicle Class:\n"
                          "1: Compact Cars - 2: SUVs - 3: LDVs (Light Duty Vehicles) \n"))
    return veh_class


# =============================================================================
# Verrechnen der LHS Ergebnisse mit Eingangsvariablen -> var_final entstehen      LHS!
# =============================================================================
def var_final(p, dimension, class_sel):
    propType = ['BEV', 'FCEV', 'PHEV', 'ICEV']
    var_all = []
    global vehicle
    for vehicle in range(len(propType)):                               # Durchlauf jedes propTypes
        gV = get_variables(class_sel, vehicle)                          # holt die Values aus getVariables
        lhs_items = 0                                                  # TODO: muss bei PHEV evtl verändert werden
        var_array = []

        if vehicle == 2:                 # PHEV #
            for r in range(n):
                var_list = []
                dual = 0                                  # Changes getVariable from BEV to ICEV
                while dual <= 3:                           # 0 ^= BEV
                    gV_alt = get_variables(class_sel, dual)
                    m = 0
                    t = 1
                    for k in range(dimension):  # alle Range-Werte mit reihe des LHS multiplizieren
                        var_max = gV_alt.iloc[m][t]  # bestimmung des max Wertes der eingegebenen Range
                        t -= 1
                        var_min = gV_alt.iloc[m][t]  # bestimmung des min Wertes der eingegebenen Range
                        t += 1
                        var = (p.item(lhs_items) * (
                                    var_max - var_min)) + var_min  # Verrechnen der Variablen mit LHS Ergebnissen in var
                        var_list.append(var)  # Anhängen der Parameter an liste
                        lhs_items += 1
                        m += 1
                    dual += 3           # Erhöhung um 3 (3 ^= ICEV)
                var_array.append(var_list)
            var_array = np.around(var_array, decimals=4)

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
                                                                                # propType Variablen
    return var_all


def get_variables(class_sel, vehicle):
    global lhs_vals
    if class_sel == 1:                                  # compact car #   cc = changed compact
        if vehicle == 0:    # BEV
            cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                    'Em_elBatt', 'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],
                                                   axis='rows')
            lhs_vals = pd.concat([cc_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cc_fcev = gin.changed_compact().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelH2','C_batt', 'C_fc'],
                                                    axis='rows')
            lhs_vals = pd.concat([cc_fcev, cg_fcev])

        elif vehicle == 2:  # vehicle in getVariable never gets 2!! (see var Final dual loop)
            pass

        # elif vehicle == 2:  # PHEV

        elif vehicle == 3:  # ICEV
            cc_icev = gin.changed_compact().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'],
                                                    axis='rows')
            cg_icev = gin.changed_general().reindex(['C3_synth', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                                                     'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cc_icev, cg_icev])

    elif class_sel == 2:                              # midsize SUV #       cs = changed suv
        if vehicle == 0:    # BEV
            cs_bev = gin.changed_suv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                    'Em_elBatt', 'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],
                                                   axis='rows')
            lhs_vals = pd.concat([cs_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cs_fcev = gin.changed_suv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(['C3_h2', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                                                    axis='rows')
            lhs_vals = pd.concat([cs_fcev, cg_fcev])

        elif vehicle == 2:
            pass

        elif vehicle == 3:  # ICEV
            cs_icev = gin.changed_suv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'],
                                                axis='rows')
            cg_icev = gin.changed_general().reindex(['C3_synth', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                                                     'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cs_icev, cg_icev])

    elif class_sel == 3:                              # Light Duty Vehicle #       cl = changed ldv
        if vehicle == 0:    # BEV
            cl_bev = gin.changed_ldv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                    'Em_elBatt', 'L', 'D', 'r', 'C_fuelEl', 'C_batt','C_fcEmpty'],
                                                   axis='rows')
            lhs_vals = pd.concat([cl_bev, cg_bev])

        elif vehicle == 1:  # FCEV
            cl_fcev = gin.changed_ldv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(['C3_h2', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                                                    axis='rows')
            lhs_vals = pd.concat([cl_fcev, cg_fcev])

        elif vehicle == 2:
            pass

        elif vehicle == 3:  # ICEV
            cl_icev = gin.changed_ldv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(['C3_synth', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                                                     'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cl_icev, cg_icev])

    else:
        print('Wrong Input! \n')
        veh_class_sel()                               # Erneute Eingabe der Fahrzeugklasse
    return lhs_vals


#################################################################################
# ============================================================================= #
# Definition of Classes (Calculations)                                          #
# ============================================================================= #
#################################################################################
class LCE:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def fuel_cycle(self):
        # FuelCycle Emissions
        if vehicle == 0 or vehicle == 1 or vehicle == 3:  # trennung von PHEV. Calculation andere
            e_fc = self.C3 * self.FE * self.Em_elFC * self.w_h2 * self.w_synth + self.C5 * self.FE
            # print('C3: {}, FE: {}, Em_elFC: {}, w_h2: {}, w_synth: {}, C5: {}'.format(self.C3, self.FE, self.Em_elFC,
            #                                                                      self.w_h2, self.w_synth, self.C5))
            # print('e_fc_normal: {}'.format(e_fc))
            return e_fc

    def calc_lce(self, e_fc):
        # Vehicle Cycle Emissions
        m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.E_batt - self.X12 * self.P_fc
        e_vc = self.X2 + self.X3 * self.Em_elVC + m_scal * (self.X4 + self.X5 * self.Em_elVC) + self.P_batt * (
                self.X7 + self.X8 * self.Em_elBatt) + self.E_batt * (
                       self.X10 + self.X11 * self.Em_elBatt) + self.P_fc * (self.X13 + self.X14 * self.Em_elFC)
        # print('e_vc: {}'.format(e_vc))
        e_lce = (e_vc / (self.L * self.D) + e_fc)
        # print('e_lce: {}\n'.format(e_lce))
        return e_lce


class FuelCycle_phev():                             # EXTRA FUELCYCLE CLASS FOR PHEV
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def fuel_cycle_phev(self, **kwargs):
        self.cs = (100 - self.cd_bev)/100
        # Calc of ICEV FuelCycle
        e_fc_cs = self.C3_icev * self.FE_icev * self.Em_elFC * self.w_h2 * self.w_synth + self.C5_icev * self.FE_icev
        # Calc of BEV FuelCycle
        e_fc_cd = self.C3_bev * self.FE_bev * self.Em_elFC * self.w_h2 * self.w_synth + self.C5_bev * self.FE_bev
        self.e_fc = ((e_fc_cs * self.cs) + (e_fc_cd * self.cd_bev))
        #print('e_fc_phev: {}'.format(self.e_fc))
        return self.e_fc

    def new_phev_vals(self): # TODO: 1.26 ??? Faktor klären!
        FE = (self.FE_icev * self.cs) + (self.FE_bev * self.cd_bev * 1.26)  # Fuel Economy Convversion FE/2 (cd)
        E_batt = self.E_batt_bev
        P_batt = self.P_batt_bev
        P_fc = self.P_fc_bev
        C3 = self.C3_icev * self.cs + self.C3_bev * self.cd_bev
        C5 = self.C5_icev * self.cs + self.C5_bev * self.cd_bev
        Em_elFC = self.Em_elFC
        Em_elVC = self.Em_elVC
        cd = self.cd_bev
        Em_elBatt = self.Em_elBatt
        L = self.L
        D = self.D
        r = self.r
        C_fuel = self.C_fuel_icev * self.cs + self.C_fuel_bev* self.cd
        C_batt = self.C_batt_bev
        C_fc = self.C_fc_bev
        phev_vals = [FE, E_batt, P_batt, P_fc, C3, C5, Em_elFC, Em_elVC, cd, Em_elBatt, L, D, r, C_fuel, C_batt, C_fc]
        return phev_vals


class TCO:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def calc_tco(self):
        sum_tco = 0
        for years in range(1, int(round(self.L+1))):  # Bildung der Summe               TODO: Schleife testen! L+1  ???
            Eq = ((self.C_fuel * self.FE) + (self.C_main / self.D)) / (1 + self.r) ** (years - 1)
            sum_tco += Eq
        c_veh = self.C_msrp + ((self.C_batt * self.P_batt) - (self.C_battSet * self.P_battSet)) * (1/self.CF) + \
                ((self.C_batt * self.E_batt) - (self.C_battSet * self.E_battSet)) + \
                ((self.C_fc * self.P_fc) - (self.C_fcSet * self.P_fcSet))-self.S_ren
        # print('c_veh: {} €'.format(c_veh))
        # print('sum_tco: {} €/km\n'.format(sum_tco))
        c_tco = (c_veh / (self.L * self.D)) + sum_tco
        return c_tco


#################################################################################
# ============================================================================= #
# Berechnung des results mit varFinal variablen                                 #
# ============================================================================= #
#################################################################################
def result_calc(var, class_sel):
    all_para_keys = ['FE', 'E_batt', 'P_batt', 'P_fc', 'C3', 'C5', 'Em_elFC', 'Em_elVC', 'cd', 'Em_elBatt', 'L', 'D',
                     'r', 'C_fuel', 'C_batt', 'C_fc', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10',
                     'X11', 'X12', 'X13', 'X14', 'C_main', 'm_curb', 'C_msrp', 'P_battSet', 'E_battSet', 'P_fcSet',
                     'C_battSet', 'C_fcSet', 'CF', 'w_h2', 'w_synth','S_ren']

    result = np.zeros(shape=(0, 2))

    vehicle = 0
    if class_sel == 1:            # Compact
        countType = 0

    elif class_sel ==2:           # SUV
        countType = 1

    elif class_sel == 3:          # LDV
        countType = 2

    while countType < len(gin.x_vals()):            # zähler durch fix vals of class (bev, fcev, phev, icev)
        lhs_lists = var[vehicle]                    # alle ergebnis listen von einem propType
        x_vals = list(gin.x_vals().iloc[countType])
        spec_vals = list(gin.spec_vals().iloc[countType])
        x_vals.extend(spec_vals)          # hier sind alle fix vals
        single_res = np.zeros(shape=(n, 2))
        for list_num in range(n):          # changed from 'len(lhs_lists)' to 'n'
            if vehicle == 2:
                all_para_phev = ['FE_bev', 'E_batt_bev', 'P_batt_bev', 'P_fc_bev', 'C3_bev', 'C5_bev', 'Em_elFC',
                                 'Em_elVC', 'cd_bev', 'Em_elBatt', 'L', 'D', 'r','C_fuel_bev','C_batt_bev','C_fc_bev',
                                 'FE_icev','E_batt','P_batt','P_fc', 'C3_icev', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd',
                                 'Em_elBatt', 'L', 'D', 'r', 'C_fuel_icev', 'C_batt', 'C_fc','X1', 'X2', 'X3', 'X4',
                                 'X5', 'X6', 'X7', 'X8', 'X9', 'X10','X11', 'X12', 'X13', 'X14', 'C_main', 'm_curb',
                                 'C_msrp', 'P_battSet', 'E_battSet', 'P_fcSet', 'C_battSet', 'C_fcSet', 'CF', 'w_h2',
                                 'w_synth','S_ren']
                all_phev_lhs = list(lhs_lists[list_num])
                if booleanCheckbox == 1 and (vehicle == 0 or vehicle == 1):  # Check if theres a Subsituization
                    S_ren = 4000
                elif booleanCheckbox == 1 and (vehicle == 2):
                    S_ren = 3000
                else:
                    S_ren = 0.0
                all_phev_lhs.extend(x_vals)
                lhs_dict = dict(zip(all_para_phev, all_phev_lhs))
                e_inst = FuelCycle_phev(**lhs_dict)
                e_fc_inst = e_inst.fuel_cycle_phev()                  # e_fc von PHEV hier

                phev_vals = list(e_inst.new_phev_vals())
                phev_vals.extend(x_vals)
                phev_vals.append(S_ren)
                lhs_dict = dict(zip(all_para_keys, phev_vals))

                lce_inst = LCE(**lhs_dict)

            elif vehicle == 0 or vehicle == 1 or vehicle == 3:
                all_values = list(lhs_lists[list_num])  # should be one single list of lhs_variable_results
                all_values.extend(x_vals)        # ALL NEEDED VARS ARE HERE NOW
                if booleanCheckbox == 1 and (vehicle == 0 or vehicle == 1):          # Check if theres a Subsituization
                    S_ren = 4000
                elif booleanCheckbox == 1 and (vehicle == 2):
                    S_ren = 3000
                else:
                    S_ren = 0.0
                all_values.append(S_ren)
                lhs_dict = dict(zip(all_para_keys, all_values))
                lce_inst = LCE(**lhs_dict)
                e_fc_inst = lce_inst.fuel_cycle()

            tco_inst = TCO(**lhs_dict)
            e_lce_res = lce_inst.calc_lce(e_fc_inst)     #??
            c_tco_res = tco_inst.calc_tco()

            # Hier alle ergebnisse von BEV bzw. FCEV etc
            single_res[list_num] = [np.around(c_tco_res, decimals=4), np.around(e_lce_res, decimals=4)]

        result = np.append(result, single_res, axis=0)    # Hier gesamtergebnis

        # append to a longer list
        countType+=3            # Sprung von compact_bev auf compact_fcev auf compact_phev ...
        vehicle +=1                                 # erhöhung -> lhs_lists bev -> fcev
    result = np.around(result, decimals=4)
    return result


# =============================================================================
# Plot results
# =============================================================================
class SaveResults():
    def __init__(self, res, parent=None):
        self.res = res
        self.save_csv()


    def save_csv(self):
        # SAVE all results to results/result.csv
        if not os.path.exists('results/'):
            os.makedirs('results/')
        with open("results/result.csv", 'w+') as fp:
            a = csv.writer(fp, delimiter=";")
            a.writerows(map(lambda t: ("%.4f" % t[0], "%.4f" % t[1]), self.res))

        # SAVE propType Results to base-temp folder
        if not os.path.exists('temp/'):
            os.makedirs('temp/')
        bev_points = self.res[:n]
        with open("temp/bev_result_temp.csv", "w+") as csv_count:
            csvWriter = csv.writer(csv_count, delimiter=';')
            csvWriter.writerows(bev_points)
        fcev_points = self.res[n:(n * 2)]
        with open("temp/fcev_result_temp.csv", "w+") as csv_count:
            csvWriter = csv.writer(csv_count, delimiter=';')
            csvWriter.writerows(fcev_points)
        phev_points = self.res[(2 * n):(n * 3)]
        with open("temp/phev_result_temp.csv", "w+") as csv_count:
            csvWriter = csv.writer(csv_count, delimiter=';')
            csvWriter.writerows(phev_points)
        icev_points = self.res[(3 * n):(n * 4)]
        with open("temp/icev_result_temp.csv", "w+") as csv_count:
            csvWriter = csv.writer(csv_count, delimiter=';')
            csvWriter.writerows(icev_points)

class PlotClass():
    def __init__(self, border=True, title = 'irgendwas', name='blabla',parent=None):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        mw.resize(1000, 800)
        view = pg.GraphicsLayoutWidget()
        mw.setCentralWidget(view)
        mw.setWindowTitle('OVEmAt - Open Vehicle Emission Analysis Tool')
        self.plt = view.addPlot()
        # X Axis Settings
        self.plt.setLabel('bottom', text='Total Cost of Ownership', units='€ / km')
        # Y Axis Settings
        self.plt.setLabel('left', text='Lifecycle Emissions', units='gGHG / km')

        self.plt.showGrid(True, True, alpha=.5)
        self.legend = pg.LegendItem((100,60), offset=(-30,30))  # args are (size, offset)
        self.legend.setParentItem(self.plt.graphicsItem())  # Note we do NOT call plt.addItem in this case

        # Set Climate Goal lines
        #InfiniteLine.__init__()
        self.plt.addLine(x=None, y=200, z=None)  # Ziel 2030: 60 gGHG/km
        self.plt.addLine(x=None, y=120, z=None)  # Aim 2040: .. gGHG/km

        self.plt.setMenuEnabled(enableMenu=True, enableViewBoxMenu='same')

        # Menubar
        self.menubar = QtGui.QMenuBar(mw)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 22))
        mw.setMenuBar(self.menubar)

        # Status Bar
        self.statusbar = QtGui.QStatusBar(mw)
        mw.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(mw)

        self.plotting()

    def plotting(self):
        # self.plt.scene().minDragTime = 0  # let us simulate mouse drags very quickly.
        # vline = self.plt.addLine(x=0, movable=True)
        #
        # self.plt.addItem(vline)
        # hline = self.plt.addLine(y=0, movable=True)
        # hline2 = self.plt.addLine(y=-1, movable=False)
        # self.plt.setXRange(-10, 10)
        # self.plt.setYRange(-10, 10)


        # SPLIT RESULTS
        x = end_result[:, 0]
        # print(x)
        y = end_result[:, 1]
        # print(y)

        now = pg.ptime.time()

        # Create Scatter Plot
        point_size = 12
        # BEV
        plot_bev = pg.ScatterPlotItem(x[:n], y[:n], size=point_size, pen=pg.mkPen(None),
                                  symbol='x', brush='cd5959', name='BEV')                              # red
        # FCEV
        plot_fcev = pg.ScatterPlotItem(x[n:n * 2], y[n:n * 2], size=point_size, pen=pg.mkPen(None),
                                  symbol='x', brush='5a9fcd', name ='FCEV')                            # blue
        # PHEV
        plot_phev = pg.ScatterPlotItem(x[n * 2:n * 3], y[n * 2:n * 3], size=point_size, pen=pg.mkPen(None),
                                  symbol='x', brush='ea8f20', name='PHEV')                            # orange
        # ICEV
        plot_icev = pg.ScatterPlotItem(x[n * 3:n * 4], y[n * 3:n * 4], size=point_size, pen=pg.mkPen(None),
                                  symbol='x', brush='b2cd5b', name='ICEV')                            # green

        # pfill = pg.FillBetweenItem(plot_icev, plot_fcev, brush='59cdc1')

        # Adding Plots to window plt
        self.plt.addItem(plot_bev, name='BEV')
        self.plt.addItem(plot_fcev, name='FCEV')
        self.plt.addItem(plot_phev, name='PHEV')
        self.plt.addItem(plot_icev, name='ICEV')
        # self.plt.addItem(pfill, name='FILL')

        # Adding Legend items to legendview l
        self.legend.addItem(plot_bev, name='BEV')
        self.legend.addItem(plot_fcev, name='FCEV')
        self.legend.addItem(plot_phev, name='PHEV')
        self.legend.addItem(plot_icev, name='ICEV')
        print('plot time: {} sec'.format(pg.ptime.time() - now))


def run(n):
    # Call Functions
    while True:
        try:
            class_sel = veh_class_sel()
        except ValueError:
            print('Value Error! Hit a Number 1 - 3\n')
        else:
            break

    now = pg.ptime.time()
    dimension = lhs_dimension()
    # print(timeit.timeit(lhs_dimension()))
    print('dimension time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    p = latin_hype(dimension, n)
    print('LatinHype time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    var = var_final(p, dimension, class_sel)
    print('varFinal time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    res = result_calc(var, class_sel)
    print('resultCalc time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    SaveResults(res)
    print('SaveResult time: {} sec'.format(pg.ptime.time() - now))

    return res


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Number of repeats ( Todo: test it!)
    n = 200

    end_result = run(n)

    # Make App
    app = QtGui.QApplication(sys.argv)
    mw = QtGui.QMainWindow()

    w = PlotClass(end_result)

    mw.show()
    sys.exit(app.exec_())
