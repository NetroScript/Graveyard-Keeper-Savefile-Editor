
# My personal save file from the beginning has an error in the string encoding of the Serializer which is fixed with the following code
# You probably don't need it unless you have the same type of corruption in the savefile
# If you get other errors and know what you are doing, feel free to add a fix for them here


def prefix(buffer, stream, beginning, num):

    # print(buffer)
    if str(buffer) == "[-48, -95, 2, 109, 11, 2, 31, 25, 77, 2, 11, 77, 11, 12, 4, 25]":
        buffer.append(stream.read("int8"))
    if str(buffer).endswith("-47]"):
        stream.file.seek(beginning + num+1)

    if str(buffer).startswith("[45, -47, -127,") or str(buffer).startswith("[-47, -127, 1") or str(buffer).startswith("[0, -47, -127,"):
        buffer.append(stream.read("int8"))
        stream.file.seek(beginning + num+1)


def postfix(string, stream, buffer):
    if string == "steep_yellow_blockage_0__destructio":
        buffer.append(stream.read("int8"))
        return "steep_yellow_blockage_0__destruction"
    return string.replace("D", "C")