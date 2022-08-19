import os
import sys
import argparse


def set_arguments() -> dict:
    option = argparse.ArgumentParser()
    option.add_argument("-p", "--path", dest='path', help="filepath to set ")
    
    args = vars(option.parse_args())
    return args


def folder_creation(file_path : str) -> None:
        
        try:
            os.mkdir(file_path)
        except PermissionError:
            print('Do not have the write permissions to create a folder in this directory. Either change file path or the directories permssions')
            sys.exit(1)


if __name__ == '__main__':
    
    # Make the following into an importable function
    args = set_arguments()

    try:
        assert os.path.exists(args['path'])
        print('Directory exists, skipping...')
    
    except AssertionError:
        print(args['path'], ' does not exist. Creating folder now')
        folder_creation(args['path'])