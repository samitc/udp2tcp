import socket
import threading
import time

from TcpClient import TcpClient


class Server:
    def __init__(self, udpPort, tcpPort, closeServerWhenNoData=True, useTimeout=True, closeOnlyWhenNoClient=True,
                 importantMessageRetrying=True, importantMessageTimeout=1.0,
                 tcpTimeout=1.0,
                 bufferSize=4096):
        self.udpPort = udpPort
        self.tcpPort = tcpPort
        self.bufferSize = bufferSize
        self.isConnect = False
        self.tcpTimeout = tcpTimeout
        self.useTimeout = useTimeout
        self.recData = 0
        self.closeServerWhenNoData = closeServerWhenNoData
        self.closeOnlyWhenNoClient = closeOnlyWhenNoClient
        self.importantMessageRetrying = importantMessageRetrying
        self.importantMessageTimeout = importantMessageTimeout
        self.tcpClients = []
        self.importantMessage = []
        self.serverRun = True
        self.setOnGotMessage(None)
        self.setIsImportant(None)
        self.setOnClientConnect(None)

    def startServer(self):
        udpIp = "127.0.0.1"
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSock.bind((udpIp, self.udpPort))
        data, addr = self.udpSock.recvfrom(self.bufferSize)
        self.gotMessage(data)
        self.serverThread = threading.Thread(target=self.connectTcp)
        self.serverThread.start()
        while self.serverRun:
            try:
                data, addr = self.udpSock.recvfrom(self.bufferSize)
                self.recData = self.recData + 1
                self.gotMessage(data)
            except KeyboardInterrupt:
                self.serverRun = False
            except:
                pass

    def gotMessage(self, data):
        self.sendToTcp(data)
        isImportant = False
        if self.importantMessageRetrying and self.isImportantHandle is not None:
            isImportant = self.isImportantHandle(data)
        if isImportant:
            self.importantMessage.append((data, time.time()))
        if self.gotMessageHandle is not None:
            self.gotMessageHandle(data)
        self.removeOldImportant()

    def sendToTcp(self, data):
        for client in self.tcpClients:
            try:
                client.sendMessage(data)
            except IOError as e:
                client.close()
                self.tcpClients.remove(client)

    def createServerSocket(self):
        tcpIp = "127.0.0.1"
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.bind((tcpIp, self.tcpPort))
        if self.useTimeout:
            self.tcpServer.settimeout(self.tcpTimeout)
        self.tcpServer.listen(0)

    def connectTcp(self):
        curRecData = self.recData
        isConnect = False
        while self.serverRun:
            newData = curRecData == self.recData
            curRecData = self.recData
            if newData is True:
                if isConnect and self.closeServerWhenNoData and (
                        not self.closeOnlyWhenNoClient or len(self.tcpClients) is 0):
                    self.tcpServer.close()
                    isConnect = False
            else:
                try:
                    if not isConnect:
                        self.createServerSocket()
                        isConnect = True
                    conn, addr = self.tcpServer.accept()
                    self.clientConnected(TcpClient(conn, addr))
                except socket.timeout as e:
                    pass
                except:
                    pass
            if self.useTimeout:
                time.sleep(self.tcpTimeout)

    def setOnGotMessage(self, gotMessageHandle):
        self.gotMessageHandle = gotMessageHandle

    def setIsImportant(self, isImportant):
        self.isImportantHandle = isImportant

    def setOnClientConnect(self, onClientConnect):
        self.onClientConnect = onClientConnect

    def clientConnected(self, client):
        if self.onClientConnect is not None:
            self.onClientConnect(client, self.tcpClients)
        self.tcpClients.append(client)
        self.sendImportandMessage(client)

    def removeOldImportant(self):
        if self.importantMessageRetrying:
            curTime = time.time()
            if self.importantMessageRetrying:
                for importantMessage in self.importantMessage:
                    if curTime > importantMessage[1] + self.importantMessageTimeout:
                        self.importantMessage.remove(importantMessage)
                    else:
                        break

    def sendImportandMessage(self, client):
        if self.importantMessageRetrying:
            self.removeOldImportant()
            for importantMessage in self.importantMessage:
                client.sendMessage(importantMessage[0])
