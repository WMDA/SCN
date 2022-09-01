import multiprocessing

class Random_Graph_Creator:

    def __init__(self) -> None:
        pass

    def data(self, *data) -> dict:

        return dict(zip([f'group_{data}'for key in range(len(data))], [group for group in data]))

    #def permutations(self):





    




        