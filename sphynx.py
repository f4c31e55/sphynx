import os, logging

from .dragon import Dragon
from .eagle import Eagle, OwlBear
from .lion import Lion, Panda

log = logging.getLogger('sphynx')
log.setLevel(logging.INFO)

class Sphynx:
    def __init__(self): pass
    
    # static animal
    def add_dragon(self, *args): 
        log.info('Waking the dragon ...')
        self.dragon = Dragon(*args)
        return self.dragon

    # concrete animal
    def add_lion(self, *args, panda=None, **kwargs): 
        log.info('Taming the lion ...')
        if panda:
            self.lion = Panda(*args, script=panda, **kwargs)
        else:
            self.lion = Lion(*args, **kwargs)
        return self.lion

    # symbolic animal
    def add_eagle(self, *args, **kwargs): 
        log.info('Eagle taking flight ...')
        if getattr(self, 'lion', None): 
            owlbear = OwlBear(self.lion)
            kwargs['concrete_target'] = owlbear

            mo,lo = owlbear.load_addrs(args[0])
            
            main_opts = kwargs.get('main_opts', {})
            main_opts.update(mo)

            lib_opts = kwargs.get('lib_opts', {})
            lib_opts.update(lo)

            kwargs['main_opts'] = main_opts
            kwargs['lib_opts'] = lib_opts

        self.eagle = Eagle(*args, **kwargs)
        return self.eagle

'''
maybe sphynx can be inside a contextmanager then dragon and pwn would work
'''