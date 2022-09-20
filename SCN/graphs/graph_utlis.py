import pickle
import os
from decouple import config
import pandas as pd
import time

def list_of_measures() -> list:
    '''
    Function to get list of graph measures
    TODO add small_world to functionality

    Parameters
    ----------
    None

    Returns
    -------
    list: list of graph theory measures
    '''
    return ['average_clustering', 'average_shortest_path_length', 'assortativity', 'modularity', 'efficiency']


def save_pickle(name: str, object_to_pickle: object) -> None:

    '''
    Function to save an object as pickle file in the work/pickle directory.

    Parameters
    ----------
    name:str of name of file.
    object_to_pickle: object to save as pickle file

    Returns
    -------
    None
    '''

    pickle_path = os.path.join(config('root'), 'work/pickle')

    with open(f'{pickle_path}/{name}.pickle', 'wb') as handle:
        pickle.dump(object_to_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(name_of_pickle_object: str) -> object:

    '''
    Function to load pickle object in the work/pickle directory.

    Parameters
    ----------
    name_of_pickle_object: str name of object to be loaded. 
                           Doesn't need extension

    Returns
    -------
    unpickled obect
    '''

    pickle_path = os.path.join(config('root'), 'work/pickle')

    try: 
        with open(f'{pickle_path}/{name_of_pickle_object}.pickle', 'rb') as handle:
            return pickle.load(handle)
    
    except FileNotFoundError as e:
        print(f'Unable to load pickle file {pickle_path}/{name_of_pickle_object} Please check the pickle object exists')

def df_for_sns_barplot(measures, original_network) -> pd.DataFrame:
    
    '''
    This is a horrible function needs refactoring
    modified scona create_df_sns_barplot function.
    See original function for full documentation.
    
    Main difference is this function does not calculate global and small world measures 
    as this has been done by previous functions. 

    Also refactored code to remove unecessary variables.
    '''
    
    bundleGraphs_measures = measures['global_measures']
    small_world = measures['small_world']

    abbreviation = {'assortativity': 'a',
                    'average_clustering': 'C',
                    'average_shortest_path_length': 'L',
                    'efficiency': 'E',
                    'modularity': 'M'}

    new_columns = ["measure", "value", "TypeNetwork"]
    no_columns_old = len(bundleGraphs_measures.columns)
    no_rows_old = len(bundleGraphs_measures.index)
    total_rows = no_columns_old * no_rows_old
    index = [index for index in range(1, total_rows + 1)]
    data_array = list()

    for measure in bundleGraphs_measures.columns:
 
        try:
            value = bundleGraphs_measures.loc[original_network, measure]
        except Exception as e:
            print(e)

        measure_short = abbreviation[measure]
        tmp = [measure_short, value, "Observed network"]
        data_array.append(tmp)

    random_df = bundleGraphs_measures.drop(original_network)

    for measure in random_df.columns:

        for rand_graph in random_df.index:
            value = random_df[measure][rand_graph]
            measure_short = abbreviation[measure]
            tmp = [measure_short, value, "Random network"]
            data_array.append(tmp)


    new_df = pd.DataFrame(data=data_array, index=index,
                                columns=new_columns)

    if len(small_world) > 1:

        df_small_world = []
        for value in small_world.values:
            tmp = {'measure': 'sigma',
                   'value': float(value),
                   'TypeNetwork': 'Observed network'}

            df_small_world.append(tmp)

        new_df = new_df.append(df_small_world, ignore_index=True)

        rand_small_world = {'measure': 'sigma',
                            'value': 1,
                            'TypeNetwork': 'Random network'}

        new_df = new_df.append(rand_small_world,
                                           ignore_index=True)

    return new_df

class TimeError(Exception):
    """Custom Timer Exception"""

class MeasureError(Exception):
    """Custom measure exception"""

class Timer:

    '''
    Custom Class to time how long scripts take to run.

    Usage:
    
    from functions.utils import Timer

    timer = Timer()
    timer.start()
    <code here>
    timer.stop()
    '''

    def __init__(self) -> None:
        self.__start = None

    def start(self) -> None:
        
        if self.__start is not None:
            raise TimeError("Timer is already started")

        self.__start = time.perf_counter()

    def stop(self) -> None:
        
        if self.__start is None:
            raise TimeError("Timer has not been started. Use .start() to start timer")
        
        time_taken = time.perf_counter() - self.__start
        self.__start = None
        
        if time_taken > 60:
            time_taken = time_taken / 60
            print(f"Finished in {time_taken} mins")

        else:
            print(f"Finished in {time_taken} seconds")