#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:22:16 2019

@author: JahBuh
"""

import numpy as np
import matplotlib.pyplot as plt
import pyDOE as pyDOE


### Latin Hypercube
def latin_hypercube_2d_uniform(n):      # n = number of samples
    #lower_limits = np.arange(0, n)/n
    #upper_limits = np.arange(1, n+1)/n
    #points = np.random.uniform(low=lower_limits, high=upper_limits, size=[2,n]).T #n-dimensional array
    #np.random.shuffle(points[:,1])
    #return points

    points = pyDOE.lhs(2, samples=n, criterion='center')
    return points                       # output.type = array

n=5 # Number of repeats (test)

# Plot von p (LHS Ergebnis) letztlich völlig unwichtig!!!!!!! 

#n = int(input('Set the Point number: '))
p = latin_hypercube_2d_uniform(n)

print("LHS Values")
print(p)
#print('\n')

##############
# Erstellung von Beispielvariablen (max, min)
##############
### Var1                   Werte müssen natürliche eingelesen werden
var1_max = 100   # 20€
var1_min = 10   # 10€

### Var2
var2_max = 100   # gCO_2/km
var2_min = 10   # gCO_2/km

### Var3

# =============================================================================
# 
# ### erstellen eines mit Nullen gefüllten arrays
# result = np.zeros(shape=(n,2)) 
# 
# 
# i=0 # laufvar. für values in array (0 = 1. item / 1 = 2.item etc.)
# r=0 # laufvar. für schleife
# for r in np.arange(0,n,1):        # 
#     x = (p.item(i)*(var1_max - var1_min))+var1_min
#     i+=1
#     y = (p.item(i)*(var2_max - var2_min))+var2_min
#     i+=1
#     result[r] = [x,y]
#     #print(result[r])
#     r+=1
#     
# =============================================================================
# 
    
#print("Result Values")
#print(result)
#print('\n')


### Create figure
plt.figure(figsize=[5,5])
x_max,y_max = result.max(axis=0)
#print(x_max,y_max)

x_min,y_min = result.min(axis=0)


### relative achsen
#plt.xlim([(x_min-x_max/5),(x_max+x_max/5)]) # Anpassen der Achsen xmin / xmax +- 20%
#plt.ylim([(y_min-y_max/5),(y_max+y_max/5)])

### absolute Achsen
plt.xlim([0,1]) # Anpassen der Achsen xmin / xmax +- 20%
plt.ylim([0,1])

### Plot result
plt.scatter(p[:,0],p[:,1], c='r')     # scatter plot result
plt.grid(True)                                  # activate grid

# =============================================================================
# i=0
# step = (x_max+x_max/5) - (x_min-x_min/5)
# for i in np.arange((x_min-x_min/5),(x_max+x_max/5)+1,step/n):
#     plt.axvline(i)
#     plt.axhline(i)
# =============================================================================
    
    
plt.show()

#print(p)

