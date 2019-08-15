import struct

TYPES = {
    'bool': "?",
    'char': "B",
    'short': "h",
    'int': "i",
    'long': "q",
    'ushort': "H",
    'uint': "I",
    'ulong': "Q",
    'float': "f",
    'double': "d",
}


def GetBytes(value, typ):
    return struct.pack(TYPES[typ], value)


def DoubleToInt64Bits(value: float):
    byte = struct.pack('d', value)
    return struct.unpack('q', byte)


def Int64BitsToDouble(value: int) -> float:
    byte = struct.pack('q', value)
    return struct.unpack('d', byte)


def ToBoolean(value: bytearray, startIndex: int) -> bool:
    return bool(value[startIndex])


def ToChar(value: bytearray, startIndex: int) -> int:
    return struct.unpack("b", value[startIndex:startIndex+1])[0]


def ToDouble(value: bytearray, startIndex: int) -> float:
    return struct.unpack("d", value[startIndex:startIndex+8])[0]


def ToInt16(value: bytearray, startIndex: int) -> int:
    return struct.unpack("h", value[startIndex:startIndex+2])[0]


def ToInt32(value: bytearray, startIndex: int) -> int:
    return struct.unpack("i", value[startIndex:startIndex+4])[0]


def ToInt64(value: bytearray, startIndex: int) -> int:
    return struct.unpack("q", value[startIndex:startIndex+8])[0]


def ToSingle(value: bytearray, startIndex: int) -> float:
    return struct.unpack("f", value[startIndex:startIndex+4])[0]


def ToString(value, *args):
    if len(args) == 0:
        return value.decode()
    elif len(args) == 1:
        startIndex = args[0]
        return value[startIndex:].decode()
    elif len(args) == 2:
        startIndex = args[0]
        length = args[1]
        return value[startIndex:startIndex+length].decode()


def ToUInt16(value: bytearray, startIndex: int) -> int:
    return struct.unpack("H", value[startIndex:startIndex+2])[0]


def ToUInt32(value: bytearray, startIndex: int) -> int:
    return struct.unpack("I", value[startIndex:startIndex+4])[0]


def ToUInt64(value: bytearray, startIndex: int) -> int:
    return struct.unpack("Q", value[startIndex:startIndex+8])[0]
