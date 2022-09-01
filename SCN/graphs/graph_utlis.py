import pickle
import os
from decouple import config


def save_pickle(name: str, object_to_pickle) -> None:

    pickle_path = os.path.join(config('root'), 'work/pickle')

    with open(f'{pickle_path}/{name}.pickle', 'wb') as handle:
        pickle.dump(object_to_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(name_of_pickle_object: str) -> object:

    pickle_path = os.path.join(config('root'), 'work/pickle')

    try: 
        with open(f'{pickle_path}/{name_of_pickle_object}.pickle', 'rb') as handle:
            return pickle.load(handle)
    
    except FileNotFoundError:
        print(f'Unable to load pickle file {pickle_path}/{name_of_pickle_object} Please check the pickle object exists')