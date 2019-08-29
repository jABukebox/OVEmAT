# OVEmAT - Open Vehicle Emission Analysis Tool

# About 

This tool is the base of the Master Thesis "Multidimensional uncertainty quantification of alternative drive technologies regarding Life Cycle Emissions and Total Cost of Ownership " written by Jaron Bucka in 2019.

It calculates the emissions (LCE) and total costs (TCO) for four vehicle drives powered by renewable energy: 
Battery Electric Vehicles (BEV), Fuel Cell Electric Vehicles (FCEV), Plug-In Hybrid Vehicles (PHEV) and Internal Combustion Engine Vehicle (ICEV).

Additionally there are three vehicle classes, of which one must be selected at the beginning of usage: Compact Car, SUV, Light Duty Vehicle.

This tool is created to operationalize important parameters of vehicles. Therefore all vehicles are calculated n times (internally set to n=500), to create a scatter plot of each drive.
All important ingoing parameters are given in ranges, while these ranges act as uncertainty of the specific parameter. 
With adjusting the parameters in the file save_defaults.py, a lot of conditions can be simulated.

The formulas used for the calculations are based on carboncounter.com and their support papers (https://pubs.acs.org/doi/full/10.1021/acs.est.6b00177) but adjusted to the personal needs with adding a Monte Carlo simulation for the parameter selection.


FOR FURTHER INFORMATION CONTACT ME AT: jaron.bucka@gmx.de




# Call Functions - PROCEDURE OF PROGRAM
class_sel = veh_class_sel()         # 1. VEHICLE CLASS SELECT

dimension = lhs_dimension()         # 2. CALCULATE DIMENSION

p = latin_hype(dimension, n)        # 3. GENERATE LHS SAMPLEPOINTS WITH "dimension" DIMENSION AND n REPEATS

var = final_variables(p, dimension, class_sel)      # 4. CALCULATE FINAL VARIABLES

res, res_extend, all_values = result_calc(var, class_sel, dimension)    # 5. CALCULATE ALL RESULTS

SaveResults(res, res_extend, all_values)            # 5. SAVE ALL RESULTS TO .CSV

PlotClass                                           # 6. PLOT EVERYTHING





# ------- ADD VALUES TO LHS-RANGE ------- # 
1. Add value name to ether default_general or default_compact etc in save_defaults.py
2. Add corresponding value min and value max
3. Add value name to list in function lhs_dimension
4. Add value name to every corresponding list in function get_variables
...



-----------------
MIT Licence

Copyright (c) 2019 Jaron Bucka

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.