import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = bytearray((0, 0, 0, 1, 97, 98, 99, 100, 64, 44, 204, 205))
message1 = bytearray((0, 0, 0, 2, 64, 44, 204, 205, 98, 98, 99, 100))
while True:
    sock.sendto(message, ("127.0.0.1", 10000))
    print ("send message", time.time())
    time.sleep(1)
    sock.sendto(message1, ("127.0.0.1", 10000))
    print ("send message", time.time())
    time.sleep(1)
