from struct import Struct


class ETypes:
    EMPTY_BYTE = 0
    Char = 1
    SignedChar = 2
    UnsignedChar = 3
    Bool = 4
    Short = 5
    UnsignedShort = 6
    Int = 7
    UnsignedInt = 8
    Long = 9
    UnsignedLong = 10
    Float = 11
    Double = 12
    String = 13
    convertMap = dict()

    def __init__(self, type):
        self.type = type

    @staticmethod
    def initMap():
        ETypes.convertMap[ETypes.EMPTY_BYTE] = 'x'
        ETypes.convertMap[ETypes.Char] = 'c'
        ETypes.convertMap[ETypes.SignedChar] = 'b'
        ETypes.convertMap[ETypes.UnsignedChar] = 'B'
        ETypes.convertMap[ETypes.Bool] = '?'
        ETypes.convertMap[ETypes.Short] = 'h'
        ETypes.convertMap[ETypes.UnsignedShort] = 'H'
        ETypes.convertMap[ETypes.Int] = 'i'
        ETypes.convertMap[ETypes.UnsignedInt] = 'I'
        ETypes.convertMap[ETypes.Long] = 'q'
        ETypes.convertMap[ETypes.UnsignedLong] = 'Q'
        ETypes.convertMap[ETypes.Float] = 'f'
        ETypes.convertMap[ETypes.Double] = 'd'
        ETypes.convertMap[ETypes.String] = 's'

    @staticmethod
    def getDesc(type):
        return ETypes.convertMap[type]


ETypes.initMap()


class ClassDesc:
    def __init__(self, isLittleEndian):
        self.members = []
        self.hasChanged = False
        self.isLittleEndian = isLittleEndian

    def addMember(self, name, type, maxCount=1):
        self.members.append((name, (type, maxCount)))
        self.hasChanged = True

    def addStringMember(self, name, charMaxCount):
        self.addMember(name, ETypes.String, charMaxCount)

    def calcStructFormat(self):
        self.frt = '<' if self.isLittleEndian else '>'
        for member in self.members:
            type = member[1][0]
            size = member[1][1]
            self.frt += " "
            if size > 1:
                self.frt += str(size)
            self.frt += ETypes.getDesc(type)
        self.s = Struct(self.frt)
        self.hasChanged = False

    def getInstance(self, data):
        if self.hasChanged:
            self.calcStructFormat()
        unpackData = self.s.unpack_from(data)
        return self.createInstance(unpackData)

    def createInstance(self, unpackData):
        instance = dict()
        i = 0
        for member in self.members:
            size = member[1][1]
            name = member[0]
            if size > 1:
                array = []
                for j in range(size):
                    array.append(unpackData[i+j])
                instance[name] = array
                i += size
            else:
                instance[name] = unpackData[i]
                i += 1
        return instance
