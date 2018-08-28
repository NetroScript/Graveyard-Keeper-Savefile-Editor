from data.tools import BinaryWriter
from data.types import Types

class Encoder:

    def __init__(self):
        self.hashes = {}

    def encode(self, file_path, data):
        self.hashes = data["hashes"]
        with open(file_path, "wb") as fi:
            print("Beginning to encode to: " + file_path)
            bw = BinaryWriter(fi)
            bw.write("int64", 0)
            print("Writing header")
            bw.write("int64", data["header"]["offset"])
            bw.write("int32", data["header"]["version"])
            for i in range(15):
                bw.write("int32", 0)
            print("Writing gamedata")
            self.serialize(data["savedata"], bw, data["serializer"])
            print("Writing strings")
            self.insertserializer(bw, data["serializer"])
            print("Finished saving file: " + file_path)
    
    def serialize(self, data, stream, serializer):
        if data is None:
            stream.write("int32", -1)
        else:
            stream.write("int32", len(data))
            #print(len(data))
            i = 0
            for key in data:
                if type(key) is str and key in self.hashes:
                    hash = int(self.hashes[key])
                else:
                    hash = int(key)
                #print(hash)
                stream.write("int32", hash)
                self.serializedata(data[key], stream, serializer, hash)
                i+=1

    def serializedata(self, data, stream, serializer, hash):

        if type(data) is dict and "type" in data:
            if data["type"] == "Vector2":
                if data["x"] == 0 and data["y"] == 0:
                    curtype = Types.Vector2_00.value
                elif data["x"] == 1 and data["y"] == 1:
                    curtype = Types.Vector2_11.value
                else:
                    curtype = Types.Vector2.value
            elif data["type"] == "Vector3":
                if data["x"] == 0 and data["y"] == 0 and data["z"] == 0:
                    curtype = Types.Vector3_000.value
                elif data["x"] == 1 and data["y"] == 1 and data["z"] == 1:
                    curtype = Types.Vector3_111.value
                else:
                    curtype = Types.Vector3.value
            elif data["type"] == "Quaternion":
                if data["x"] == 0 and data["y"] == 0 and data["z"] == 0 and data["n"] == 1:
                    curtype = Types.Quaternion_0001.value
                else:
                    curtype = Types.Quaternion.value

            if "v" in data:
                curtype = data["type"]
                data = data["v"]
    
        stream.write("uint8", curtype)
        if curtype == Types.SmartSerialized:
            self.serialize(data, stream, serializer)
        elif curtype == Types.NullValue:
            pass
        elif curtype == Types.String:
            self.insertstring(data,stream, False)
        elif curtype == Types.String_Empty:
            pass
        elif curtype == Types.String_Indexed:

            try:
                indx = serializer.index(data)
            except ValueError:
                indx = 0
                for i in range(len(serializer)):
                    if type(serializer[i]) == dict:
                        if data == serializer[i]["string"]:
                            indx = i
                            break

            stream.write("int32", indx)
        elif curtype == Types.Int32_0:
            pass
        elif curtype == Types.Int32_1:
            pass
        elif curtype == Types.Int32:
            stream.write("int32", data)
        elif curtype == Types.Int64:
            stream.write("int64", data)
        elif curtype == Types.Single:
            stream.write("float", float(data))
        elif curtype == Types.Single_0:
            pass
        elif curtype == Types.Single_1:
            pass
        elif curtype == Types.Double:
            stream.write("double", data)
        elif curtype == Types.Byte:
            return stream.write("uint8", data)
        elif curtype == Types.Char:
            return stream.write("char", data)
        elif curtype == Types.Bool_True:
            pass
        elif curtype == Types.Bool_False:
            pass
        elif curtype == Types.Vector2:
            stream.write("float", data["x"])
            stream.write("float", data["y"])
        elif curtype == Types.Vector2_00:
            pass
        elif curtype == Types.Vector2_11:
            pass
        elif curtype == Types.Vector3:
            stream.write("float", data["x"])
            stream.write("float", data["y"])
            stream.write("float", data["z"])
        elif curtype == Types.Vector3_000:
            pass
        elif curtype == Types.Vector3_111:
            pass
        elif curtype == Types.Quaternion:
            stream.write("float", data["x"])
            stream.write("float", data["y"])
            stream.write("float", data["z"])
            stream.write("float", data["n"])
        elif curtype == Types.Quaternion_0001:
            pass
        elif curtype == Types.ByteArray:
            stream.write("int32", len(data))
            for i in range(len(data)):
                stream.write("uint8", data[i])
        elif curtype == Types.GenericList:
            stream.write("int32", len(data))
            for i in range(len(data)):
                self.serializedata(data[i], stream, serializer, hash)
        elif curtype == Types.Array:
            stream.write("int32", len(data))
            for i in range(len(data)):
                self.serializedata(data[i], stream, serializer, hash)
        else:
            print("Datatype: " + str(curtype) + " can not be parsed")
    
    def insertstring(self, string, stream, encrypt=False):
        if string is None:
            stream.write("int32", -1)
            return
        if type(string) == dict:
            stream.write("int32", string["length"])
            for byte in string["buffer"]:
                stream.write("int8", byte)
        else:
            stream.write("int32", len(string))
            for char in string:
                n = ord(char)
                if encrypt:
                    if n <= 255 and n != 0 and n != 109:
                        n ^= 0x6D
                stream.write("uint8", n)
    
    def insertserializer(self, stream, serializer):
        pos = stream.file.tell()
        stream.file.seek(0)
        stream.write("int64", pos)
        stream.file.seek(pos)
        stream.write("int32", len(serializer))
        for i in range(len(serializer)):
            self.insertstring(serializer[i], stream, True)
