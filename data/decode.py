from data.tools import BinaryReader
from data.types import Types
from data.corruptionfix import prefix, postfix

class Decoder:

    def __init__(self, hashes):
        self.hashes = hashes

    def decode(self, file):
        print("Beginning to decode file: " + file)
        with open(file, "rb") as f:
            b = BinaryReader(f)
            print("Extracting String Array")
            sd = self.extractserializer(b)
            header = dict()
            print("Extracting header")
            header["offset"] = b.read("int64")
            header["version"] = b.read("int32")
            for i in range(15):
                b.read("int32")
            #print(header)
            #print(sd)
            print("Extracting game objects")
            x = self.deserialize(b, sd, {})
            obj = {
                "savedata": x,
                "header": {
                    "offset": header["offset"],
                    "version": header["version"]
                },
                "serializer": sd,
                "hashes": self.hashes.name_to_hash
            }
            print("Loaded file: " + file)
            return obj

    def deserialize(self, stream, serializer,layer):

        n = stream.read("int32")

        if n == -1:
            return
        # print(num)
        # print("Following things are Serialized")

        for i in range(n):
            hash = str(stream.read("int32"))
            nam = hash
            if hash in self.hashes.hash_to_name:
                nam = self.hashes.hash_to_name[hash]
            # print("Hash: " + str(nam))
            #     pass
            layer[nam] = dict()
            # print("Deserialized Object:")
            x = self.deserializedata(stream, serializer, layer[nam], hash)

            layer[nam] = x
        return layer

    def deserializedata(self, stream, serializer, layer, hash):
        curtype = stream.read("uint8")
        self.hashes.hash_to_type[hash] = curtype
        # print("Datatype: " + str(curtype))
        if curtype == Types.SmartSerialized:
            # return deserialize(stream, serializer, layer)
            return {"v": self.deserialize(stream, serializer, layer), "type": curtype}
        elif curtype == Types.NullValue:
            return {"v": None, "type": curtype}
        elif curtype == Types.String:
            return {"v": self.extractstring(stream, False), "type": curtype}
        elif curtype == Types.String_Empty:
            return {"v": "", "type": curtype}
        elif curtype == Types.String_Indexed:
            return {"v": serializer[stream.read("int32")], "type": curtype}
        elif curtype == Types.Int32_0:
            return {"v": 0, "type": curtype}
        elif curtype == Types.Int32_1:
            return {"v": 1, "type": curtype}
        elif curtype == Types.Int32:
            return {"v": stream.read("int32"), "type": curtype}
        elif curtype == Types.Int64:
            return {"v": stream.read("int64"), "type": curtype}
        elif curtype == Types.Single:
            return {"v": stream.read("float"), "type": curtype}
        elif curtype == Types.Single_0:
            return {"v": 0, "type": curtype}
        elif curtype == Types.Single_1:
            return {"v": 1, "type": curtype}
        elif curtype == Types.Double:
            return {"v": stream.read("double"), "type": curtype}
        elif curtype == Types.Byte:
            return {"v": (stream.read("uint8")).to_bytes(1, byteorder="little"), "type": curtype}
        elif curtype == Types.Char:
            return {"v": stream.read("char"), "type": curtype}
        elif curtype == Types.Bool_True:
            return {"v": True, "type": curtype}
        elif curtype == Types.Bool_False:
            return {"v": False, "type": curtype}
        elif curtype == Types.Vector2:
            return {"x":stream.read("float"), "y": stream.read("float"), "type": "Vector2"}
        elif curtype == Types.Vector2_00:
            return {"x": 0, "y": 0, "type": "Vector2"}
        elif curtype == Types.Vector2_11:
            return {"x": 1, "y": 1, "type": "Vector2"}
        elif curtype == Types.Vector3:
            return {"x":stream.read("float"), "y": stream.read("float"), "z": stream.read("float"), "type": "Vector3"}
        elif curtype == Types.Vector3_000:
            return {"x": 0, "y": 0, "z": 0, "type": "Vector3"}
        elif curtype == Types.Vector3_111:
            return {"x": 1, "y": 1, "z": 1, "type": "Vector3"}
        elif curtype == Types.Quaternion:
            return {"x":stream.read("float"), "y": stream.read("float"), "z": stream.read("float"), "n": stream.read("float"), "type": "Quaternion"}
        elif curtype == Types.Quaternion_0001:
            return {"x": 0, "y": 0, "z": 0, "n": 1, "type": "Quaternion"}
        elif curtype == Types.ByteArray:
            amount = stream.read("int32")
            arr = []
            for i in range(amount):
                arr.append((stream.read("uint8")).to_bytes(1, byteorder="little"))
            return {"v": arr, "type": curtype}
        elif curtype == Types.GenericList:
            amount = stream.read("int32")
            arr = []
            for i in range(amount):
                arr.append(self.deserializedata(stream, serializer, {}, hash))

            return {"v": arr, "type": curtype}
        elif curtype == Types.Array:
            amount = stream.read("int32")
            arr = []
            for i in range(amount):
                arr.append(self.deserializedata(stream, serializer, {}, hash))

            return {"v": arr, "type": curtype}
        else:
            print("Datatype: " + str(curtype) + " can not be parsed")

    def extractserializer(self, stream):
        pos = stream.read("int64")
        pos2 = stream.file.tell()
        # print(pos2)
        stream.file.seek(pos)
        n = stream.read("int32")
        data = []
        # print(n)
        for i in range(n):
            data.append(self.extractstring(stream, True))
        stream.file.seek(pos2)
        return data

    def extractstring(self, stream, encrypt=False):
        n = stream.read("int32")
        # print(n)
        if(n == -1):
            return None

        buffer = []
        out = ""
        beginning = stream.file.tell()
        for i in range(n):
            # buffer.append(int.from_bytes(stream.read("char"), byteorder="little"))
            buffer.append(stream.read("int8"))
        l = stream.file.tell() - beginning
        prefix(buffer, stream, beginning, l)

        # print(num4)
        if encrypt:
            for i in range(l):
                num5 = buffer[i]
                if num5 <= 255 and num5 is not 0 and num5 is not 109:
                    buffer[i] = chr(abs(num5 ^ 0x6D))
                else:
                    buffer[i] = chr(abs(num5))
        else:
            for i in range(l):
                buffer[i] = chr(abs(buffer[i]))

        for char in buffer:
            out += str(char)
       
        out = postfix(out, stream, buffer)
        #print(out)

        return out
