import socket

address = ('192.168.2.160', 6500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

while True:
    data, addr = s.recvfrom(2048)
    if not data:
        print "client has exist"
        break
    print "received:", data, "from", addr
    f = open('map.txt', 'w')
    f.write(data)
s.close()

