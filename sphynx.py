import os

from .dragon import Dragon
from .eagle import Eagle, OwlBear


class Sphynx:
    def __init__(self): pass
    
    # static animal
    def add_dragon(self, *args): self.dragon = Dragon(*args)

    # concrete animal
    def add_lion(self, cls, *args, debug=False): self.lion = cls(*args, debug=debug)

    # symbolic animal
    def add_eagle(self, *args, **kwargs): 
        if getattr(self, 'lion'): kwargs['concrete_target'] = OwlBear(self.lion)
        self.eagle = Eagle(*args, **kwargs)




    

'''
maybe sphynx can be inside a contextmanager then dragon and pwn would work
'''