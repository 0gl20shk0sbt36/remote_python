import os
from json import dumps
from time import sleep
from socket import socket

__print = print
__input = input

conn = None  # type: socket


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
            except ConnectionResetError:
                return 'error', 'ConnectionResetError'
        data += n[:-1]
        if n[-1] == 0:
            return data


def send(s, n, a=0):
    i = -1024
    for i in range(0, len(n) // 1024 * 1024, 1024):
        s.send(n[i: i + 1024] + b'\x01')
    s.send(n[i + 1024:] + bytes([a]))


def print(*args, **kwargs):
    send(conn, dumps({'args': args, 'kwargs': kwargs}).encode(), 2)
    sleep(0.1)


def input(*args, **kwargs):
    send(conn, dumps({'args': args, 'kwargs': kwargs}).encode(), 4)
    n = recv(conn)
    if type(n) == tuple:
        return n
    else:
        return str(n, 'utf-8')


def walk():
    return list(os.walk(os.getcwd()))[0]


class Instructions:

    def __init__(self):
        self.v = {}

    def instructions(self, ndsvbsuiadsnbdkacnjbisavaiakavajnkvaaiaosniviasnvias):
        locals().update(self.v)
        exec(ndsvbsuiadsnbdkacnjbisavaiakavajnkvaaiaosniviasnvias)
        self.v = locals()

    def conn(self, conn_):
        global conn
        conn = conn_
