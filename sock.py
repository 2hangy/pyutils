#!/usr/bin/python2

from contextlib import contextmanager
import socket

@contextmanager
def sockctx(host, port):
    # todo: 增加异常处理
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    yield sock
    sock.close()

def main():
    with sockctx('0.0.0.0', 2333) as sock:
        sock.sendall('all hope abadon ye who enter here')
        print(sock.recv(1024))

if __name__ == '__main__':
    main()

