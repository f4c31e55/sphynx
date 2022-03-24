import os, atexit
from pwn import process, gdb
'''
lion is basically avatar
but we need to leave the gdb for our interactive so shrug
'''

class Lion:
    def __init__(self, gdb_port=None):
        if gdb_port: _, self.gdb = gdb.attach(('127.0.0.1', gdb_port), exe=1, api=True)
    
    def rm(self, addr, size): return self.gdb.selected_inferior().read_memory(addr,size).tobytes()


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
