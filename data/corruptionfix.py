# My personal save file from the beginning has an error in the string encoding of the Serializer which is fixed with the following code
# You probably don't need it unless you have the same type of corruption in the savefile
# If you get other errors and know what you are doing, feel free to add a fix for them here

# To update the description from above. It seems the game used unicode characters when saving, I load the characters
# as Ascii (more or less) meaning in the case of a character having more than 1 Byte it throws an error because it will
# be offset (the word length and read bytes). Because it seems there are only specific characters where this happens
# this code is enough as special cases for the characters which are longer than 1 Byte - in the future it is possible
# that more fixes need to be added


# A fix for the direct buffer of the characters
# If a fix was applied we add the original length and buffer so that we can save that information
# before was the bug that we encoded Unicode Characters as Ascii (as single Byte) leading to errors when the game was
# loading the file.
def prefix(buffer, stream, beginning, num):

    length = len(buffer)
    # print(buffer)
    if str(buffer) == "[-48, -95, 2, 109, 11, 2, 31, 25, 77, 2, 11, 77, 11, 12, 4, 25]":
        buffer.append(stream.read("int8"))
        return {"length": length, "buffer": buffer[:]}
    if str(buffer).endswith("-47]"):
        return {"length": length, "buffer": buffer[:] + [stream.read("int8")]}

    if str(buffer).startswith("[45, -47, -127,") or str(buffer).startswith("[-47, -127, 1") or str(buffer).startswith("[0, -47, -127,"):
        buffer.append(stream.read("int8"))
        return {"length": length, "buffer": buffer[:]}

    return False


# Here we fix specific strings which are read as ascii but are unicode leading to missing / wrong / too many characters
# Especially notably: Uppercase C
def postfix(string, stream, buffer):
    if string == "steep_yellow_blockage_0__destructio":
        buffer.append(stream.read("int8"))
        return "steep_yellow_blockage_0__destruction"
    if string == "C4omfort of fait5":
        return "Comfort of faith"
    # for debugging purposes to be able to place a breakpoint in this specific case
    if "D" in string:
        pass
    return string.replace("D", "C")