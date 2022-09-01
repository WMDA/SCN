import os



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
