#tcpclient.py
import sys
import socket
import threading
import os

def connectTCP(ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip,port))
    return client
def main():
    while True:
	remote_server = connectTCP('10.97.82.24',5001)
	time.sleep(5)
        remote_server.close()
	time.sleep(1)
if __name__ == '__main__':
    main()
