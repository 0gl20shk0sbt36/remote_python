import socket
# from time import sleep
from pickle import dumps, loads
from traceback import format_exc
from json import loads
from os import listdir
from os.path import join
from fold import folds_conversion

from psutil import disk_partitions

from instructions import Instructions, recv, send
from sys import stdout
from ctypes import windll


# red
def print_red(mess):
    STD_OUTPUT_HANDLE = -11
    FOREGROUND_RED = 0x0c  # red.
    FOREGROUND_BLUE = 0x09  # blue.
    FOREGROUND_GREEN = 0x0a  # green.
    std_out_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleTextAttribute(std_out_handle, FOREGROUND_RED)
    stdout.write(mess + '\n')
    windll.kernel32.SetConsoleTextAttribute(std_out_handle, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


def main():
    instructions = Instructions()
    state = 'cloud'  # native:本地, cloud:云端
    n_ = []
    for i in disk_partitions():
        if 'removable' in i.opts:
            if 'password.txt' in listdir(i.device):
                n_.append(join(i.device, 'password.txt'))
    n = None
    for i in n_:
        with open(i) as f:
            try:
                n = folds_conversion(f.read(), 4)
            except:
                pass
    if n is None:
        n = input('链接：')
    else:
        n = '.'.join([str(i) for i in n])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((n, 10000))
    # print(s.recv(1024))
    while True:
        n = input('>>>')
        if not n:
            continue
        if n[-1] == ':':
            while True:
                n_ = input('...')
                if n_:
                    n += '\n'
                    n += n_
                else:
                    break
        if n == 'quit()':
            send(s, n.encode())
            break
        if n == 'quit(0)':
            send(s, n.encode())
            break
        if n == 'quit(1)':
            send(s, n.encode())
            break
        elif n == 'native':
            state = 'native'
            continue
        elif n == 'cloud':
            state = 'cloud'
            continue
        if state == 'native':
            n_ = n.split()
            if n_[0] == 'send' and len(n_) == 3:
                send(s, b'send_to ' + n_[1].encode())
                print(instructions.v[n_[2]])
                send(s, dumps(instructions.v[n_[2]]))
                recv(s)
            else:
                try:
                    instructions.instructions(n)
                except:
                    print_red(format_exc())
        elif state == 'cloud':
            n_ = n.split()
            if n_[0] == 'send' and len(n_) == 3:
                send(s, n.encode())
                n = recv(s)
                instructions.instructions(f'{n_[1]} = {loads(n[0])}')
            else:
                send(s, n.encode())
                while True:
                    n = recv(s)
                    data, mode = n
                    if mode == 0:
                        if data != b'\x00':
                            print(str(n[0], 'utf-8'))
                        break
                    elif mode == 2:
                        n = loads(data)
                        print(*n['args'], **n['kwargs'])
                    elif mode == 3:
                        # print('\033[31m', end='')
                        # print(str(data, "utf-8"), end='')
                        # print('\033[0m')
                        print_red(str(data, "utf-8"))
                        break
                    elif mode == 4:
                        n = loads(data)
                        send(s, input(*n['args'], **n['kwargs']).encode())
    s.close()


# input()


if __name__ == '__main__':
    main()
