class TcpClient:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def sendMessage(self, data):
        self.conn.send(data)

    def close(self):
        self.conn.close()
