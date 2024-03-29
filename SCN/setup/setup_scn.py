import datetime
import sys
import os
import argparse
from decouple import config

def arguments() -> dict:

    '''
    Function to set arguments

    Parameters
    ----------
    None.

    Returns
    -------
    arg : dict of args
    '''
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
    option.add_argument('-G', '--group-only', dest='group-only', action='store_true', help='Run only group differences. Skips assumptions workflow')
    option.add_argument('-N', '--no-logs', dest='no-logs', action='store_true', help='Does not store output in log files.' )
    option.add_argument('-t', '--threshold', dest='threshold', type=int, default=100,
                        help="Upper boundary to threshold graphs at. Default is set at 99.")
    arg = vars(option.parse_args())

    return arg

def set_up_logs(logtype: str, date_time: object, measure: str) -> None:

    '''
    Function to set up log files.

    Parameters
    ----------
    logtype: str of logtype.
    date_time: object a date_time object
    measure: str of measure

    Returns
    ------
    None
    '''

    log_path = os.path.join(config('root'), 'logs')
    log_name = date_time.strftime(f'{measure}_{logtype}_logFile_%S%M_%Y.txt')
    print(f'\nSetting up log files. Log files being saved to {log_path}')
    sys.stdout = open(f'{log_path}/{log_name}','w')


def logo() -> str:
    
    '''
    Function to return SCN logo.

    Parameters
    ----------
    None

    Returns
    -------
    str of logo
    '''
    
    return (
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

def write_to_file(measure: str) -> None:

  '''
  Function to write stdoutput to a file.

  Parameters
  ----------
  measure: str of measure to be used in file name
  
  Returns
  -------
  None

  '''
   
  results_path = os.path.join(config('root'), 'results/group_differences')
  results_file_name = f'results_for_{measure}'
  sys.stdout = open(f'{results_path}/{results_file_name}','w')
