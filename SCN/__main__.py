from SCN.workflow.assumptions_workflow import main_assumptions_work_flow
from SCN.folder_structure.folder_setup import setup
from SCN.graphs.graph_utlis import Timer

import argparse
import os
import sys
import pandas as pd
from datetime import datetime
from decouple import config

def arguments():
    option = argparse.ArgumentParser()
    option.add_argument('-g0', '--group_0', dest='group_0',
                        help='csv file of participants structural measures. SCN at the moment does not track group names only numbers. SCN also can only handle upto three groups.')
    option.add_argument('-g1', '--group_1', dest='group_1',
                        help='csv file of participants structural measures. SCN at the moment does not track group names only numbers. SCN also can only handle upto three groups.')
    option.add_argument('-g2', '--group_2', dest='group_2',
                        help='csv file of participants structural measures. SCN at the moment does not track group names only numbers. SCN also can only handle upto three groups.')
    option.add_argument('-p', '--perms', dest='perms', type=int,
                        help="number of permuations to do")
    option.add_argument("--path", dest='path',
                        help="filepath to set up project in")
    option.add_argument('-n', '--name', dest='name',
                        help="name of project. Default is SCN")
    option.add_argument('-s', '--skip', dest='skip', help="skip folder set up", action='store_true')
    option.add_argument('-w', '--wdir', dest='wdir',
                        help='working directory where data is stored')
    option.add_argument('-m', '--measure', dest='measure',
                        help='measure that is being examined')

    arg = vars(option.parse_args())

    return arg


if __name__ == '__main__':
    
    print( 
    """

     _---~~(~~-_.
    _{        )   )
  ,   ) -~~- ( ,-' )_
 (  `-,_..`., )-- '_,)
( ` _)  (  -~( -_ `,  }
(_-  _  ~_-~~~~`,  ,' )
  `~ -^(    __;-,((()))
        ~~~~ {_ -_(())
               `\  }
                 { })

    SCN - Structural Covariance Network pipeline
    Based on the paper by Drakesmith et al and scona (https://github.com/WhitakerLab/scona)
    Art by Steven James Walker
    For queries/problems/contribute at https://github.com/WMDA/SCN
    

    
    """
    )

    print('Starting SCN.')
    print('\nChecking and setting up SCN folder structure')
    
    args = arguments()
    
    # The following code sets the arguments with 
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
    
    
    # THe following code uses pandas to load csvs
    print('\nLoading data')

    if args['wdir'] != None:
        group_0_data = os.path.join(args['wdir'], args['group_0'])
        group_1_data = os.path.join(args['wdir'], args['group_1'])
        
        if args['group_2'] != None:
            group_2_data = os.path.join(args['wdir'], args['group_2'])

    else:
        group_0_data = args['group_0']
        group_1_data = args['group_1']

        if args['group_2'] != None:
            group_2_data = args['group_2']

    try: 
        group_0 = pd.read_csv(group_0_data)
        group_1 = pd.read_csv(group_1_data)
    
        if args['group_2'] != None:
            group_2 = pd.read_csv(group_2_data)
        
        else:
            group_2 = None

    except Exception as e:
        print('\nUnable to load in data due to the following reason:\n', e, '\nExiting')
        sys.exit(1)
    
    log_path = os.path.join(config('root'), 'logs')
    date_time = datetime.now()
    log_name = date_time.strftime(f'{args["measure"]}_assumptions_logFile_%S%M_%Y.txt')
    print(f'\nSetting up log files. Log files being saved to {log_path}')
    sys.stdout = open(f'{log_path}/{log_name}','w')

    # The following code runs the assumptions workflow
    time_class = Timer()
    time_class.start()
    print(date_time)
    print(f"\nWorking on Assumptions workflow for {args['measure']} with {args['perms']} permutations\n")
    

    try:
        main_assumptions_work_flow(group_0, group_1, group_2, args['perms'], args['measure'])
        print('\nAssumptions work flow sucessfully completed with out any errors')
        time_class.stop()
        sys.stdout = sys.__stdout__
        print('SCN Assumptions has completed.')

    except KeyboardInterrupt:
        sys.stdout = sys.__stdout__
        print('\nUser initiated shutdown. Bye!!')
        sys.exit(0)