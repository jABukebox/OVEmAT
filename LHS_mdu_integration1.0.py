#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:22:16 2019

@author: JahBuh
"""

# =============================================================================
# LHS Loop with hard coded variables -- Umschreiben: Fct returns und parameterübergabe!
# =============================================================================

### imports
import numpy as np
#import matplotlib.pyplot as plt
import pyDOE as pyDOE
import pandas as pd
import pyqtgraph as pg
import random as rd
#import pyqtgraph.opengl as gl
import os, sys, csv






#n=1000 # Number of repeats (test)
#dimension = 4 # Dimension, bzw. Zahl der Variablen
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # Define Base Directory

# Plot von p (LHS Ergebnis) letztlich völlig unwichtig!!!!!!! 
#n = int(input('Set the Point number: '))




# =============================================================================
# Latin Hypercube Calculation - check pyDOE "criterion and samples"!!
# =============================================================================
def LatinHype(dimension, n):      # n = number of samples
    points = pyDOE.lhs(dimension, samples=n)
    return points                       # output.type = array



#p = LatinHype(n)

#print("LHS Values")
#print(p)
#print('\n')
a,b,c,d,e,f,g,h,i,j,k = 0,0,0,0,0,0,0,0,0,0,0

variablen = [a,b,c,d,e,f,g,h,i,j,k]

# =============================================================================
# Erstellung von Beispielvariablen - Werte müssen natürliche eingelesen werden
# =============================================================================
def getVariables():    
    ### Dataframe - get values from User Input 
    global var_range_sort_df
    var_get = {'Bounderies':['min','max']}
    # Schleife: for i in range(len("my_variablelist")):
    #               var_get.append{'var'+i:[rd.randrange(0,11,1),rd.randrange(20,61,1)]}          # in [] getvalues von eingabe
    var_get = {'Bounderies':['min','max'],'var1':[10,60], 'var2':[5,15],'var3':[60,100],'var4':[1,4]} #'Dictionary' -> Values have to be set from user or default
    var_range_df = pd.DataFrame(data=var_get) # create dataframe from dictionary
    var_range_sort_df = var_range_df.set_index("Bounderies") #Sort after min, max
    
    print(var_range_sort_df)
    #print(var_range_sort_df.iloc[1][0]) # Zeile * Spalte
    #print(p.item(0))
    
    return var_range_sort_df


##################################################################################################################################
# =============================================================================
# Definition of Classes (Calculations)
# =============================================================================


class FuelCycle():
    C1,C2,C3,C4,C5,C6,FE,E_elec=0,0,0,0,0,0,0,0
    def __init__(self, C1, C2, C3, C4, C5, C6, FE, E_elec):
        self.C1 = C1
        self.C2 = C2 
        self.C3 = C3
        self.C4 = C4
        self.C5 = C5
        self.C6 = C6
        self.FE = FE
        self.E_elec = E_elec
        self.calcFuelCycle
        
    def calcFuelCycle(self):
        try:
            E_fc = self.C1 + self.C2 * 1/(self.FE) + self.C3 * 1/(self.FE) * self.E_elec + self.C4 + self.C5 * 1/(self.FE) + self.C6 * 1/self.FE * self.E_elec
            return E_fc
        except: 
            print("An error has occured! Please try again!")
            
class VehicleCycle():
# FCEV2 = vehicle_cycle(35.25, 1.124, 1.074, 2.41, 2.43, 1.25, 5.01, 6.22,   0,   0,     0,     5,    56.48, 40.89(x14),24.3,      489,       40,      0,        90,       1850)
    def __init__(self, X1=0,   X2=0,  X3=0,  X4=0, X5=0, X6=0, X7=0, X8=0, X9=0, X10=0, X11=0, X12=0, X13=0, X14=0, E_elec=0, m_scal=0, P_batt=0, C_batt=0, P_fc=0, m_curb=0):
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
        self.calcVehicleCycle
        
    def calcVehicleCycle(self):
        try:
            m_scal = self.m_curb - self.X1 -self.X6 * self.P_batt - self.X9 * self.C_batt - self.X12 * self.P_fc
            E_vc = self.X2 + self.X3*self.E_elec + m_scal * (self.X4 + self.X5*self.E_elec) + self.P_batt * (self.X7 + self.X8*self.E_elec) + self.C_batt * (self.X10 + self.X11*self.E_elec) + self.P_fc * (self.X13 + self.X14*self.E_elec)
            return E_vc
        except: 
            print("An error has occured! Please try again!")
    
class TCO():           # FE may not be '0' - (ZeroDevisionError)
    def __init__(self,      C_msrp=0, C_aV=0, C_EM=0, C_Pbatt=0, C_Ebatt=0, C_FC=0, C_CM=0, C_TM=0, L=0, D=0, r=0, C_fuel=0, FE=0, C_maint=0, C_BEV=0, C_FCEV=0, C_ICEV=0, C_PHEV=0):
        # Beispiel Values FCEV): 0,  20000,    10000,  15000,     0,         3000,    0,      0,   14, 20000, 1.5,   7.4,     66,     150,      0,      0,        0,        0
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
        self.calcTCO
        
    def calcTCO(self):  
        try:
            # Hier C_BEV, C_FCEV berechnen mit C_BEV = self.C_aV + self.C_EM, self.C_Pbatt, Cself._Ebatt, self.C_FC, self.C_CM, self.C_Tm
            L=self.L+1
            y=1
            SUMME = 0
            for y in range(1, L):       # Bildung der Summe
                Eq = ((self.C_fuel / self.FE) + (self.C_maint / self.D)) / (1+self.r)**(y-1)
                SUMME = SUMME + Eq
                y =+1
            
            C_msrp = self.C_aV + self.C_BEV + self.C_FCEV + self.C_ICEV + self.C_PHEV
            C_tot = C_msrp/(self.L*self.D) + SUMME
            return C_tot
        except: 
            print("An error has occured! Please try again!")

class LCE():
    def __init__(self,E_vc, E_fc, L, D):
        self.E_vc = E_vc
        self.E_fc = E_fc
        self.L = L
        self.D = D
        self.calcLCE
    
    def calcLCE(self):
        try:
            E = (self.E_vc/(self.L*self.D)+self.E_fc)
            return E
        except:
            print("An error has occured! Please try again!")
            
# =============================================================================
# Data Input & Print
# =============================================================================
#print("Please type in the fuel_cycle values: \n") 
print('\n\n\n')              # toyota ... 

#fuel_val = (0,0,13.814,0,0,0,28.06,489)
#FCEV1 = fuel_cycle(fuel_val)

FCEV1 = FuelCycle(0,0,13.814,0,0,0,28.06,489)
#print(FCEV1)
FCEV2 = VehicleCycle(335.25, 1.124, 1.074, 2.41, 2.43, 1.25, 5.01, 6.22,0,0,0,5,56.48, 40.89,24.3,489,40,0,90,1850)
#print(FCEV2)
FCEV3 = TCO(0, 20000, 10000, 15000, 0, 3000, 0, 0, 14, 20000, 1.5, 7.4, 66, 150, 0, 0, 0, 0)       # hier darf 13. eintrag nicht 0 sein!! fehler ABFANGEN!
#print(FCEV3)
FCEV4 = LCE(VehicleCycle.calcVehicleCycle(FCEV2), FuelCycle.calcFuelCycle(FCEV1), 15, 10000)
#FCEV4 = LCE(self.E_vc, self.E_fc, 15, 10000)
#print(FCEV4)

#emp_2 = Employee('Test', 'User', '12315')

# =============================================================================
# Ausgabe
# =============================================================================

#emp_1.fullname()
print("Fuel Cycle:\t\t" + str(FuelCycle.calcFuelCycle(FCEV1))+ ' ' + "gCO_2eq / km")
print("\nVehicle Cycle:\t\t", str(VehicleCycle.calcVehicleCycle(FCEV2)) +' '+ "gCO_2eq")
print("\nTotal Cost per km:\t" + str(TCO.calcTCO(FCEV3)) +' '+ " € / km")
print("\n\nGesamte LCE:\t\t" + str(LCE.calcLCE(FCEV4)) +' '+ "gCO_2 / km")

##################################################################################################################################



# =============================================================================
# Verrechnen der LHS Ergebnisse mit Eingangsvariablen -> var_final entstehen      LHS!
# =============================================================================
def varFinal():    
    global var_array
   # print(var_range_sort_df)
    #k = 0
    r=0
    lhs_items = 0
    var_array=[]
    
    #for r in np.arange(0,n,1):
    for r in range(n):
        var_list=[]                     
        #for k in np.arange(0,dimension,1):   
        k=0
        m = 1
        t = 0
        for k in range(dimension):
            var_max = var_range_sort_df.iloc[m][t]
            m-=1
            var_min = var_range_sort_df.iloc[m][t]
            m+=1
            var = (p.item(lhs_items)*(var_max - var_min))+var_min
            var_list.append(var)
            lhs_items += 1
            t+=1
        
        var_array.append(var_list)                                  # Var_list gets appended to var_array
    var_array = np.around(var_array, decimals=4)                    # round numbers 
    #print(var_array)   
    return var_array

# =============================================================================
# Berechnung des results mit varFinal variablen
# =============================================================================
def resultCalc():
    ### erstellen eines mit Nullen gefüllten arrays
    global result
    result = np.zeros(shape=(n,2))                                  #  m * n Matrix = zeile * Spalte     
    #r = 0                                                          # laufvar. für schleife "LHS-Durchläufe"
    m = 0
    
    
    for r in range(n):        # 
        t=0
        x1 = var_array[r][t]
        t+=1
        x2 = var_array[r][t]
        x = np.around(x1 + x2, decimals=4)
        t+=1
        y1 = var_array[r][t]
        t+=1
        y2 = var_array[r][t]
        y = np.around(y1 + y2, decimals=4)
        #print(r)
        #print(x,y)
        m+=1
        result[r] = [x,y]
        #print(result[r])
        #r+=1

    result = np.around(result, decimals=4)
    #print("Result Values")
    #print(result)
    return result                           # *
    

# =============================================================================
# Plot results
# =============================================================================
class PlotClass():
    def __init__(self, parent=None):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.save_csv()
    
    def save_csv(self):                                         # create folder & file and write results
        #global result                                                           # *
        if not os.path.exists('results/'):
            os.makedirs('results/')        
        with open("results/result.csv",'w') as fp:
            a = csv.writer(fp,delimiter = ";")
            a.writerows(map(lambda t: ("%.4f" % t[0], "%.4f" % t[1]), result))
            self.plotting()

    def plotting(self):   
        self.i=0
        #global n, result
        # create the view
        self.view = pg.PlotWidget()
        self.view.resize(800,600)
        self.view.setWindowTitle('scatter plot using pyqtgraph - test')
        self.view.setAspectLocked(True)
        self.view.showGrid(True, True, alpha=.5)
        self.view.show()
        
        
        # Create Scatter Plot and add it to view
        self.plot = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color='r'), symbol = 'x', size=1)
        #self.plot = pg.gl.GLSurfacePlotItem(pen=pg.mkPen(width=5, color='r'), symbol = 'x', size=1)
        self.view.addItem(self.plot)
        
        # Convert data array into a list of dictionaries with the x,y-coordinates
        self.pos = [{'pos':result[self.i,:]} for self.i in range(n)]
        
        self.now = pg.ptime.time()
        self.plot.setData(self.pos)
    
        print('plot time: {} sec'.format(pg.ptime.time() - self.now))


#p = LatinHype(dimension, n)
#getVariables()
#a = varFinal()
#print(a)
#resultCalc()


if __name__ == '__main__':

    n = 1000  # Number of repeats (test)
    dimension = 4  # Dimension, bzw. Zahl der Variablen
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    p = LatinHype(dimension, n)

    getVariables()
    a = varFinal()

    print(a)
    resultCalc()
    app = pg.mkQApp() # main application instance
    w = PlotClass()
    #w.show()
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

