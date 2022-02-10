'''
Script used to create random graphs. Recommended to run this script first to permutate random graphs as it uses multipleprocessing to speed up time.
'''

import functions.statistical_functions as Sfun
from functions.utils import load_data
import argparse
import multiprocessing
import os
from decouple import config

def options():
    
    '''
    Function to set command line options. 
    
    Usage:
    python3 random_graph_creation.py -h for help

    '''

    args = argparse.ArgumentParser()
    args.add_argument('-d', '--data', dest='data', help='File path to data. If left blank will search for .env file')
    args.add_argument('-r', '--results', dest='results', help='File path to results. If left blank will search for .env file')
    args.add_argument('-l', '--logs', dest='logs', help='File path to log files. If left blank will search for .env file')
    args.add_argument('-m', '--measure', dest='measure', help='Specify measure, pick from either LGI, area or volume')
    args.add_argument('-o', '--overwrite', dest='overwrite', help='Set overwrite to be true', action='store_true')
    args.add_argument('-p', '--perms', dest='perms', help='Specify number of permutations')

    flags = vars(args.parse_args())

    if not flags['measure']:
        args.error('No measure provided. Please specify -m with a measure. use -h or --help')
    elif not flags['perms']:
        args.error('Number of permutations not provided. Please specify -p with a number. use -h or --help')

    return flags

def arguments():

    '''
    Function to clean up arguments.
    Checks if flags were given and if not searches the .env file
    for any enviornmental variables.
    
    Parameters
    -----------
    None

    Returns
    ---------
     results: dict object with values for;
              data, results, logs, perms, measure, 
              overwrite
    '''
    
    args = options()

    if args['data'] != None:
        data = args['data']
    else:
        data = config('data')
    
    if args['results'] != None:
        results = args['results']
    else:
        results = config('results')
    
    if args['logs'] != None:
        logs = args['logs']
    else:
        logs = config('logs')
    
    try:
        perms= int(args['perms'])
    
    except Exception:
        print('Number of permutations not correctly set')
        sys.exit(1)
    
    results ={
        'data':data,
        'results':results,
        'logs':logs,
        'perms':perms,
        'measure':args['measure'],
        'overwrite':args['overwrite']
    }

    return results

if __name__=='__main__':
    
    from functions.utils import Timer
    import sys
    from datetime import datetime

    args = arguments()

    logs = args['logs']

    date_time = datetime.now()
    log_name = date_time.strftime('logFile_%S%M_%Y.txt')
    
    #This creates a log file and all std output is directed to the log file
    os.system(f'touch {logs}/{log_name}')

    sys.stdout = open(f'{logs}/{log_name}','w')
    
    time = Timer()
    time.start()
    
    print(date_time)
    print(args['measure'])
    
    try:
        
        loaded_data = load_data('LGI', args['data'])

        aan_graphs = Sfun.create_graphs(loaded_data['aan'].iloc[:,1:69], loaded_data['names'], loaded_data['centroids'])
        wr_graphs = Sfun.create_graphs(loaded_data['wr'].iloc[:,1:69],  loaded_data['names'], loaded_data['centroids'])
        hc_graphs = Sfun.create_graphs(loaded_data['hc'].iloc[:,1:69],  loaded_data['names'], loaded_data['centroids'])

        def multiprocessing_permutations(group):
            
            '''
            Multiprocessing function. Placed here in script so cannot be imported.
            Also due to limiations in multiprocessing needs to be here to get all the correct variables. 
            '''
        
            measure = args['measure']

            if group == 'aan':
                aan_bundle = Sfun.permutations(aan_graphs['graph_threshold'], args['results'], name=f'AAN_graph_{measure}', overwrite=args['overwrite'], perms=args['perms'])
            elif group == 'wr':
                wr_bundle = Sfun.permutations(wr_graphs['graph_threshold'], args['results'], name=f'WR_graph_{measure}', overwrite=args['overwrite'], perms=args['perms'])
            elif group == 'hc':
                hc_bundle = Sfun.permutations(hc_graphs['graph_threshold'], args['results'], name=f'HC_graph_{measure}', overwrite=args['overwrite'], perms=args['perms'])
            
        aan_bundle = multiprocessing.Process(target=multiprocessing_permutations, args=('aan',))
        wr_bundle = multiprocessing.Process(target=multiprocessing_permutations, args=('wr',))
        hc_bundle = multiprocessing.Process(target=multiprocessing_permutations, args=('hc',))
    
        aan_bundle.start()
        wr_bundle.start()
        hc_bundle.start()

        print(f'\nprocess id of Graph bundle one {aan_bundle.pid}')
        print(f'process id of Graph bundle one {wr_bundle.pid}')
        print(f'process id of Graph bundle one {hc_bundle.pid}')

        aan_bundle.join()
        wr_bundle.join()
        hc_bundle.join()

        print('\nFinished Processing\n')
        
        print(f'Exit code of Graph bundle one {aan_bundle.exitcode}')
        print(f'Exit code of Graph bundle two {wr_bundle.exitcode}')
        print(f'Exit code of Graph bundle three {hc_bundle.exitcode}')

    except Exception as e:
        print('The following exception occured:', e)
    
    time.stop()
    sys.stdout.close()
    args = arguments()