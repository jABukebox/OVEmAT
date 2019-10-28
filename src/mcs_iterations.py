
import pandas as pd
import os



# setting the directory
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#os.chdir('../inputfiles/')

# defining the iterations of D
D_iterations = [2500, 5000, 10000, 20000, 40000]


counter = 1
# Loop for annual distances D
for D in D_iterations:

    print('Start of iteration, D =', D)
    # Loop for sth else, perhaps LCE top down values

    # altering the default_general input file
    default_general = pd.read_csv('/Users/Alex/Projects/PycharmProjects/OVEmAT/src/inputfiles/_default_general.csv', sep=';')  # reading the data into a pd dataframe
    default_general = default_general.set_index('vars') # set vars as indeces
    default_general.loc['D'] = D    # assigning the D of iteration to both min and max
    default_general.to_csv('/Users/Alex/Projects/PycharmProjects/OVEmAT/src/inputfiles/_default_general.csv', index='vars', sep=';') #saving back

    #executing the simulation
    os.system('python3 /Users/Alex/Projects/PycharmProjects/OVEmAT/src/main.py')



    #loading new results_all
    new_iteration_df = pd.read_csv('/Users/Alex/Projects/PycharmProjects/OVEmAT/src/results/result_all.csv',
                sep=';')  # reading the data into a pd dataframe

    if counter == 1: #first time
        #take dataframe without concatenating
        all_iterations_df = new_iteration_df
    else:
        #concatenating old iterations and new iteration
        all_iterations_df = all_iterations_df.append(new_iteration_df)


    #saving everything to a new file
    all_iterations_df.to_csv('/Users/Alex/Projects/PycharmProjects/OVEmAT/src/results/iterations_all.csv', sep=';')

    print('end of iteration, D =', D)
    counter += 1


