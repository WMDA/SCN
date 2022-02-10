import functions.statistical_functions as Sfun
import pandas as pd
import argparse

def options():
    args = argparse.ArgumentParser()
    args.add_argument('-d', '--data', dest='data', help='File path to data. If left blank will search for .env file')
    args.add_argument('-r', '--results', dest='results', help='File path to results. If left blank will search for .env file')
    args.add_argument('-l', '--logs', dest='logs', help='File path to log files. If left blank will search for .env file')
    args.add_argument('-m', '--measure', dest='measure', help='Specify measure, i.e LGI, area')
    args.add_argument('-o', '--overwrite', dest='overwrite', help='Set overwrite to be true', action='store_true')
    args.add_argument('-p', '--perms', dest='perms', help='Specify number of permutations')

    flags = vars(args.parse_args())

    if not flags['measure']:
        args.error('No measure provided. Please specify -m with a measure. use -h or --help')
    
    elif not flags['perms']:
        args.error('Number of permutations not provided. Please specify -p with a number. use -h or --help')

    return flags


def main(data,results,measure,overwrite,perms):
    measure = measure.lower()
    if measure == 'lgi':
        try: 
            
            lh_measure = pd.read_csv(f'{data}/lh_lgi.dat',sep='\t').drop([
                     'BrainSegVolNotVent', 'eTIV'],axis=1).rename(columns={'lh.aparc.pial_lgi.thickness':'G-Number'})
                     
            rh_measure =  pd.read_csv(f'{data}/rh_lgi.dat',sep='\t').drop([
                       'BrainSegVolNotVent', 'eTIV','rh.aparc.pial_lgi.thickness'],axis=1)
        
        except Exception:
            print('Unable to load files')

    else:
        
        try:
            lh_measure = pd.read_csv(f'{data}/lh_{measure}.dat',sep='\t').drop([
                     'BrainSegVolNotVent', 'eTIV'],axis=1).rename(columns={'lh.aparc.volume':'G-Number'})
            
            rh_measure =  pd.read_csv(f'{data}/rh_{measure}.dat',sep='\t').drop([
                       'BrainSegVolNotVent', 'eTIV','rh.aparc.volume'],axis=1)

        except Exception:
            print('Unable to load files')
                       
    group = pd.read_csv(f'{data}/cortical_measures.csv').iloc[0:,2]
    volume = pd.concat([lh_measure, rh_measure, group],axis=1)
    names = list(volume.columns.drop(['G-Number','age_adjusted_group']))
    centroids = pd.read_csv(f'{data}/atlas.csv')
    centroids = centroids[['x.mni', 'y.mni', 'z.mni']].to_numpy()

    group = volume.groupby('age_adjusted_group')  
    aan = group.get_group('AAN').reset_index(drop=True)
    hc = group.get_group('HC').reset_index(drop=True)
    wr = group.get_group('WR').reset_index(drop=True)

    aan_graphs = Sfun.create_graphs(aan.iloc[:,1:69], names, centroids)
    wr_graphs = Sfun.create_graphs(wr.iloc[:,1:69], names, centroids)
    hc_graphs = Sfun.create_graphs(hc.iloc[:,1:69], names, centroids)

    aan_bundle = Sfun.permutations(aan_graphs['graph_threshold'], results, name=f'AAN_graph_{measure}', overwrite=overwrite, perms=perms)
    wr_bundle = Sfun.permutations(wr_graphs['graph_threshold'], results, name=f'WR_graph_{measure}', overwrite=overwrite, perms=perms)
    hc_bundle = Sfun.permutations(hc_graphs['graph_threshold'], results, name=f'HC_graph_{measure}', overwrite=overwrite, perms=perms)

if __name__=='__main__':
    
    from functions.utils import Timer
    from decouple import config
    import sys
    from datetime import datetime
    import os
    
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

    date_time = datetime.now()

    log_name = date_time.strftime('logFile_%S%M_%Y.txt')

    os.system(f'touch {logs}/{log_name}')
    sys.stdout = open(f'{logs}/{log_name}','w')

    print(date_time)
    
    time = Timer()
    time.start()
    
    try:
        
        main(data, results, args['measure'], args['overwrite'] ,perms)
    
    except Exception as e:
        print('The following exception occured:', e)
    
    time.stop()
    sys.stdout.close()


