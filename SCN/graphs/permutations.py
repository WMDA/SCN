from SCN.folder_structure.folder_utlis import check_path
from SCN.graphs.graph_utlis import load_pickle, save_pickle

import os
import scona as scn
import pandas as pd
from decouple import config


def perm_path():
    
    '''
    Function to get permuation pickle file location

    Parameters
    ----------
    None

    Returns
    -------
    file path: str to permutation pickle file
    '''

    return os.path.join(config('root'), 'work/pickle')


def random_graphs(thresholded_graph: scn.BrainNetwork, perms: int, name: str = 'graph') -> dict:
    '''
    Function to simulate random graphs for checking that actual graphs 
    differs from the random graphs. 

    Parameters
    -----------
    thresholded_graph: scona thresholded graph object.
    perms: int, number of permutations
    name: optional str, Name of graph object



    Returns
    ---------
    results: dict, pandas dataframe of global measures, 
             rich club and small world properties.

    '''

    brain_bundle = scn.GraphBundle(
        [thresholded_graph], [f'{name}_thresholded'])
    brain_bundle.create_random_graphs(f'{name}_thresholded', perms)

    global_measures = brain_bundle.report_global_measures()
    rich_club = brain_bundle.report_rich_club()
    small_world = brain_bundle.report_small_world(f'{name}_thresholded')
    small_world_df = pd.DataFrame.from_dict(
        small_world, orient='index', columns=['small_world_coefficient'])

    return {
        'small_world': small_world_df,
        'global_measures': global_measures,
        'rich_club': rich_club,
    }


def random_graph_permutations(thresholded_graph: scn.BrainNetwork, perms: int, name: str = 'graph') -> dict:
    '''
    Function wrapper around random_graphs function. Will pickle results for later use in work/pickle.
    Will load pickle file if exists. 

    Parameters
    --------------------------------------------------
    thresholded_graph: scona thresholded graph object.
    perms: int, number of permutations
    name: optional str, Name of graph object

    Returns
    --------------------------------------------------
    results: dict, pandas dataframe of global measures, 
             rich club and small world properties.

    '''

    pickle_file = f'/assumptions/random_graphs_for_{name}_at_{perms}_permutations'
    data_path = os.path.join(perm_path(), 'assumptions')
    file_exist = check_path(os.path.join(data_path, f'{pickle_file}.pickle'))

    if file_exist == False:

        results = random_graphs(thresholded_graph, perms, name)
        save_pickle(pickle_file, results)

    if file_exist == True:

        try:
            results = load_pickle(pickle_file)
            print('\nLoaded previous permutation file\n')

        except Exception:

            print('\nError while loading pickle file. Permutating now\n')
            results = random_graphs(thresholded_graph, perms, name)
            save_pickle(pickle_file, results)

    return results
