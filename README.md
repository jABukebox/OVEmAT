# OVEmAT - Open Vehicle Emission Analysis Tool

# Call Functions - PROCEDURE OF PROGRAM
class_sel = veh_class_sel()         # 1. CLASS SELECT

dimension = lhs_dimension()         # 2. CALCULATE DIMENSION

p = latin_hype(dimension, n)        # 3. GENERATE LHS SAMPLEPOINTS WITH "dimension" DIMENSION AND n REPEATS

var = final_variables(p, dimension, class_sel)      # 4. CALCULATE FINAL VARIABLES

res, res_extend, all_values = result_calc(var, class_sel, dimension)    # 5. CALCULATE ALL RESULTS

SaveResults(res, res_extend, all_values)            # 5. SAVE ALL RESULTS TO .CSV

PlotClass                                           # 6. PLOT EVERYTHING



# For saving result figure, change line 70 in pyqtgraphs "ImageExporter.py" to:
## bg = np.empty((int(self.params['width']), int(self.params['height']), 4), dtype=np.ubyte)


# ------- ADD VALUES TO LHS-RANGE ------- # 
1. Add value name to ether default_general or default_compact etc in save_defaults.py
2. Add corresponding value min and value max
3. Add value name to list in function lhs_dimension
4. Add value name to every corresponding list in function get_variables
5. 
