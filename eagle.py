import angr
from angr_targets import ConcreteTarget
from angr_targets.memory_map import MemoryMap

import os, logging
from re import findall

log = logging.getLogger('eagle')
log.setLevel(logging.INFO)

emit = angr.misc.loggers.CuteHandler.emit
def patched_emit(self, record):
    if record.name.startswith('pwn'): return
    emit(self, record)
angr.misc.loggers.CuteHandler.emit = patched_emit


class OwlBear(ConcreteTarget):
    ''' it's really an EagleLion '''
    def __init__(self, lion):
        self.lion = lion
        self.bps = {}
    
    # now the angr_targets ConcreteTarget API
    def read_memory(self, address, nbytes):
        return self.lion.rm(address, nbytes)
    
    def write_memory(self, address, value):
        return self.lion.wm(address, value)
    
    def read_register(self, register):
        try: return self.lion.rr(register)
        except Exception as e: raise angr.SimConcreteRegisterError(f"OwlBear can't read register {register} exception {e}")
    
    def write_register(self, register, value):
        return self.lion.wr(register, value)
    
    def set_breakpoint(self, address, **kwargs): 
        return self.lion.gdb.execute(f"bp {hex(address)}")
    
    def remove_breakpoint(self, address):
        for bp in self.lion.gdb.breakpoints():
            if hex(address) in bp.location: bp.delete()
    
    def run(self): return self.lion.gdb.continue_and_wait()

    def get_mappings(self):
        vmmap = self.lion.gdb.execute('vmmap', to_string=True)
        return [
            MemoryMap(int(s,16), int(e,16), None, os.path.basename(p)) for s,e,p in findall(" (0x[0-9a-f]+).* (0x[0-9a-f]+).*?([^ ]+?)\x1b", vmmap)[::-1] if not p.startswith("[")
        ]
    
    def load_addrs(self, exe_path):

        main_opts, lib_opts = {},{}
        try:
            vmmap = self.lion.gdb.execute('vmmap', to_string=True)
            load_addrs = {os.path.basename(p):int(s,16) for s,_,p in  findall(" (0x[0-9a-f]+).* (0x[0-9a-f]+).*?([^ ]+?)\x1b", vmmap)[::-1] if not p.startswith("[")}

            main_opts = {'base_addr':y for x,y in load_addrs.items() if x == os.path.basename(exe_path)}
            lib_opts = {x:{'base_addr':y} for x,y in load_addrs.items() if x != os.path.basename(exe_path)}
        
        except Exception as e:
            log.warning(f"Couldn't get loaded addresses: {e}")


        return main_opts, lib_opts


class Eagle:
    def __init__(self, *args, **kwargs):
        self.project = angr.Project(*args, **kwargs)
    
    def execute_concretley(self, state, address, memory_concretize=[], register_concretize=[], timeout=0):
        simgr = self.project.factory.simgr(state)
        simgr.use_technique(angr.exploration_techniques.Symbion(find=[address], memory_concretize=memory_concretize,
                                                                register_concretize=register_concretize, timeout=timeout))
        exploration = simgr.run()
        return exploration.stashes['found'][0]