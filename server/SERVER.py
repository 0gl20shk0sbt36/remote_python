import socket
import traceback
from sys import exc_info
from instructions import Instructions, send, recv
from os import system
from fold import increases_conversion
import pickle


def main():
    run = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 10000))
    print(socket.gethostbyname(socket.gethostname()))
    with open('password.txt', 'w') as f:
        f.write(increases_conversion([int(i) for i in socket.gethostbyname(socket.gethostname()).split('.')],
                                     1024 * 2 ** 9))
    s.listen(1)
    while run:
        conn, address = s.accept()
        print(f'{address}连接成功')
        conn.setblocking(False)
        # v = {}
        instructions = Instructions()
        instructions.conn(conn)
        while True:
            try:
                n = recv(conn)
                if type(n) == tuple:
                    break
                else:
                    n = str(n, 'utf-8')
                if n == 'quit()':
                    break
                elif n == 'quit(0)':
                    system('shutdown -s -t 0')
                    break
                elif n == 'quit(1)':
                    run = False
                    break
                try:
                    if n.split()[0] == 'send':
                        n = n.split()
                        if len(n) == 2:
                            send(conn, str(instructions.v[n[1]]).encode())
                            continue
                        elif len(n) == 3:
                            send(conn, pickle.dumps(instructions.v[n[2]]))
                    instructions.instructions(n)  # main(n, v)
                    n = None
                    e = None
                except:
                    n = traceback.format_exc()
                    e = exc_info()[0]
                if e == ConnectionAbortedError:
                    break
                if n is None:
                    send(conn, b'\x00')
                else:
                    if e is not None:
                        send(conn, str(n).encode(), 3)
                    else:
                        send(conn, str(n).encode())
            except BlockingIOError:
                pass
        conn.close()
        print(f'{address}断开链接')
    s.close()


if __name__ == '__main__':
    main()
