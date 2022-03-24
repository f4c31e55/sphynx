import os

from dragon import Dragon


class Sphynx:
    def __init__(self): pass
    
    # static animal
    def add_dragon(self, *args): self.dragon = Dragon(*args)

    # concrete animal
    def add_lion(self, cls, *args, debug=False): self.lion = cls(*args, debug=debug)





    

'''
maybe sphynx can be inside a contextmanager then dragon and pwn would work
'''