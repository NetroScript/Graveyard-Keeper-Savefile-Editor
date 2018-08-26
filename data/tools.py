import struct

structtypes = {
        'int8': ['b', 1],
        'uint8': ['B', 1],
        'int16': ['h', 2],
        'uint16': ['H', 2],
        'int32': ['i', 4],
        'uint32': ['I', 4],
        'int64': ['q', 8],
        'uint64': ['Q', 8],
        'float': ['f', 4],
        'double': ['d', 8],
        'char': ['s', 1]
}

class BinaryReader:

    def __init__(self, file):
        self.file = file

    def read(self, typ):
        form, size = structtypes[typ]
        val = self.file.read(size)
        return struct.unpack(form, val)[0]


class BinaryWriter:

    def __init__(self, file):
        self.file = file

    def write(self, typ, val):
        form = structtypes[typ][0]
        self.file.write(struct.pack(form, val))
