'''
Functions used to create graphs and generate statistical measures from created graphs.
'''

import numpy as np
import scona as scn
import os
import sys
import pandas as pd
from colorama import Fore

def mean_std(values):
   
    '''
    Function to calculate mean and standard deviation.

    Parameters
    ------------------------------------------------
    values: list, list of values to calculate mean and std

    Returns
    ----------------------------------------------
    results: dict, dictionary of mean and std devations 

    '''
    
    val = np.array(values)
    mean = val.mean()
    std_dev = np.std(val)
    lower_2std = mean - 2*std_dev
    upper_2std =  mean + 2*std_dev
    lower_1std = mean - std_dev
    upper_1std = mean + std_dev 
    
    results = {

        'mean': mean, 
        'upper_1std':upper_1std, 
        'upper_2std':upper_2std, 
        'lower_1std':lower_1std, 
        'lower_2std':lower_2std

    } 
    
    return results


def create_graphs(data, names, centroids, threshold=10):
    
    '''
    Function to create a correlation matrix, graph and thresholded graph.
    Wrapper around multiple scona functions.  

    Parameters
    -----------------------------------------------------
    data: pandas dataframe object with the data for graph.
    names: list object. Names of brain regions.
    centroids. Numpy array. Co-ordinates for names (x,y,z)
    threshold: int, optional. Level to threshold the graph at.

    Returns
    -------------------------------------------------------------------
    results: dict object. Dictionary of corr_matrix (correlation matrix),
             graph (graph unthresholded) and graph_threshold (thresholded graph)      
    '''

    residuals_df = scn.create_residuals_df(data, names)
    corr_matrix = scn.create_corrmat(residuals_df, method='pearson')
    graph = scn.BrainNetwork(network=corr_matrix, parcellation=names, centroids=centroids)
    graph_threshold = graph.threshold(threshold)

    results = {

        'corr_matrix': corr_matrix,
        'graph': graph,
        'graph_threshold': graph_threshold

    }

    return results

def directories(name, data_path):
    
    '''
    Function to check if a directory exists. If directory doesn't exist 
    then creates a new directory.

    Parameters
    ---------------------------------------
    name: str, name of directory
    perms: int, number of permuations used.
    data_path: str, 

    Returns
    -----------------------------------------
    boolean: Retruns True if directory exists. 
             Returns False if directory doesn't 
             exist and makes the directory.

    '''

    dirs = os.listdir(data_path)

    if name not in dirs:        
        path = os.path.join(data_path, name)
        os.mkdir(path)
        return False
    
    else:
        return True

def permutations(thresholded_graph, data_path, name='graph', perms=1000, overwrite=False, save=True):
    
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
    directory_exist = directories(folder_name, data_path)
    path = os.path.join(data_path, folder_name)

    if directory_exist == False or overwrite == True:        
        brain_bundle = scn.GraphBundle([thresholded_graph], [f'{name}_thresholded'])
        brain_bundle.create_random_graphs(f'{name}_thresholded', perms)
        
        global_measures = brain_bundle.report_global_measures()
        rich_club = brain_bundle.report_rich_club()

        small_world = brain_bundle.report_small_world(f'{name}_thresholded')
        small_word_df = pd.DataFrame.from_dict(small_world, orient='index', columns=['small_world_coefficient'])

        if save == True:
        
            try:
                rich_club.to_csv(f'{path}/rich_club.csv')
                global_measures.to_csv(f'{path}/global_measures.csv')
                small_word_df.to_csv(f'{path}/small_world.csv')
        
            except Exception:
                print(Fore.RED + 'Unable to save CSV files.' + Fore.RESET) 

    else:

        try:
            print("Loading CSVs")
            rich_club = pd.read_csv(f'{path}/rich_club.csv')
            global_measures = pd.read_csv(f'{path}/global_measures.csv')
            small_world_df = pd.read_csv(f'{path}/small_world.csv')

        except Exception:
            print(Fore.RED + 'Unable to read in csvs. Please check that data exists in the directory. If data does not exist then use overwrite=True' 
                  + Fore.RESET)
            sys.exit(1)

    results = {

        'global_measures' : global_measures,
        'rich_club' : rich_club,
        'small_world' : small_word_df

    }

    return results


