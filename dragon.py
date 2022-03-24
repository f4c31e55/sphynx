import os; os.environ['GHIDRA_INSTALL_DIR'] = '/home/user/tools/ghidra_10.1.2_PUBLIC/'
import pyhidra

import logging
log = logging.getLogger('dragon')
log.setLevel(logging.DEBUG)

class Dragon:
    def __init__(self, program, path, proj):
        self.path = path; self.proj=proj
        os.system(f"cp -r {os.path.join(path, proj+'.rep')} {os.path.join(path, proj+'-copy.rep')}")
        os.system(f"touch {os.path.join(path, proj+'-copy.gpr')}")
        
        # TODO: clean this up somehow - we can't close the project in __del__
        self._pyh = pyhidra.open_program(program, self.path, proj+'-copy', False)
        self.api = next(self._pyh.gen)
    
    def __del__(self):
        try: next(self._pyh.gen)
        except: pass
        os.system(f"rm -r {os.path.join(self.path,self.proj+'-copy*')}")


'''
patch to pyhidra:
    ghidra.py:41 
        # project_location = project_location / project_name
'''