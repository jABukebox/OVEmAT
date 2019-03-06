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
from pyqtgraph.Qt import QtGui
import getinput as gin
import os
import sys
import csv
from PyQt5 import QtCore


# Todo: boolean muss durch checkbox ersetzt werden
# Todo: zahlen raus
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
                        #var = np.around(var, decimals=4)
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
                    #var = np.around(var, decimals=4)
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
            # print('C3: {}, FE: {}, Em_elFC: {}, w_h2: {}, w_synth: {}, C5: {}'.format(self.C3, self.FE, self.Em_elFC,
            #                                                                      self.w_h2, self.w_synth, self.C5))
            # print('e_fc_normal: {}'.format(e_fc))
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


class FuelCyclePHEV():                                          # EXTRA FuelCycle CLASS FOR PHEV
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def fuel_cycle_phev(self, **kwargs):
        print('cd_phev fuel cycle: {}'.format(self.cd_phev))
        self.cd_phev = self.cd_phev/100
        print("cd: {}\n".format(self.cd_phev))
        self.cs = (1 - self.cd_phev)

        print("cs: {}".format(self.cs))
        FE_bev = self.FE_bev * 1.5            # TODO: Zahl rausnehmen - change FE_bev to self.FE_bev
        #FE_icev = self.FE_icev

        # Calc of ICEV FuelCycle
        e_fc_cs = (100/self.C3_icev) * (self.FE_icev/100) * self.Em_elFC * self.w_synth + self.C5_icev * (self.FE_icev/100)

        # Calc of BEV FuelCycle
        e_fc_cd = (100/self.C3_bev) * (FE_bev/100) * self.Em_elFC + self.C5_bev * (FE_bev/100)  # w_bev = 1 -> not needed
        e_fc = ((e_fc_cs * self.cs) + (e_fc_cd * self.cd_phev))
        return e_fc

    def new_phev_vals(self):  # TODO: 1.26 ??? Faktor klären! - phev_fac  * self.phev_fac
        print("em_elBatt= {}".format(self.Em_elBatt))
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
        print("sum_tco: {}".format(sum_tco))
        c_veh = self.C_msrp + ((self.C_batt * self.P_batt) - (self.C_battSet * self.P_battSet)) * (1/self.CF) + \
            ((self.C_batt * self.E_batt) - (self.C_battSet * self.E_battSet)) + \
            ((self.C_fc * self.P_fc) - (self.C_fcSet * self.P_fcSet)) - self.s_ren
        # print('c_veh: {} €'.format(c_veh))
        # print('sum_tco: {} €/km\n'.format(sum_tco))
        c_tco = (c_veh / (self.L * self.D)) + sum_tco
        return c_tco

    def calc_tco_phev(self):
        sum_tco = 0
        for years in range(1, int(round(self.L + 1))):  # creating sum              # splitten - 2 x summe
            equation = ((self.C_fuel * (self.FE / 100)) + (self.C_main / self.D)) / (1 + self.r) ** (years - 1)
            # equation = np.around(equation, decimals=4)
            # print("equation: {}".format(equation))
            sum_tco += equation
        c_veh = self.C_msrp + ((self.C_batt * self.P_batt) - (self.C_battSet * self.P_battSet)) * (1 / self.CF) + \
                ((self.C_batt * self.E_batt) - (self.C_battSet * self.E_battSet)) + \
                ((self.C_fc * self.P_fc) - (self.C_fcSet * self.P_fcSet)) - self.s_ren
        # print('c_veh: {} €'.format(c_veh))
        # print('sum_tco: {} €/km\n'.format(sum_tco))
        c_tco = (c_veh / (self.L * self.D)) + sum_tco
        return c_tco


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
    result_all = np.zeros(shape=(0, 4))
    #all_dicts = np.zeros(shape=(n*4, dimension))
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
        single_all_res = np.zeros(shape=(n, 4))
        for list_num in range(n):                       # changed from 'len(lhs_lists)' to 'n'
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
                #print('S_REN:{}'.format(s_ren))
                lhs_dict = dict(zip(all_para_phev, all_phev_lhs))
                #print('lhs dict: \n{}'.format(lhs_dict))
                e_inst = FuelCyclePHEV(**lhs_dict)
                e_fc = e_inst.fuel_cycle_phev()                        # e_fc of PHEV
                phev_vals = list(e_inst.new_phev_vals())
                phev_vals.extend(x_vals)
                phev_vals.append(s_ren)
                lhs_dict = dict(zip(all_para_keys, phev_vals))

                e_inst = LCE(**lhs_dict)
                e_vc = e_inst.vehicle_cycle()                          # e_vc of PHEV
                lce_inst = LCE(**lhs_dict)
                e_lce_res = lce_inst.calc_lce(e_fc, e_vc)

                tco_inst = TCO(**lhs_dict)
                c_tco_res = tco_inst.calc_tco_phev()                    # tco result PHEV

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
                e_lce_res = lce_inst.calc_lce(e_fc, e_vc)
                c_tco_res = tco_inst.calc_tco()                         # tco result rest

            if not os.path.exists('results/'):
                os.makedirs('results/')

            # SAVE lhs_dict
            # headers = ['TCO (€/km)', "LCE (gGHG/km)"]
            lhs_dict = pd.DataFrame(lhs_dict.items())
            print("dataframe:\n{}".format(lhs_dict))
            lhs_dict = lhs_dict.set_index([0][0])
            #with open("results/lhs_dicts.csv", 'w+') as fp:
                #csv_writer = csv.writer(fp, delimiter=";")
                # csv_writer.writerow([h for h in headers])
                #csv_writer.writeheader()
            lhs_dict.to_csv("results/lhs_dicts.csv", sep=";")
                #csv_writer.writerow(lhs_dict.keys())
                #csv_writer.writerow(lhs_dict.values())
            #all_dicts[list_num] = lhs_dict

            # all results of BEV or FCEV etc
            single_res[list_num] = [np.around(c_tco_res, decimals=4), np.around(e_lce_res, decimals=4)]
            single_all_res[list_num] = [np.around(c_tco_res, decimals=4), np.around(e_lce_res, decimals=4), np.around(e_fc, decimals=4), np.around(e_vc, decimals=4)]

        result = np.append(result, single_res, axis=0)           # --- TOTAL RESULT ---
        result_all = np.append(result_all, single_all_res, axis=0)
        #all_values = np.append(all_values, lhs_dict, axis=0)

        # append to a longer list
        count_type += 3                                 # Jump from compact_bev to compact_fcev to compact_phev ...
        vehicle_type += 1                                    # increasing -> lhs_lists bev -> fcev
    result = np.around(result, decimals=4)
    print('single results:\n{}'.format(single_res))
    print('result:\n{}'.format(result))
    result_all = np.around(result_all, decimals=4)
    return result, result_all


# =============================================================================
# Save Results
# =============================================================================
class SaveResults:
    def __init__(self, res, res_all, parent=None):
        self.res = res
        self.res_all = res_all
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
        headers = ['TCO (€/km)', "LCE (gGHG/km)", "Em_fc (gGHG/km)", "Em_vc (gGHG)"]
        with open("results/result_all.csv", 'w+') as fp:
            csv_writer = csv.writer(fp, delimiter=";")
            csv_writer.writerow([h for h in headers])
            csv_writer.writerows(map(lambda t: ("%.4f" % t[0], "%.4f" % t[1],"%.4f" % t[2],"%.4f" % t[3]), self.res_all))

        # SAVE propType Results to base-temp folder
        if not os.path.exists('temp/'):
            os.makedirs('temp/')
        bev_points = self.res[:n]
        with open("temp/bev_result_temp.csv", "w+") as csv_count:
            csv_writer = csv.writer(csv_count, delimiter=';')
            csv_writer.writerows(bev_points)

        fcev_points = self.res[n:(n * 2)]
        with open("temp/fcev_result_temp.csv", "w+") as csv_count:
            csv_writer = csv.writer(csv_count, delimiter=';')
            csv_writer.writerows(fcev_points)

        phev_points = self.res[(2 * n):(n * 3)]
        with open("temp/phev_result_temp.csv", "w+") as csv_count:
            csv_writer = csv.writer(csv_count, delimiter=';')
            csv_writer.writerows(phev_points)

        icev_points = self.res[(3 * n):(n * 4)]
        with open("temp/icev_result_temp.csv", "w+") as csv_count:
            csv_writer = csv.writer(csv_count, delimiter=';')
            csv_writer.writerows(icev_points)


# =============================================================================
# Plot Widget and Results
# =============================================================================

class PlotClass:
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
        self.plt.addLine(x=None, y=200, z=None)  # Ziel 2020: 200 gGHG/km
        self.plt.addLine(x=None, y=120, z=None)  # Aim 2030: 120 gGHG/km

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


# =============================================================================
# Run functions and classes
# =============================================================================

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
    var = final_variables(p, dimension, class_sel)
    print('varFinal time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    res, res_all = result_calc(var, class_sel, dimension)
    print('resultCalc time: {} sec'.format(pg.ptime.time() - now))

    now = pg.ptime.time()
    SaveResults(res, res_all)
    print('SaveResult time: {} sec'.format(pg.ptime.time() - now))

    return res


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Number of repeats
    n = 10

    # Call all function in run function
    end_result = run(n)

    # Make App
    app = QtGui.QApplication(sys.argv)
    mw = QtGui.QMainWindow()

    # Call PlotClass and show view
    w = PlotClass(end_result)
    mw.show()
    sys.exit(app.exec_())
