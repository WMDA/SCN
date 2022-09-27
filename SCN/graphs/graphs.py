import scona as scn
import pandas as pd
import numpy as np
import os
import sys


def load_atlas_csv() -> pd.DataFrame:
    '''
    Functon to return freesurfer atlas with mni co-ordinates and names

    Parameters
    ----------
    None

    Returns
    -------
    atlas.csv pd.Dataframe
    '''
    
    try:
       path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'SCN/graphs/data')
       return pd.read_csv(f'{path}/atlas.csv')
    except Exception:
        
        try:
            path = os.path.join(os.getcwd(), 'SCN/graphs/data')
            return pd.read_csv(f'{path}/atlas.csv')  
        except Exception as e:
            print('Unable to load atlas.csv due to:', e)
            print('This commonly happens with venvs or grid systems. If using a grid system please make sure grid script is in the SCN root directory')
            sys.exit(1)


def load_centroids() -> np.float64:
    '''
    Function to return centroids from freesurfer atlas. 

    Parameters
    ----------
    None

    Returns
    -------
    array of np.float64 values representing x, y, z co-ordinates in MNI space
    '''

    atlas_df = load_atlas_csv()
    return atlas_df[['x.mni', 'y.mni', 'z.mni']].to_numpy()


def load_names() -> list:
    '''
    Function to return names from freesurfer atlas. 

    Parameters
    ----------
    None

    Returns
    -------
    list str values of name of brain regions
    '''

    atlas_df = load_atlas_csv()
    return list(atlas_df['name'])


def create_graphs(data: pd.DataFrame, names: list, centroids: np.float64, threshold: int) -> dict:
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
    graph = scn.BrainNetwork(
        network=corr_matrix, parcellation=names, centroids=centroids)
    graph_threshold = graph.threshold(threshold)

    results = {

        'corr_matrix': corr_matrix,
        'graph': graph,
        'graph_threshold': graph_threshold

    }

    return results
