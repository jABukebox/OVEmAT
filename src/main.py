#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################################
# ===========================    OVEmAT    ==================================== #
#                'Open Vehicle Emission Analysis Tool'                          #
#             < --------------------------------------- >                       #
#            Calculated with Latin Hypercube Sampling (LHS)                     #
# ============================================================================= #
#################################################################################

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pyDOE as pyDOE
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.exporters
from PyQt5 import QtCore, QtGui
from src.functions import getinput as gin
import os
import sys
import csv
from scipy.spatial import ConvexHull
#import matplotlib.pyplot as plt



# Todo: boolean muss durch checkbox ersetzt werden
# todo: FE_phev_cd, FE_phev_cs
global booleanCheckbox
booleanCheckbox = 1

# =============================================================================
# Latin Hypercube Calculation
# =============================================================================


def lhs_dimension():                     # Dynamic dimension of LHS - depending on no. of Vars saved as "dimension"
    cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'],
                                           axis='rows')  # for LHS-Dimension / s_ren!!!
    cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'cd_empty', 'cd', 'Em_elBatt', 'Em_elVC',
                                            'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'], axis='rows')  # 17
    range_length = pd.concat([cc_bev, cg_bev])  # concatinate all needed lhs-variables
    dim = (len(range_length))                   # Length of Variable list
    return dim


def latin_hype(dimension, n):                   # n = number of samples
    points = pyDOE.lhs(dimension, samples=n*4)
    return points  # Actual creation of LHS-Samples


# =============================================================================
# Choose Vehicle Class
# =============================================================================


def veh_class_sel():                                                # saved as "class_sel"
    veh_class = int(input("Select Vehicle Class:\n"
                          "1: Compact Cars - 2: SUVs - 3: LDVs (Light Duty Vehicles) \n"))
    return veh_class


# =============================================================================
# Multiplication of LHS-Samples with set Variable Ranges -> var_final created
# =============================================================================


def final_variables(p, dimension, class_sel):
    prop_type = ['BEV', 'FCEV', 'PHEV', 'ICEV']
    var_all = []
    global vehicle
    for vehicle in range(len(prop_type)):                               # passing of every prop_type
        g_v = get_variables(class_sel, vehicle)                         # gets the Values from get_variables
        lhs_items = 0                                                   # TODO: muss bei PHEV evtl verändert werden
        var_array = []

        if vehicle == 2:                                        # PHEV #
            for r in range(n):
                var_list = []
                dual = 0                                            # Changes getVariable from BEV to ICEV
                while dual <= 3:                                    # 0 ^= BEV
                    g_v_alt = get_variables(class_sel, dual)
                    m = 0
                    t = 1
                    for k in range(dimension):                      # multiply all range-values with row of LHS
                        var_max = g_v_alt.iloc[m][t]                # determine max value of set range
                        t -= 1
                        var_min = g_v_alt.iloc[m][t]                # determine min value of set range
                        t += 1
                        var = (p.item(lhs_items) * (
                                    var_max - var_min)) + var_min   # Allocation of variables with LHS results in var

                        var_list.append(var)                        # append Parameter to list
                        lhs_items += 1
                        m += 1
                    dual += 3                                       # increasing of 3 (3 => ICEV)
                var_array.append(var_list)
            var_array = np.around(var_array, decimals=4)

        else:                                                       # BEV, FCEV, ICEV #
            for r in range(n):                                      # Counter of LHS-loop
                var_list = []                                       # initialize var_list
                                                                    # all parameters per 'n' should be saved here
                m = 0                                           # row / zeile
                t = 1                                           # column / spalte
                for k in range(dimension):                          # all range-values multiplied with row of LHS
                    var_max = g_v.iloc[m][t]                        # determine max value of set range
                    t -= 1
                    var_min = g_v.iloc[m][t]                        # determine min value of set range
                    t += 1
                    var = (p.item(lhs_items) * (var_max - var_min)) + var_min   # calculation of variables with LHS

                    var_list.append(var)                                        # append Parameter to list
                    lhs_items += 1
                    m += 1
                var_array.append(var_list)                                      # Var_list gets appended to var_array
            var_array = np.around(var_array, decimals=4)                        # round numbers
        var_all.append(var_array)                                               # saving all calculated propType vars
    return var_all


def get_variables(class_sel, vehicle):
    global lhs_vals
    if class_sel == 1:                                  # compact car #   cc = changed compact
        if vehicle == 0:                                        # BEV
            cc_bev = gin.changed_compact().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd',
                                                    'Em_elBatt', 'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],
                                                   axis='rows')
            lhs_vals = pd.concat([cc_bev, cg_bev])
            #print("bev_lhs_vals:\n {}".format(lhs_vals))

        elif vehicle == 1:                                      # FCEV
            cc_fcev = gin.changed_compact().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                                                    axis='rows')
            lhs_vals = pd.concat([cc_fcev, cg_fcev])

        elif vehicle == 2:                                      # PHEV
            pass

        elif vehicle == 3:                                      # ICEV
            cc_icev = gin.changed_compact().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'],
                                                    axis='rows')
            cg_icev = gin.changed_general().reindex(['C3_synth', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                                                     'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cc_icev, cg_icev])

    elif class_sel == 2:                              # midsize SUV #       cs = changed suv
        if vehicle == 0:                                        # BEV
            cs_bev = gin.changed_suv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd',
                                                    'Em_elBatt', 'L', 'D', 'r', 'C_fuelEl', 'C_batt', 'C_fcEmpty'],
                                                   axis='rows')
            lhs_vals = pd.concat([cs_bev, cg_bev])

        elif vehicle == 1:                                      # FCEV
            cs_fcev = gin.changed_suv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(['C3_h2', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                                                    axis='rows')
            lhs_vals = pd.concat([cs_fcev, cg_fcev])

        elif vehicle == 3:                                      # ICEV
            cs_icev = gin.changed_suv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(['C3_synth', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                                                     'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cs_icev, cg_icev])

    elif class_sel == 3:                              # Light Duty Vehicle #       cl = changed ldv
        if vehicle == 0:                                        # BEV
            cl_bev = gin.changed_ldv().reindex(['FE_batt', 'E_batt', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_bev = gin.changed_general().reindex(['C3_batt', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd',
                                                    'Em_elBatt', 'L', 'D', 'r', 'C_fuelEl', 'C_batt','C_fcEmpty'],
                                                   axis='rows')
            lhs_vals = pd.concat([cl_bev, cg_bev])

        elif vehicle == 1:                                      # FCEV
            cl_fcev = gin.changed_ldv().reindex(['FE_h2', 'E_battEmpty', 'P_batt', 'P_fc'], axis='rows')
            cg_fcev = gin.changed_general().reindex(['C3_h2', 'C5_empty', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelH2', 'C_batt', 'C_fc'],
                                                    axis='rows')
            lhs_vals = pd.concat([cl_fcev, cg_fcev])

        elif vehicle == 3:                                      # ICEV
            cl_icev = gin.changed_ldv().reindex(['FE_synth', 'E_battEmpty', 'P_battEmpty', 'P_fcEmpty'], axis='rows')
            cg_icev = gin.changed_general().reindex(['C3_synth', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                                     'Em_elBatt', 'L', 'D', 'r', 'C_fuelSynth', 'C_battEmpty',
                                                     'C_fcEmpty'], axis='rows')
            lhs_vals = pd.concat([cl_icev, cg_icev])

    else:
        print('Wrong Input! \n')
        veh_class_sel()                               # repeat selection of vehicle class
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

    def fuel_cycle(self):                                       # FuelCycle Emissions
        if vehicle == 0 or vehicle == 1 or vehicle == 3:            # Seperate prop Types from PHEV
            e_fc = (100/self.C3) * (self.FE/100) * self.Em_elFC * self.w_h2 * self.w_synth + self.C5 * (self.FE/100)
            return e_fc

    def vehicle_cycle(self):                                    # Vehicle Cycle Emissions
        m_scal = self.m_curb - self.X1 - self.X6 * self.P_batt - self.X9 * self.E_batt - self.X12 * self.P_fc
        e_vc = self.X2 + self.X3 * self.Em_elVC + m_scal * (self.X4 + self.X5 * self.Em_elVC) + self.P_batt * (
                self.X7 + self.X8 * self.Em_elBatt) + self.E_batt * (
                       self.X10 + self.X11 * self.Em_elBatt) + self.P_fc * (self.X13 + self.X14 * self.Em_elFC)
        return e_vc

    def calc_lce(self, e_fc, e_vc):
        e_lce = (e_vc / (self.L * self.D) + e_fc)
        return e_lce


class FuelCyclePHEV:                                          # EXTRA FuelCycle CLASS FOR PHEV
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def fuel_cycle_phev(self, **kwargs):
        self.cd_phev = self.cd_phev/100
        self.cs = (1 - self.cd_phev)

        FE_bev = self.FE_bev * gin.fe_cd_x()            # TODO: Zahl rausnehmen - change FE_bev to self.FE_bev

        # Calc of ICEV FuelCycle
        e_fc_cs = (100/self.C3_icev) * (self.FE_icev/100) * self.Em_elFC * self.w_synth + self.C5_icev * (self.FE_icev/100)

        # Calc of BEV FuelCycle
        e_fc_cd = (100/self.C3_bev) * (FE_bev/100) * self.Em_elFC + self.C5_bev * (FE_bev/100)  # w_bev = 1 -> not needed
        e_fc = ((e_fc_cs * self.cs) + (e_fc_cd * self.cd_phev))
        return e_fc

    def new_phev_vals(self):  # TODO: 1.26 ??? Faktor klären! - phev_fac  * self.phev_fac
        FE = (self.FE_icev * self.cs) + (self.FE_bev * self.cd_phev * 1.5)  # Fuel Economy Conversion FE/2 (cd)
        E_batt = self.E_batt_bev
        P_batt = self.P_batt_bev
        P_fc = self.P_fc_bev
        C3 = self.C3_icev * self.cs + self.C3_bev * self.cd_phev
        C5 = self.C5_icev * self.cs + self.C5_bev * self.cd_phev
        Em_elFC = self.Em_elFC
        Em_elVC = self.Em_elVC
        cd = self.cd_empty
        cd_phev = self.cd_phev
        Em_elBatt = self.Em_elBatt
        L = self.L
        D = self.D
        r = self.r
        C_fuel = self.C_fuel_icev * self.cs + self.C_fuel_bev * self.cd_phev
        C_batt = self.C_batt_bev
        C_fc = self.C_fc_bev
        phev_vals = [FE, E_batt, P_batt, P_fc, C3, C5, Em_elFC, Em_elVC, cd, cd_phev, Em_elBatt, L, D, r, C_fuel, C_batt, C_fc]
        return phev_vals


class TCO:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def calc_tco(self):
        sum_tco = 0
        for years in range(1, int(round(self.L+1))):  # creating sum
            equation = ((self.C_fuel * (self.FE/100)) + (self.C_main / self.D)) / (1 + self.r) ** (years - 1)
            equation = np.around(equation, decimals=4)
            sum_tco += equation

        c_veh = self.C_msrp + ((self.C_batt * self.P_batt) - (self.C_battSet * self.P_battSet)) * (1/self.CF) + \
            ((self.C_batt * self.E_batt) - (self.C_battSet * self.E_battSet)) + \
            ((self.C_fc * self.P_fc) - (self.C_fcSet * self.P_fcSet)) - self.s_ren

        c_tco = (c_veh / (self.L * self.D)) + sum_tco
        return c_tco, sum_tco, c_veh

    def calc_tco_phev(self):

        ## BEV
        sum_tco_cd = 0
        FE_cd = self.FE_bev * gin.fe_cd_x()                      # TODO: take numbers out code
        for years in range(1, int(round(self.L + 1))):  # creating sum              # splitten - 2 x summe
            equation = ((self.C_fuel_bev * (FE_cd / 100)) + (self.C_main / self.D)) / (1 + self.r) ** (years - 1)
            sum_tco_cd += equation

        ## ICEV
        sum_tco_cs = 0
        FE_cs = self.FE_icev * gin.fe_cs_x()
        for years in range(1, int(round(self.L + 1))):  # creating sum              # splitten - 2 x summe
            equation = ((self.C_fuel_icev * (FE_cs / 100)) + (self.C_main / self.D)) / (1 + self.r) ** (years - 1)
            sum_tco_cs += equation

        sum_tco = sum_tco_cd + sum_tco_cs

        # print("FE_bev: {}\t FE_icev: {}".format(FE_cd, FE_cs))

        c_veh = self.C_msrp + ((self.C_batt * self.P_batt) - (self.C_battSet * self.P_battSet)) * (1 / self.CF) + \
                ((self.C_batt * self.E_batt) - (self.C_battSet * self.E_battSet)) + \
                ((self.C_fc * self.P_fc) - (self.C_fcSet * self.P_fcSet)) - self.s_ren

        c_tco = (c_veh / (self.L * self.D)) + sum_tco
        return c_tco, sum_tco, c_veh


#################################################################################
# ============================================================================= #
# Berechnung des results mit varFinal variablen                                 #
# ============================================================================= #
#################################################################################
def result_calc(var, class_sel, dimension):
    all_para_keys = ['FE', 'E_batt', 'P_batt', 'P_fc', 'C3', 'C5', 'Em_elFC', 'Em_elVC', 'cd', 'cd_phev', 'Em_elBatt', 'L', 'D',
                     'r', 'C_fuel', 'C_batt', 'C_fc', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10',
                     'X11', 'X12', 'X13', 'X14', 'C_main', 'm_curb', 'C_msrp', 'P_battSet', 'E_battSet', 'P_fcSet',
                     'C_battSet', 'C_fcSet', 'CF', 'w_h2', 'w_synth', 's_ren']

    result = np.zeros(shape=(0, 2))
    result_all = np.zeros(shape=(0, 6))

    all_values = []
    vehicle_type = 0

    if class_sel == 1:            # Compact
        count_type = 0

    elif class_sel == 2:           # SUV
        count_type = 1

    elif class_sel == 3:          # LDV
        count_type = 2

    while count_type < len(gin.x_vals()):               # count through fix vals of class (bev, fcev, phev, icev)
        lhs_lists = var[vehicle_type]                        # all result lists of one propType

        x_vals = list(gin.x_vals().iloc[count_type])
        spec_vals = list(gin.spec_vals().iloc[count_type])
        x_vals.extend(spec_vals)                        # all fix vals saved here
        single_res = np.zeros(shape=(n, 2))
        single_all_res = np.zeros(shape=(n, 6))
        for list_num in range(n):                       # changed from 'len(lhs_lists)' to 'n'
            tco_res, lce_res, tco_capex, tco_opex, e_fc, e_vc, lhs_dict = 0,0,0,0,0,0,0
            if vehicle_type == 2:
                all_para_phev = ['FE_bev', 'E_batt_bev', 'P_batt_bev', 'P_fc_bev', 'C3_bev', 'C5_bev', 'Em_elFC',
                                 'Em_elVC', 'cd_empty', 'cd_phev', 'Em_elBatt', 'L', 'D', 'r','C_fuel_bev', 'C_batt_bev', 'C_fc_bev',
                                 'FE_icev', 'E_batt', 'P_batt', 'P_fc', 'C3_icev', 'C5_icev', 'Em_elFC', 'Em_elVC', 'cd_empty', 'cd_empty',
                                 'Em_elBatt', 'L', 'D', 'r', 'C_fuel_icev', 'C_batt', 'C_fc','X1', 'X2', 'X3', 'X4',
                                 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'C_main', 'm_curb',
                                 'C_msrp', 'P_battSet', 'E_battSet', 'P_fcSet', 'C_battSet', 'C_fcSet', 'CF', 'w_h2',
                                 'w_synth', 's_ren']  # 58 vals - 60 with 2 x cd_phev
                all_phev_lhs = list(lhs_lists[list_num])

                if booleanCheckbox == 1 and (vehicle_type == 0 or vehicle_type == 1):  # Check if there is a subsidy
                    s_ren = gin.sub_big()
                elif booleanCheckbox == 1 and (vehicle_type == 2):
                    s_ren = gin.sub_small()
                else:
                    s_ren = 0.0

                all_phev_lhs.extend(x_vals)
                all_phev_lhs.append(s_ren)
                lhs_dict = dict(zip(all_para_phev, all_phev_lhs))

                e_inst = FuelCyclePHEV(**lhs_dict)
                e_fc = e_inst.fuel_cycle_phev()                         # e_fc of PHEV


                ## Hier unterscheidung tco icev / bev - FE
                tco_inst = TCO(**lhs_dict)
                tco_res, tco_opex, tco_capex  = tco_inst.calc_tco_phev()                    ## tco result PHEV


                phev_vals = list(e_inst.new_phev_vals())                # updated PHEV vals
                phev_vals.extend(x_vals)
                phev_vals.append(s_ren)
                lhs_dict = dict(zip(all_para_keys, phev_vals))

                lce_inst = LCE(**lhs_dict)
                e_vc = lce_inst.vehicle_cycle()                         # e_vc of PHEV

                lce_res = lce_inst.calc_lce(e_fc, e_vc)               ## LCE


            elif vehicle_type == 0 or vehicle_type == 1 or vehicle_type == 3:
                all_vals = list(lhs_lists[list_num])          # should be one single list of lhs_variable_results
                all_vals.extend(x_vals)                       # ALL NEEDED VARS ARE HERE NOW
                if booleanCheckbox == 1 and (vehicle_type == 0 or vehicle_type == 1):  # checks if there is a subsidy
                    s_ren = gin.sub_big()
                elif booleanCheckbox == 1 and (vehicle_type == 2):
                    s_ren = gin.sub_small()
                else:
                    s_ren = 0.0
                all_vals.append(s_ren)
                lhs_dict = dict(zip(all_para_keys, all_vals))

                lce_inst = LCE(**lhs_dict)
                e_fc = lce_inst.fuel_cycle()                           # e_fc of rest
                e_vc = lce_inst.vehicle_cycle()                        # e_vc of rest
                tco_inst = TCO(**lhs_dict)
                lce_res = lce_inst.calc_lce(e_fc, e_vc)                ##### LCE
                tco_res, tco_opex, tco_capex = tco_inst.calc_tco()                         # tco result rest



            all_values.append(lhs_dict)

            # all results of BEV or FCEV etc
            single_res[list_num] = [np.around(tco_res, decimals=4), np.around(lce_res, decimals=4)]
            single_all_res[list_num] = [tco_res, lce_res, tco_capex, tco_opex, e_fc, e_vc]
            single_all_res = np.around(single_all_res, decimals=4)

        result = np.append(result, single_res, axis=0)
        result_all = np.append(result_all, single_all_res, axis=0)      # --- TOTAL RESULT ---

        # append to a longer list
        count_type += 3                                 # Jump from compact_bev to compact_fcev to compact_phev ...
        vehicle_type += 1                                    # increasing -> lhs_lists bev -> fcev

    all_values = pd.DataFrame(all_values, columns=all_para_keys)
    all_values = round(all_values, 4)
    all_values.to_csv("results/input_values.csv", sep=";")

    result = np.around(result, decimals=4)

    columns = ['TCO (€/km)', "LCE (gGHG/km)", "TCO_Capex (€)", "TCO_Opex (€/km)", "Em_fc (gGHG/km)", "Em_vc (gGHG)"]
    result_extend = np.around(result_all, decimals=4)
    result_extend = pd.DataFrame(data=result_extend, columns=columns)

    return result, result_extend, all_values


# =============================================================================
# Save Results
# =============================================================================
class SaveResults:
    def __init__(self, res, res_extend, all_values, parent=None):
        self.res = res
        self.res_extend = res_extend
        self.all_values = all_values
        self.save_csv()

    def save_csv(self):
        if not os.path.exists('results/'):
            os.makedirs('results/')

        # SAVE results to results/result.csv (LCE / TCO)
        headers = ['TCO (€/km)', "LCE (gGHG/km)"]
        with open("results/result.csv", 'w+') as fp:
            csv_writer = csv.writer(fp, delimiter=";")
            csv_writer.writerow([h for h in headers])
            csv_writer.writerows(map(lambda t: ("%.4f" % t[0], "%.4f" % t[1]), self.res))

        # SAVE results + all values to results/result_all.csv
        global all_data
        all_data = self.res_extend.join(self.all_values)
        all_data.to_csv("results/result_all.csv", sep=';', header=True)

        # SAVE propType Results to base-temp folder
        if not os.path.exists('temp/'):
            os.makedirs('temp/')

        self.bev_points = all_data[:n]
        self.bev_points.to_csv("temp/bev_result_temp.csv", sep=';', header=True)

        self.fcev_points = all_data[n:(n * 2)]
        self.fcev_points.to_csv("temp/fcev_result_temp.csv", sep=';', header=True)

        self.phev_points = all_data[(2 * n):(n * 3)]
        self.phev_points.to_csv("temp/phev_result_temp.csv", sep=';', header=True)

        self.icev_points = all_data[(3 * n):(n * 4)]
        self.icev_points.to_csv("temp/icev_result_temp.csv", sep=';', header=True)


# =============================================================================
# Plot Widget and Results
# =============================================================================

class PlotClass(QtGui.QMainWindow):
    def __init__(self, execute):
        super(QtGui.QMainWindow, self).__init__()
        self.mw = QtGui.QMainWindow()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.mw.resize(1000, 800)
        self.view = pg.GraphicsLayoutWidget()
        self.mw.setCentralWidget(self.view)
        self.mw.setWindowTitle('OVEmAt - Open Vehicle Emission Analysis Tool')
        self.plt = self.view.addPlot()
        #self.plt_add = self.view.addItem()

        # X Axis Settings
        self.plt.setLabel('bottom', text='Total Cost of Ownership', units='€ / km')
        # Y Axis Settings
        self.plt.setLabel('left', text='Lifecycle Emissions', units='gGHG / km')

        self.plt.showGrid(True, True, alpha=.5)
        self.legend = pg.LegendItem((100, 60), offset=(-30, 30))  # args are (size, offset)
        self.legend.setParentItem(self.plt.graphicsItem())  # Note we do NOT call plt.addItem in this case

        # Set Climate Goal lines
        self.plt.addLine(x=None, y=200, z=None)  # Ziel 2020: 200 gGHG/km
        self.plt.addLine(x=None, y=120, z=None)  # Aim 2030: 120 gGHG/km

        self.plt.setMenuEnabled(enableMenu=True, enableViewBoxMenu='same')

        # Menubar
        extractAction = QtGui.QAction("&Close app", self)
        extractAction.setShortcut("Ctrl+O")
        extractAction.setStatusTip("Leave the app")
        extractAction.triggered.connect(self.close_application)

        # Open Files
        openFile = QtGui.QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        # Save Files
        saveFile = QtGui.QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        self.statusBar()

        mainMenu = self.mw.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        # Status Bar
        statusbar = self.mw.statusBar()
        self.mw.setStatusBar(statusbar)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Result Points
        self.bev_points = execute[:n]
        self.fcev_points = execute[n:(n * 2)]
        self.phev_points = execute[(2 * n):(n * 3)]
        self.icev_points = execute[(3 * n):(n * 4)]

        self.plotting()

    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        file = open(name, 'r')
        self.editor()
        with file:
            text = file.read()
            self.textEdit.setText(text)

    def file_save(self):
        options = QtGui.QFileDialog.Options()
        options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, _ = QtGui.QFileDialog.getSaveFileName(self, "Save File", "",
                                                        "All Files (*);;Image Files (*.png);;Text Files (*.txt)",
                                                        options=options)

        if fileName:
            exporter = pg.exporters.ImageExporter(self.plt)
            exporter.export(fileName)
            print(fileName)

    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        #self.menu_bar()
        # self.CrossHair()

    # def menu_bar(self):
    #     self._menu = QtGui.QMenuBar(self)
    #     self._menu.setNativeMenuBar(False)
    #
    #     fileMenu = self._menu.addMenu("File")
    #     fileMenu.addAction("New")
    #     fileMenu.addAction("Open", self.openFileBrowser)
    #     fileMenu.addAction("Save", self.saveToFile)
    #     fileMenu.addAction("Save As")
    #     fileMenu.addSeparator()
    #     fileMenu.addAction("Import")
    #     fileMenu.addAction("Export")
    #
    #     nodeMenu = self._menu.addMenu("Node")
    #     nodeMenu.addAction("Create...")
    #     nodeMenu.addAction("Duplicate")
    #     nodeMenu.addAction("Delete")
    #     nodeMenu.addAction("Find...")
    #
    #     self._menu.addAction("Save", self.saveToFile)
    #
    #     self._layout.addWidget(self._menu)
    #     self.plotting()
    def close_application(self):
        sys.exit()

    def plotting(self):
            # SPLIT RESULTS
            x = execute[:, 0]
            # print(x)
            y = execute[:, 1]
            # print(y)

            now = pg.ptime.time()

            # Create Scatter Plot
            point_size = 4
            # BEV
            plot_bev = pg.ScatterPlotItem(x[:n], y[:n], size=point_size, pen=pg.mkPen(None),
                                          symbol='o', brush='cd5959', name='BEV')                              # red
            # FCEV
            plot_fcev = pg.ScatterPlotItem(x[n:n * 2], y[n:n * 2], size=point_size, pen=pg.mkPen(None),
                                           symbol='o', brush='5a9fcd', name ='FCEV')                            # blue
            # PHEV
            plot_phev = pg.ScatterPlotItem(x[n * 2:n * 3], y[n * 2:n * 3], size=point_size, pen=pg.mkPen(None),
                                           symbol='o', brush='b2cd5b', name='PHEV')                            # green
            # ICEV
            plot_icev = pg.ScatterPlotItem(x[n * 3:n * 4], y[n * 3:n * 4], size=point_size, pen=pg.mkPen(None),
                                           symbol='o', brush='ea8f20', name='ICEV')                            # orange

            ### plot Hulls
            hull_bev = np.array(self.convex_hull(self.bev_points))
            hull_fcev = np.array(self.convex_hull(self.fcev_points))
            hull_phev = np.array(self.convex_hull(self.phev_points))
            hull_icev = np.array(self.convex_hull(self.icev_points))

            # Hull Color
            color_bev = QtGui.QColor(249, 202, 202)     # f9caca
            color_bev.setAlphaF(0.5)
            color_fcev = QtGui.QColor(186, 227, 255)    # bae3ff
            color_fcev.setAlphaF(0.5)
            color_phev = QtGui.QColor(239, 249, 207)    # eff9cf
            color_phev.setAlphaF(0.5)
            color_icev = QtGui.QColor(249, 209, 159)    # f9d19f
            color_icev.setAlphaF(0.5)

            # Hull Plot
            self.plt.plot(hull_bev, pen=pg.mkPen('f9b8b8', width=3), fillLevel=0., fillBrush=pg.mkBrush(color_bev, alpha=0.5))
            self.plt.plot(hull_fcev, pen=pg.mkPen('a4d7f9', width=3), fillLevel=0., fillBrush=pg.mkBrush(color_fcev, alpha=0.5))
            self.plt.plot(hull_phev, pen=pg.mkPen('eefcbf', width=3), fillLevel=0., fillBrush=pg.mkBrush(color_phev, alpha=0.5))
            self.plt.plot(hull_icev, pen=pg.mkPen('f7c88f', width=3), fillLevel=0., fillBrush=pg.mkBrush(color_icev, alpha=0.5))

            # Adding Scatter to window plt
            self.plt.addItem(plot_bev, name='BEV')
            self.plt.addItem(plot_fcev, name='FCEV')
            self.plt.addItem(plot_phev, name='PHEV')
            self.plt.addItem(plot_icev, name='ICEV')

            # Adding Legend items to legendview l
            self.legend.addItem(plot_bev, name='BEV')
            self.legend.addItem(plot_fcev, name='FCEV')
            self.legend.addItem(plot_phev, name='PHEV')
            self.legend.addItem(plot_icev, name='ICEV')
            print('plot time: {} sec'.format(pg.ptime.time() - now))

            self.mw.show()

    def split(self, u, v, points):
        # return points on left side of UV
        return [p for p in points if np.cross(p - u, v - u) < 0]

    def extend(self, u, v, points):
        if not points:
            return []
        # find furthest point W, and split search to WV, UW
        w = min(points, key=lambda p: np.cross(p - u, v - u))
        p1, p2 = self.split(w, v, points), self.split(u, w, points)
        return self.extend(w, v, p1) + [w] + self.extend(u, w, p2)

    def convex_hull(self, points):
        # find two hull points, U, V, and split to left and right search
        u = min(points, key=lambda p: p[0])
        v = max(points, key=lambda p: p[0])
        left, right = self.split(u, v, points), self.split(v, u, points)

        # find convex hull on each side
        return [v] + self.extend(u, v, left) + [u] + self.extend(v, u, right) + [v]


# =============================================================================
# Run functions and classes
# =============================================================================

def run(n):
    # Call Functions
    global now2

    while True:
        try:
            class_sel = veh_class_sel()
        except ValueError:
            print('Value Error! Hit a Number 1 - 3\n')
        else:
            break
    now2 = pg.ptime.time()
    now = pg.ptime.time()
    dimension = lhs_dimension()
    # print(timeit.timeit(lhs_dimension()))
    print('dimension time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    p = latin_hype(dimension, n)
    print('LatinHype time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    var = final_variables(p, dimension, class_sel)
    print('varFinal time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    res, res_extend, all_values = result_calc(var, class_sel, dimension)
    print('resultCalc time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    SaveResults(res, res_extend, all_values)
    print('SaveResult time: {} sec'.format(pg.ptime.time() - now))


    return res


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Number of repeats
    n = 60

    # Call all function in run function
    execute = run(n)

    # Make App
    app = QtGui.QApplication(sys.argv)
    #mw = QtGui.QMainWindow()

    # Call PlotClass and show view
    print('ALL time: {} sec'.format(pg.ptime.time() - now2))
    w = PlotClass(execute)
    #mw.show()
    sys.exit(app.exec_())
