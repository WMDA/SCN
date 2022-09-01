import os



def check_directories(name:str, data_path:str) -> bool:
    
    '''
    Function to check if a directory exists. If directory doesn't exist 
    then creates a new directory.

    Parameters
    ---------------------------------------
    name: str, name of directory
    data_path: str, path to directory

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
