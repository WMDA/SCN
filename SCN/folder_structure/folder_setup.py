import os
import sys
import argparse
import re


def set_arguments() -> dict:

    option = argparse.ArgumentParser()
    option.add_argument("-p", "--path", dest='path',
                        help="filepath to set up directories in")
    option.add_argument('-n', '--name', dest='name',
                        help='Name of directory. Default is SCN')
    args = vars(option.parse_args())
    return args


def folder_creation(file_path: str, name: str = 'SCN') -> None:

    try:
        os.mkdir(f'{file_path}/{name}')
        os.mkdir(f'{file_path}/{name}/logs')
        os.mkdir(f'{file_path}/{name}/results')
        os.mkdir(f'{file_path}/{name}/work')
        os.mkdir(f'{file_path}/{name}/work/pickle')
        os.mkdir(f'{file_path}/{name}/work/data')

    except PermissionError:
        print("Do not have the write permissions to create a folder in this directory. Either change file path or the directory's permssions")
        sys.exit(1)

def update_env(file_path: str, name: str):
    
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
                    lines[index] = value.replace(value, f'root={file_path}/{name}')

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

    if name == None:
        name = 'SCN'

    try:
        assert os.path.exists(file_path + '/' + name)
        print('Directory setup exists, skipping...')

    except AssertionError:
        print(file_path, ' does not exist. Setting up directories now')
        folder_creation(file_path, name)

    update_env(file_path, name)

if __name__ == '__main__':

    args = set_arguments()
    setup(args['path'], args['name'])