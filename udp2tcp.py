UDP_PORT = 10000
TCP_PORT = 10001
from ClassDesc import ClassDesc, ETypes

classDesc = ClassDesc(False)
classDesc.addMember("intM", ETypes.UnsignedInt)
classDesc1 = ClassDesc(False)
classDesc1.addStringMember("str", 4)
classDesc1.addMember("flt", ETypes.Float)
classDesc2 = ClassDesc(False)
classDesc2.addMember("flt", ETypes.Float)
classDesc2.addStringMember("str", 4)


def gotMessage(message):
    try:
        dat = classDesc.getInstance(message[:4])
        print dat
        if dat['intM'] == 1:
            print classDesc1.getInstance(message[4:])
        else:
            print classDesc2.getInstance(message[4:])
    except:
        pass


def isImportant(message):
    dat = classDesc.getInstance(message)
    if dat['intM'] == 1:
        return True
    else:
        return False


def clientConnect(client, clients):
    for c in clients:
        c.close()


from Server import Server

s = Server(UDP_PORT, TCP_PORT, tcpTimeout=1.0, importantMessageTimeout=10)
s.setOnGotMessage(gotMessage)
s.setIsImportant(isImportant)
s.setOnClientConnect(clientConnect)
s.startServer()
