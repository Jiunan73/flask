import socket
import random,time

address = ('127.0.0.1', 6500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    X=random.randint(0,300)
    Y=random.randint(0,300)
    msg = str(X) +','+ str(Y) + '\n'
    
    s.sendto(msg, address)
    time.sleep(1)
s.close()

