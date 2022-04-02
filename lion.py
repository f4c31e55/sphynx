import os, atexit
from pwn import process, gdb, context
'''
lion is basically avatar
but we need to leave the gdb for our interactive so shrug
'''

class Lion:
    def __init__(self, gdb_port=None):
        if gdb_port: 
            _, self.gdb = gdb.attach(('127.0.0.1', gdb_port), exe=1, api=True)
    
    def rm(self, addr, size): return self.gdb.selected_inferior().read_memory(addr,size).tobytes()
    def wm(self, addr, data): return self.gdb.selected_inferior().write_memory(addr,data)
    def rr(self, r): 
        return int(self.gdb.parse_and_eval(f'${r}').cast(self.gdb.lookup_type('unsigned int')))
    def wr(self, r, v): return self.gdb.execute(f'set ${r}={v}')

    def run_shellcode(self, code):
        loc = self.rr('pc')
        save = self.rm(loc, len(code))        
        self.wm(loc, code)
        
        class RestoreBP(self.gdb.Breakpoint):
            def stop(s):
                self.wr('pc', loc)
                self.wm(loc, save)
                return True
        RestoreBP("*"+hex(loc+len(code)), temporary=True)
        self.gdb.continue_and_wait()



class Panda(Lion):
    ''' a lion that expects a pypanda script '''
    def __init__(self, *args, debug=True, image='pandare/panda', script='panda.py'):
        global process
        self.process = process

        self.console = self.process([
            "docker","run","--name","sphynx","--rm",
            "-e",'TERM=xterm', # for term things
            "-v",os.path.dirname(os.path.abspath(script))+":/host", # for script sharing
            '-v','/tmp:/tmp', # for pwntools gdb
            "--network","host", # for gdb
            image,
            "python3",'-u',os.path.join("/host",script)])
        
        atexit.register(lambda: self.process(['docker', 'kill', 'sphynx']).recvuntil(b'sphynx'))

        super().__init__(1234)
