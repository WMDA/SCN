from SCN.folder_structure.folder_utlis import check_directories

import numpy as np
import scona as scn
import os
import sys
import pandas as pd
from colorama import Fore


def random_graph_permutations(thresholded_graph:scn.BrainNetwork, data_path:str, perms:int, name:str='graph',  overwrite:bool=False, save:bool=True) -> dict:
    
    '''
    Function to simulate random graphs for checking that actual graphs 
    differs from the random graphs. Will also create a directory with 
    csvs if one doesn't exist.
    

    Parameters
    --------------------------------------------------
    thresholded_graph: scona thresholded graph object.
    data_path: str, path to directory where to save results.
    name: optional str, Name of graph object
    perms: int, number of permutations
    overwrite: optional Boolean, 

    Returns
    --------------------------------------------------
    results: dict, pandas dataframe of global measures, 
             rich club and small world properties.

    '''

    folder_name = f'{name}_{perms}'
    directory_exist = check_directories(folder_name, data_path)
    path = os.path.join(data_path, folder_name)

    if directory_exist == False or overwrite == True:        
        brain_bundle = scn.GraphBundle([thresholded_graph], [f'{name}_thresholded'])
        brain_bundle.create_random_graphs(f'{name}_thresholded', perms)
        
        global_measures = brain_bundle.report_global_measures()
        rich_club = brain_bundle.report_rich_club()

        small_world = brain_bundle.report_small_world(f'{name}_thresholded')
        small_world_df = pd.DataFrame.from_dict(small_world, orient='index', columns=['small_world_coefficient'])

        if save == True:
        
            try:
                rich_club.to_csv(f'{path}/rich_club.csv')
                global_measures.to_csv(f'{path}/global_measures.csv')
                small_world_df.to_csv(f'{path}/small_world.csv')
        
            except Exception:
                print(Fore.RED + 'Unable to save CSV files.' + Fore.RESET) 

    else:

        try:
            print("Loading CSVs")
            rich_club = pd.read_csv(f'{path}/rich_club.csv').set_index('Unnamed: 0')
            global_measures = pd.read_csv(f'{path}/global_measures.csv').set_index('Unnamed: 0')
            small_world_df = pd.read_csv(f'{path}/small_world.csv').set_index('Unnamed: 0')


        except Exception:
            print(Fore.RED + 'Unable to read in csvs. Please check that data exists in the directory. If data does not exist then use overwrite=True' 
                  + Fore.RESET)
            sys.exit(1)

    results = {
        'small_world' : small_world_df,
        'global_measures' : global_measures,
        'rich_club' : rich_club,
        

    }

    return results