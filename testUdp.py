import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "message"
while True:
    sock.sendto(message, ("127.0.0.1", 10000))
    print ("send message", time.time())
    time.sleep(1)
