'''
Functions used to create graphs and statistical measures from created graphs.
'''

import numpy as np
import scona as scn

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
    --------------------------------------------
    data: pandas dataframe object with the data for graph.
    names: list object. Names of brain regions.
    centroids. Numpy array. Co-ordinates for names (x,y,z)
    threshold: int, optional. Level to threshold the graph at.

    Returns
    ------------------------------------------------
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