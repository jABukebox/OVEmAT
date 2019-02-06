
import pandas as pd

### übergabe der input variablen in dataframe

a,b,c,d,e,f,g,h = 0,0,0,0,0,0,0,0

### rausfinden wieviele variablen maximal und minimal und listen erstellen

var_names = [a,b,c,d,e,f,g,h]

propType = ['FCEV', 'BEV', 'ICEV', 'PHEV']

#raw_data= {'name':['']}

def getVariables(val_min, val_max):
    ### Create Dict
    var_get = {'Bounderies': ['min', 'max']}
    var_get_df = pd.DataFrame(data=var_get)
    var_get_df = var_get_df.set_index("Bounderies")

    #i = 1
    for i in range(len(var_names)):

        key = 'var'+str(i+1)
        #min_e = input('minimum eingeben:')
        #max_e = input('maximum eingeben:')
        #var_get_df[key] = [min_e, max_e]

        var_get_df[key] = [val_min, val_max] # append column to df


    print('\n')
    print(var_get_df)
    #print(var_get_df.get_value('min','var3'))
    print(var_get_df.iat['min', 'var3'])

getVariables(6,5)

#var_get_df = pd.DataFrame(data=var_get)


    # var_get = {'Bounderies': ['min', 'max'],  # 'Dictionary' -> Values have to be set from user or default
    #            'var1': [val_min, val_max],
    #            'var2': [val_min, val_max],
    #            'var3': [val_min, val_max],
    #            'var4': [val_min, val_max],
    #            'var5': [val_min, val_max],
    #            }


### Update values after input change
# if state changed: getVariables()