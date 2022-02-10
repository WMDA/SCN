'''
Useful functions. Contains functions to load data as well as metrics on data processing.
'''

import time
import pandas as pd

class TimeError(Exception):
    """Custom Timer Exception"""

class MeasureError(Exception):
    """Custom measure exception"""

class Timer:

    '''
    Custom Class to time how long scripts take to run.

    Usage:
    
    from functions.utils import Timer

    timer = Timer()
    timer.start()
    <code here>
    timer.stop()
    '''

    def __init__(self):
        self.__start = None

    def start(self):
        
        if self.__start is not None:
            raise TimeError("Timer is already started")

        self.__start = time.perf_counter()

    def stop(self):
        
        if self.__start is None:
            raise TimeError("Timer has not been started. Use .start() to start timer")
        
        time_taken = time.perf_counter() - self.__start
        self.__start = None
        
        if time_taken > 60:
            time_taken = time_taken / 60
            print(f"Finished in {time_taken} mins")

        else:
            print(f"Finished in {time_taken} seconds")

def load_data(measure, data):

    '''
    Function to load data. 

    Parameters
    -------------
    measure: str, which cortical measure to load. 
             options are volume, area and lgi
    data: str, absolute path to data

    Returns
    -------------
    results: dict of aan, wr, hc pd.dataframes,
             names of brain regions, list and
             centroids (co-ordinates) numpy array
    '''

    measure = measure.lower()
    
    if measure == 'lgi':
        try: 
            lh_measure = pd.read_csv(f'{data}/lh_lgi.dat', sep='\t').drop([
                     'BrainSegVolNotVent', 'eTIV'], axis=1).rename(columns={'lh.aparc.pial_lgi.thickness':'G-Number'})
            rh_measure =  pd.read_csv(f'{data}/rh_lgi.dat', sep='\t').drop([
                       'BrainSegVolNotVent', 'eTIV','rh.aparc.pial_lgi.thickness'], axis=1)
        
        except Exception:
            print('Unable to load files')

    elif measure == 'area':
        
        try:
            lh_measure = pd.read_csv(f'{data}/lh_area.dat',sep='\t').drop(['lh_WhiteSurfArea_area',
                                   'BrainSegVolNotVent', 'eTIV'],axis=1).rename(columns={'lh.aparc.area':'G-Number'})          
            rh_measure =  pd.read_csv(f'{data}/rh_area.dat',sep='\t').drop(['rh_WhiteSurfArea_area',
                                    'BrainSegVolNotVent', 'eTIV','rh.aparc.area'],axis=1)

        except Exception as e:
            print('Unable to load files', e)

    elif measure == 'volume':
        
        try:
            lh_measure = pd.read_csv(f'{data}/lh_volume.dat',sep='\t').drop([
                                     'BrainSegVolNotVent', 'eTIV'],axis=1).rename(columns={'lh.aparc.volume':'G-Number'})
            rh_measure =  pd.read_csv(f'{data}/rh_volume.dat',sep='\t').drop([
                                      'BrainSegVolNotVent', 'eTIV','rh.aparc.volume'],axis=1)
                                  
        except Exception as e:
            print('Unable to load files', e)

    else:
        raise MeasureError('Unknown Measure. Please use LGI, area or volume (case independent). Use -h further help')
                       
    group = pd.read_csv(f'{data}/cortical_measures.csv').iloc[0:,2]
    volume = pd.concat([lh_measure, rh_measure, group],axis=1)
    names = list(volume.columns.drop(['G-Number','age_adjusted_group']))
    centroids = pd.read_csv(f'{data}/atlas.csv')
    centroids = centroids[['x.mni', 'y.mni', 'z.mni']].to_numpy()

    group = volume.groupby('age_adjusted_group')  
    aan = group.get_group('AAN').reset_index(drop=True)
    hc = group.get_group('HC').reset_index(drop=True)
    wr = group.get_group('WR').reset_index(drop=True) 

    results ={
        'aan': aan,
        'wr': wr,
        'hc' : hc,
        'names': names,
        'centroids': centroids
    }   

    return results