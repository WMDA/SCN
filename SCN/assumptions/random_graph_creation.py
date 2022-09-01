import multiprocessing

class Random_Graph_Creator:

    def __init__(self) -> None:
        pass

    def data(self, *kargs) -> dict:

        return dict(zip([f'group_{key}'for key in range(len(kargs))], [group for group in kargs]))

    #def permutations(self):





    




        