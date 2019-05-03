# OVEmAT - Open Vehicle Emission Analysis Tool
This open source program is part of the Master Thesis "Uncertainty Quantification of Alternative Drive Technologies 
regarding Life Cycle Emissions and Total Cost of Ownership".
Written and programmed by Jaron Bucka in 2019.

The aim is to quantify and parametrize uncertainties of, which occure ... and evaluate differences i.e. advantages and disadvantages of 
the compared drive technologies in terms of Life Cycle Emissions and Total Cost of Ownership. 

With changing the settings in save_defaults.py you can customize the values to fit a specific scenario.


For more information see the documentation in the Master Thesis.


# Call Functions - PROCEDURE OF PROGRAM
class_sel = veh_class_sel()                                             # 1. CLASS SELECT

dimension = lhs_dimension()                                             # 2. CALCULATE DIMENSION

p = latin_hype(dimension, n)                                            # 3. GENERATE LHS SAMPLEPOINTS WITH "dimension" DIMENSION AND n REPEATS

var = final_variables(p, dimension, class_sel)                          # 4. CALCULATE FINAL VARIABLES

res, res_extend, all_values = result_calc(var, class_sel, dimension)    # 5. CALCULATE ALL RESULTS

SaveResults(res, res_extend, all_values)                                # 5. SAVE ALL RESULTS TO .CSV

PlotClass                                                               # 6. PLOT EVERYTHING



# For saving result figure, change line 70 in pyqtgraphs "ImageExporter.py" to:
## bg = np.empty((int(self.params['width']), int(self.params['height']), 4), dtype=np.ubyte)


Licence: MIT