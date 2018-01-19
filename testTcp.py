import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 10001))
try:
    while True:
        print sock.recv(4096)
except:
    pass
sock.close()
