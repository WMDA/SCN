import os
import sys
import argparse


def set_arguments() -> dict:
    option = argparse.ArgumentParser()
    option.add_argument("-p", "--path", dest='path', help="filepath to set up directories in")
    option.add_argument('-n', '--name', dest='name', help='Name of directory. Default is SCN')
    args = vars(option.parse_args())
    return args


def folder_creation(file_path : str, name:str = 'SCN') -> None:
        
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


if __name__ == '__main__':
    
    # Make the following into an importable function
    args = set_arguments()

    try:
        if args['name'] == None:
            assert os.path.exists(args['path']+ '/SCN')
        if args['name'] != None:
            assert os.path.exists(args['path']+ '/' + args['name'])
        
        print('Directory exists, skipping...')
    
    except AssertionError:
        print(args['path'], ' does not exist. Setting up directories now')
        
        if args['name'] != None:
            folder_creation(args['path'], args['name'])

        if args['name'] == None:
            folder_creation(args['path'])