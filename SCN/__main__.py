from SCN.workflow.assumptions_workflow import main_assumptions_work_flow
from SCN.workflow.group_difference_workflow import main_group_differences_workflow
from SCN.folder_structure.folder_setup import setup
from SCN.graphs.graph_utlis import Timer
from SCN.setup.setup_scn import logo, arguments, set_up_logs

import os
import sys
import pandas as pd
from datetime import datetime

if __name__ == '__main__':

    print(logo())
    print('Starting SCN.')
    print('\nChecking and setting up SCN folder structure.')
    
    args = arguments()

    # The following code sets the arguments with 
    if args['skip'] == False:
        if args['path'] == None:
            print('\nNo file path given. use --path to set file path for project to be set up in. Exiting.')
            sys.exit(1)

        try:
            assert os.path.exists(args['path'])
            setup(args['path'], args['name'])
            
        except AssertionError as e:
            print('\nGiven filepath given does not exist. Please provide a real file path\nExiting.')
            sys.exit(1)

    if args['skip'] == True:
        print('\nSkip argument set. Skipping directory set up.')
    
    
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

    date_time = datetime.now()
    if args['no-logs'] != True: 
        set_up_logs('assumptions', date_time, args['measure'])
        print(logo())
    
    if args['no-logs'] == True:
        print('\nNo logs option set. No log files created')
   
    # The following code runs the assumptions workflow
    
    if args['group-only'] != True:    
    
        print(date_time)
        print(f"\nWorking on assumptions workflow for {args['measure']} with {args['perms']} permutations\n")
        try:
            time_class = Timer()
            time_class.start()
            main_assumptions_work_flow(group_0, group_1, group_2, args['perms'], args['measure'])
            print('\nAssumptions work flow sucessfully completed with out any errors')
            time_class.stop()
            sys.stdout = sys.__stdout__
            print('SCN Assumptions has completed.')
    
        except KeyboardInterrupt:
            sys.stdout = sys.__stdout__
            print('\nUser initiated shutdown. Bye!!')
            sys.exit(0)
    sys.stdout = sys.__stdout__
    
    if args['group-only'] == True:
        print('\nGroup only option set. Skipping assumptions workflow')
    
    if args['no-logs'] != True: 
        set_up_logs('group_differences', date_time, args['measure'])
        
    try:
        print(date_time)
        print(f"\nWorking on group differences workflow for {args['measure']} with {args['perms']} permutations\n")
        time_class = Timer()
        time_class.start()
        main_group_differences_workflow(group_0, group_1, group_2, args['perms'], args['measure'], args['threshold'], date_time)
        print('\nGroup differences work flow sucessfully completed with out any errors')
        time_class.stop()
        sys.stdout = sys.__stdout__
        print('SCN Group differences has completed.')

    except KeyboardInterrupt:
            sys.stdout = sys.__stdout__
            print('\nUser initiated shutdown. Bye!!')
            sys.exit(0)