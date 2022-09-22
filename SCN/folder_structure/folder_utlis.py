import os
from decouple import config

def check_path(data_path:str) -> bool:
    
    '''
    Function to check if a directory exists.

    Parameters
    ---------------------------------------
    data_path: str, path to directory

    Returns
    -----------------------------------------
    boolean: Retruns True if directory exists. 
             Returns False if directory doesn't 
             exist 

    '''

    try:
        assert os.path.exists(data_path)
        return True

    except AssertionError:
        return False 

def check_pickle_file(pickle_file:str) -> bool:
    
    '''
    Function to check if a pickle file exists.

    Parameters
    ---------------------------------------
    pickle_file: str, name of pickle file (this function only checks the root pickle directory.
                 file name needs to include group_differences/ or assumptions/    )

    Returns
    -----------------------------------------
    boolean: Retruns True if directory exists. 
             Returns False if directory doesn't 
             exist 

    '''
    
    pickle_path = os.path.join(config('root'), f'work/pickle/{pickle_file}')
    
    try:
        assert os.path.exists(pickle_path)
        return True

    except AssertionError:
        return False 