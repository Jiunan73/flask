#tcpclient.py
import sys
import socket
import threading
import os

def connectTCP(ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip,port))
    return client
def readFromServer(remote_server):
    read_buff = ''
    while True:
        read_a_char = remote_server.recv(1).decode('utf-8')
        if read_a_char != '\n':
            read_buff += read_a_char
        else:
            print(read_buff)
            read_buff = ''

def main():
    remote_server = connectTCP('127.0.0.1',4001)
    p = threading.Thread(target=readFromServer,args=(remote_server,))
    p.start()
    read_buff = ''
    while True:
        read_a_char = sys.stdin.read(1)
        if read_a_char != '\n':
            read_buff += read_a_char
        else:
            if read_buff=='q':
                remote_server.close()
                os._exit(0)
            remote_server.sendall((read_buff + '\n').encode('utf-8'))
            read_buff = ''

if __name__ == '__main__':
    main()
