from data.tools import BinaryReader
from data.types import Types
from data.corruptionfix import prefix, postfix


class Decoder:

    # On Initialisation we need our Hashes object to be able to translate the numerical hashes to more readable strings
    def __init__(self, hashes):
        self.hashes = hashes

    # Decode a file, supply the path to the file here
    def decode(self, file):
        print("Beginning to decode file: " + file)
        with open(file, "rb") as f:
            # Create a instance of the Binary Reader with the path to our file
            b = BinaryReader(f)
            print("Extracting String Array")
            sd = self.extractserializer(b)
            header = dict()
            print("Extracting header")
            header["offset"] = b.read("int64")
            header["version"] = b.read("int32")

            # This is part of the header, I assume the Lazy Bear Games put this in to be able to add more header
            # information at a later points. Currently (Game version 1.034) this information is not filled
            for i in range(15):
                b.read("int32")
            # print(header)
            # print(sd)
            print("Extracting game objects")

            # Deserialize the main save
            x = self.deserialize(b, sd, {})

            # Create the output object
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

    # A recursive function to which you supply a data object
    # For that a layer is supplied, so the function can build the object layer by layer without needing a global object
    # The serializer is the extracted string data
    def deserialize(self, stream, serializer, layer):

        # Information how many objects are stored in this dataset
        n = stream.read("int32")

        if n == -1:
            return
        # print(num)
        # print("Following things are Serialized")

        # Iterate the stored datasets / objects
        for i in range(n):
            # Extract the hash of the object, this is equal to the property name of the object (f.e. toplevel this would
            # be something like the property Inventory of the object GameSave
            hash = str(stream.read("int32"))
            # Create a copy of the hash
            nam = hash

            # If we have a string for the hash we assign this string to nam
            if hash in self.hashes.hash_to_name:
                nam = self.hashes.hash_to_name[hash]
            # print("Hash: " + str(nam))
            #     pass

            # In the current layer we create a property with either the hash or the string as key
            layer[nam] = dict()
            # print("Deserialized Object:")

            # After extracting the information about the current object we now extract it's data
            x = self.deserializedata(stream, serializer, layer[nam], hash)

            layer[nam] = x
        return layer

    # Deserialize 1 object / value / list / ....
    def deserializedata(self, stream, serializer, layer, hash):

        # We extract a Byte which determines which type of object we have
        curtype = stream.read("uint8")

        # We assign the type to the hash to be able get the data type just from the hash (in the encoding function)
        self.hashes.hash_to_type[hash] = curtype
        # print("Datatype: " + str(curtype))

        # Depending on the Type we extract the data in different ways
        if curtype == Types.SmartSerialized:
            # As child we have again an object
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
            return {"x": stream.read("float"), "y": stream.read("float"), "type": "Vector2"}
        elif curtype == Types.Vector2_00:
            return {"x": 0, "y": 0, "type": "Vector2"}
        elif curtype == Types.Vector2_11:
            return {"x": 1, "y": 1, "type": "Vector2"}
        elif curtype == Types.Vector3:
            return {"x": stream.read("float"), "y": stream.read("float"), "z": stream.read("float"), "type": "Vector3"}
        elif curtype == Types.Vector3_000:
            return {"x": 0, "y": 0, "z": 0, "type": "Vector3"}
        elif curtype == Types.Vector3_111:
            return {"x": 1, "y": 1, "z": 1, "type": "Vector3"}
        elif curtype == Types.Quaternion:
            return {"x" :stream.read("float"), "y": stream.read("float"), "z": stream.read("float"), "n": stream.read("float"), "type": "Quaternion"}
        elif curtype == Types.Quaternion_0001:
            return {"x": 0, "y": 0, "z": 0, "n": 1, "type": "Quaternion"}
        elif curtype == Types.ByteArray:
            # Length of the saved array
            amount = stream.read("int32")
            arr = []
            for i in range(amount):
                arr.append((stream.read("uint8")).to_bytes(1, byteorder="little"))
            return {"v": arr, "type": curtype}
        elif curtype == Types.GenericList:
            # Length of the saved array
            amount = stream.read("int32")
            arr = []
            for i in range(amount):
                # Iterate and extract the data of an array
                arr.append(self.deserializedata(stream, serializer, {}, hash))

            return {"v": arr, "type": curtype}
        elif curtype == Types.Array:
            # Length of the saved array
            amount = stream.read("int32")
            arr = []
            for i in range(amount):
                # Iterate and extract the data of an array
                arr.append(self.deserializedata(stream, serializer, {}, hash))

            return {"v": arr, "type": curtype}
        # If it is an unknown data type
        else:
            print("Datatype: " + str(curtype) + " can not be parsed")

    # Extract the array of strings which is at the end of the save file
    def extractserializer(self, stream):
        # The position in bytes of the serialized string array
        pos = stream.read("int64")
        # our current position in the bytes
        pos2 = stream.file.tell()
        # print(pos2)
        # We go to the position in the file stream where the strings are stored
        stream.file.seek(pos)
        # we read how many strings are stored
        n = stream.read("int32")
        data = []
        # print(n)

        # We extract every string and push it into our serializer array
        for i in range(n):
            data.append(self.extractstring(stream, True))

        # We return to our start position (because after this function the object data will be read)
        stream.file.seek(pos2)
        return data

    # Function to extract a single string
    def extractstring(self, stream, encrypt=False):

        # We extract the length of the string (in Characters, not Bytes, but some Characters have multiple Bytes thats
        # why we have the prefix and postfix functions)
        n = stream.read("int32")
        # print(n)
        if(n == -1):
            return None

        buffer = []
        out = ""
        # store where the string starts in the file stream
        beginning = stream.file.tell()
        # Create a buffer of bytes in the length of the string
        for i in range(n):
            # buffer.append(int.from_bytes(stream.read("char"), byteorder="little"))
            buffer.append(stream.read("int8"))


        # We now add buffers and the length of the read to a special object should specific unicode values be detected,
        # so we can save the original buffer when encoding again
        specialread = prefix(buffer, stream, beginning, len(buffer))

        # print(num4)
        # in the case of the string being encrypted (which is the case in the string array at the end of the save file)
        if encrypt:
            for i in range(len(buffer)):
                num5 = buffer[i]
                # Replace the numerical buffer value with the character
                if num5 <= 255 and num5 is not 0 and num5 is not 109:
                    buffer[i] = chr(abs(num5 ^ 0x6D))
                else:
                    buffer[i] = chr(abs(num5))
        else:
            for i in range(len(buffer)):
                # Replace the numerical buffer value with the character
                buffer[i] = chr(abs(buffer[i]))

        # We combine every char we extracted to our output string
        out = ''.join(buffer)

        # Fixing our output string
        out = postfix(out, stream, buffer)

        # In the case of a unicode read we return a special object, otherwise we return just the string
        if type(specialread) == dict:
            out = {"string": out, "length": specialread["length"], "buffer": specialread["buffer"]}

        #print(out)

        return out
