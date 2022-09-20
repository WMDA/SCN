import argparse
import os
import sys
import pandas as pd
#from SCN.workflow.assumptions_workflow import main_assumptions_work_flow
from SCN.folder_structure.folder_setup import setup


def arguments():
    option = argparse.ArgumentParser()
    option.add_argument('-g0', '--group_0', dest='group_0',
                        help='csv file of participants structural measures. SCN at the moment does not track group names only numbers. SCN also can only handle upto three groups.')
    option.add_argument('-g1', '--group_1', dest='group_1',
                        help='csv file of participants structural measures. SCN at the moment does not track group names only numbers. SCN also can only handle upto three groups.')
    option.add_argument('-g2', '--group_2', dest='group_2',
                        help='csv file of participants structural measures. SCN at the moment does not track group names only numbers. SCN also can only handle upto three groups.')
    option.add_argument('-p', '--perms', dest='perms',
                        help="number of permuations to do")
    option.add_argument("--path", dest='path',
                        help="filepath to set up project in")
    option.add_argument('-n', '--name', dest='name',
                        help="name of project. Default is SCN")
    option.add_argument('-s', '--skip', dest='skip', help="skip folder set up", action='store_true')

    arg = vars(option.parse_args())

    return arg


if __name__ == '__main__':
    args = arguments()

    if args['skip'] == False:
        if args['path'] == None:
            print('\nNo file path given. use --path to set file path for project to be set up in. Exiting')
            sys.exit(1)

        try:
            assert os.path.exists(args['path'])
            setup(args['path'], args['name'])
            
        except AssertionError as e:
            print('\nGiven filepath given does not exist. Please provide a real file path\nExiting')
            sys.exit(1)

    if args['skip'] == True:
        print('\nSkipping directory set up')

    print('\nLoading data')
    
    try: 
        group_0 = pd.read_csv(args['group_0'])
        group_1 = pd.read_csv(args['group_0'])
    
        if args['group_2'] != None:
            group_2 = pd.read_csv(args['group_2'])
    except Exception as e:
        print('\nUnable to load in data due to the following reason:\n', e, '\nExiting')
        sys.exit(1)
