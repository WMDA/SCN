import os
import sys

def folder_creation(file_path: str, name: str = 'SCN') -> None:

    '''
    Function to make folders. 

    Parameters
    ----------
    file_path:str of absolute path file to where scn should set up
    name:str optional name of directory. If left blank then name is SCN
    '''

    try:
        os.mkdir(f'{file_path}/{name}')
        os.mkdir(f'{file_path}/{name}/logs')
        os.mkdir(f'{file_path}/{name}/results')
        os.mkdir(f'{file_path}/{name}/results/assumptions')
        os.mkdir(f'{file_path}/{name}/results/group_differences')
        os.mkdir(f'{file_path}/{name}/work')
        os.mkdir(f'{file_path}/{name}/work/pickle')
        os.mkdir(f'{file_path}/{name}/work/pickle/assumptions')
        os.mkdir(f'{file_path}/{name}/work/pickle/group_differences')
        os.mkdir(f'{file_path}/{name}/work/visual_graphs')

    except PermissionError:
        print("Do not have the write permissions to create a folder in this directory. Either change file path or the directory's permssions")
        sys.exit(1)

def update_env(file_path: str, name: str) -> None:

    '''
    Function to create/update .env file which is used by scn to keep track of directories.

    Parameters
    ----------
    file_path:str of absolute path file to where scn should set up
    name:str optional name of directory. If left blank then name is SCN

    Returns
    -------
    None
    '''
    
    env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'.env')
    if name == None:
        name = 'SCN'
    
    try:
        assert os.path.exists(env_file_path)
        print('\nmodifying .env file')

        try:
            with open(env_file_path, 'r') as file:
                lines = file.readlines()
            file.close()
            
            for index, value in enumerate(lines):
                if 'root' in value:
                    lines[index] = value.replace(value, f'root={file_path}/{name}\n')

            with open(env_file_path, 'w') as file:
                file.writelines(lines)
            file.close()

        except Exception as e:
            print(e)
    
    except:
        print('\nno .env file found. Creating one')
        env = open(env_file_path, 'w')
        env.write(f'root={file_path}/{name}')
        env.close()

def setup(file_path: str, name: str) -> None:

    '''
    Wrapper around directory set up script. Also function to assertain if directory already exists.
    
    Parameters
    ----------
    file_path:str of absolute path file to where scn should set up
    name:str optional name of directory. If left blank then name is SCN

    Returns
    -------
    None
    '''

    if name == None:
        name = 'SCN'

    try:
        assert os.path.exists(file_path + '/' + name)
        print('Directory setup exists, skipping...')

    except AssertionError:
        print('\n',file_path + '/' + name, ' does not exist. Setting up directories now')
        folder_creation(file_path, name)

    update_env(file_path, name)