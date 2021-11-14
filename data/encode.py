from data.tools import BinaryWriter
from data.types import Types


class Encoder:

    # On Initialisation we need our Hashes object to be able to translate our converted strings back into the numerical
    # values
    def __init__(self):
        self.hashes = {}

    # Encode a file, supply the path to the file and the data of the save here
    def encode(self, file_path, data):
        # The hashes of the save are stored in the data, so we set them here
        self.hashes = data["hashes"]
        # Begin writing to our output file
        with open(file_path, "wb") as fi:
            print("Beginning to encode to: " + file_path)
            # Create a instance of the Binary Writer with the instance of our file
            bw = BinaryWriter(fi)
            bw.write("int64", 0)
            print("Writing header")
            bw.write("int64", data["header"]["offset"])
            bw.write("int32", data["header"]["version"])

            # This is part of the header, I assume the Lazy Bear Games put this in to be able to add more header
            # information at a later points. Currently (Game version 1.034) this information is not filled
            for i in range(15):
                bw.write("int32", 0)
            print("Writing gamedata")
            self.serialize(data["savedata"], bw, data["serializer"])
            print("Writing strings")
            self.insertserializer(bw, data["serializer"])
            print("Finished saving file: " + file_path)

    # A recursive function to turn an object into the binary data in the form of basic values
    def serialize(self, data, stream, serializer):
        if data is None:
            stream.write("int32", -1)
        else:
            # Save how many properties our object has
            stream.write("int32", len(data))
            #print(len(data))
            i = 0

            # Iterate the properties of our object
            for key in data:
                # If we had our string before turn the string back into the numerical hash
                if type(key) is str and key in self.hashes:
                    hash = int(self.hashes[key])
                else:
                    hash = int(key)
                #print(hash)
                # Write the hash to the file
                stream.write("int32", hash)
                # Start writing the contents of the object to the file
                self.serializedata(data[key], stream, serializer, hash)
                i+=1

    # Serialize 1 object / value / list / ....
    def serializedata(self, data, stream, serializer, hash):

        # In the case of our object being a specific object like a Vector we check if the type of object changed
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

            # Otherwise if it is our default notation we just use the type which is stored there
            if "v" in data:
                curtype = data["type"]
                data = data["v"]

        # Now we write the type as Byte to the file
        stream.write("uint8", curtype)
        # Depending on the current type we call the function recursively again or just pass onto the next value
        # (In the case of simple values like Null)
        if curtype == Types.SmartSerialized:
            # Call it again recursively
            self.serialize(data, stream, serializer)
        elif curtype == Types.NullValue:
            pass
        elif curtype == Types.String:
            self.insertstring(data,stream, False)
        elif curtype == Types.String_Empty:
            pass
        elif curtype == Types.String_Indexed:

            # Here we check additionally if all strings which have a type of Indexed String are actually in the string
            # array, if those are not in there, they are added
            try:
                indx = serializer.index(data)
            except ValueError:
                indx = -1

                # Check if the string is encoded as a special object
                for i in range(len(serializer)):
                    if type(serializer[i]) == dict:
                        if data == serializer[i]["string"]:
                            indx = i
                            break

                # If it is not encoded as a special object, add it at the end of the string list
                if indx == -1:
                    indx = len(serializer)
                    serializer.append(data)

            # Save the index of the string within the string array
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
            try:
                stream.write("float", float(data))
            except TypeError:
                stream.write("float", float(0))
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
            # Save the length of our Array to the file
            stream.write("int32", len(data))
            for i in range(len(data)):
                stream.write("uint8", data[i])
        elif curtype == Types.GenericList:
            # Save the length of our Array to the file
            stream.write("int32", len(data))
            # Recursively save every item in the list as new object
            for i in range(len(data)):
                self.serializedata(data[i], stream, serializer, hash)
        elif curtype == Types.Array:
            # Save the length of our Array to the file
            stream.write("int32", len(data))
            # Recursively save every item in the list as new object
            for i in range(len(data)):
                self.serializedata(data[i], stream, serializer, hash)
        # If it is an unknown data type
        else:
            print("Datatype: " + str(curtype) + " can not be parsed")

    # Function to save a string to the file
    def insertstring(self, string, stream, encrypt=False):
        # If the string is non existant write a -1
        if string is None:
            stream.write("int32", -1)
            return

        # If the string was modified while loading (because of Unicode character) we save the original length and byte
        # buffer to the file
        if type(string) == dict:
            stream.write("int32", string["length"])
            for byte in string["buffer"]:
                stream.write("int8", byte)
        else:
            # Otherwise we just save the string length and then write every character as single Byte
            stream.write("int32", len(string))
            for char in string:
                n = ord(char)
                # For the String array at the end of the file we also encode the string
                if encrypt:
                    if n <= 255 and n != 0 and n != 109:
                        n ^= 0x6D
                stream.write("uint8", n)

    # We save our string array at the end of the file
    def insertserializer(self, stream, serializer):
        # The position of the end of the file
        pos = stream.file.tell()
        # Then we go to the beginning and save the position of the current end of the file to be able to read the
        # serialized Strings first
        stream.file.seek(0)
        stream.write("int64", pos)
        # we now go back to the end of the file
        stream.file.seek(pos)
        # Write how many strings are contained in the string array
        stream.write("int32", len(serializer))
        # Save every string encrypted to the file
        for i in range(len(serializer)):
            self.insertstring(serializer[i], stream, True)
