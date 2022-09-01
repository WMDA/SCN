import pickle
import os
from decouple import config


def save_pickle(name: str, object_to_pickle) -> None:

    pickel_path = os.path.join(config('root'), 'work/pickle')

    with open(f'{pickel_path}/{name}.pickle', 'wb') as handle:
        pickle.dump(object_to_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(name_of_pickle_object: str) -> object:

    pickel_path = os.path.join(config('root'), 'work/pickle')

    with open(f'{pickel_path}/{name_of_pickle_object}.pickle', 'rb') as handle:
        return pickle.load(handle)
