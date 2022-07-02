import os, atexit
from pwn import process, gdb, context
'''
lion is basically avatar
but we need to leave the gdb for our interactive so *shrug*
'''

class Lion:
    def __init__(self, gdb_api):
        self.gdb = gdb_api
    
    def rm(self, addr, size): return self.gdb.selected_inferior().read_memory(addr,size).tobytes()
    def wm(self, addr, data): return self.gdb.selected_inferior().write_memory(addr,data)
    def rr(self, r): 
        return int(self.gdb.newest_frame().read_register(r).cast(self.gdb.lookup_type('unsigned long')))
        # return int(self.gdb.parse_and_eval(f'${r}').cast(self.gdb.lookup_type('unsigned long')))
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
    def __init__(self, *args, image='pandare/panda', script='panda.py'):
        global process,context
        self.process,self.context = process,context

        with context.quiet:
            self.console = process([
            "docker","run","--name","sphynx","--rm",
            "-e",'TERM=xterm', # for term things
            "-v",os.path.dirname(os.path.abspath(script))+":/host", # for script sharing
            '-v','/tmp:/tmp', # for pwntools gdb
            "--network","host", # for gdb
            image,
            "python3",'-u',os.path.join("/host",script)])
        
        def clean(): 
            with self.context.quiet: 
                self.process(['docker', 'kill', 'sphynx']).recvuntil(b'sphynx')
        atexit.register(clean)

        with context.quiet: _,api = gdb.attach(('127.0.0.1', 1234), exe=1, api=True)
        super().__init__(api)
