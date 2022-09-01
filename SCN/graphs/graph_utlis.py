import pickle
import os
from decouple import config


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
    
    except FileNotFoundError:
        print(f'Unable to load pickle file {pickle_path}/{name_of_pickle_object} Please check the pickle object exists')