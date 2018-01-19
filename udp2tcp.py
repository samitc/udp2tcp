UDP_PORT = 10000
TCP_PORT = 10001
from Server import Server

s = Server(UDP_PORT, TCP_PORT, tcpTimeout=1.0)
s.startServer()
# import pickle
# class TestClass:
#    var1=1
#    var2=4
#    def __str__(self):
#        return "var1=" + str(self.var1 )+ ",var2=" + str(self.var2)
# teswtDic={3:"342423",5:7,11:"343"}
# teswtDic=TestClass()
# testStr= pickle.dumps(teswtDic,protocol=2)
# newDic=pickle.loads(testStr)
# print (str(teswtDic))
# print (testStr)
# print (str(newDic))


# import struct
# import binascii
#
# values = (1, 'abcd', 2.7)
# s = struct.Struct('! I 4s f')
# packed_data = s.pack(*values)
#
# print 'Original values:', values
# print 'Format string  :', s.format
# print 'Uses           :', s.size, 'bytes'
# print 'Packed Value   :', binascii.hexlify(packed_data)
# import struct
# import binascii
#
# packed_data = binascii.unhexlify(binascii.hexlify(packed_data))
#
# s = struct.Struct('! I 4s f')
# unpacked_data = s.unpack(packed_data)
# print 'Unpacked Values:', unpacked_data
