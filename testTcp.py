import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 10001))
try:
    while True:
        data = sock.recv(4096)
        print (data, time.time())
except:
    pass
sock.close()
