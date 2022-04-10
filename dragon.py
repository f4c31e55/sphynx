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
    
    def toAddr(self, addr): return self.api.toAddr(hex(addr))

    def emu(self):
        from ghidra.app.emulator import EmulatorHelper
        return EmulatorHelper(self.api.currentProgram)
    
    def call(self, emu, addr, *args):
        # TODO: get calling convention from eagle
        if str(self.api.currentProgram.languageID) == 'MIPS:LE:32:default':
            emu.writeRegister('ra', 0x12345678)
            emu.writeRegister('pc', addr)
            for i,a in enumerate(args):
                emu.writeRegister(f'a{i}', a)
            emu.setBreakpoint(self.toAddr(0x12345678))
            emu.run(self.api.monitor)
        else:
            raise Exception('calling convention needs implementing')

'''
patch to pyhidra:
    ghidra.py:41 
        # project_location = project_location / project_name
'''