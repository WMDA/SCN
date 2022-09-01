from SCN.folder_structure.folder_utlis import check_path
from SCN.graphs.graph_utlis import load_pickle, save_pickle

import numpy as np
import scona as scn
import pandas as pd


def random_graphs(thresholded_graph:scn.BrainNetwork, perms:int, name:str='graph') -> dict:
        
        brain_bundle = scn.GraphBundle([thresholded_graph], [f'{name}_thresholded'])
        brain_bundle.create_random_graphs(f'{name}_thresholded', perms)
        
        global_measures = brain_bundle.report_global_measures()
        rich_club = brain_bundle.report_rich_club()

        small_world = brain_bundle.report_small_world(f'{name}_thresholded')
        small_world_df = pd.DataFrame.from_dict(small_world, orient='index', columns=['small_world_coefficient'])
        
        return {
            'small_world' : small_world_df,
            'global_measures' : global_measures,
            'rich_club' : rich_club,
        }

def random_graph_permutations(thresholded_graph:scn.BrainNetwork, data_path:str, perms:int, name:str='graph') -> dict:
    
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
    directory_exist = check_path(data_path)

    if directory_exist == False:        

        results = random_graphs(thresholded_graph, perms, name)
        save_pickle(folder_name, results)

    if directory_exist == True:

        try:
            results = load_pickle(folder_name)

            if results == None:
                raise FileExistsError
        
        except FileExistsError:
            
            print('\nPermutating through graphs')
            results = random_graphs(thresholded_graph, perms, name)
            save_pickle(folder_name, results)
    
    return results