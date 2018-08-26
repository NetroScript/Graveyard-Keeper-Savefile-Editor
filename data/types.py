from enum import IntEnum
from json import load


class Types(IntEnum):
    NullValue = 0,
    Bool_True = 1,
    Bool_False = 2,
    Int32 = 3,
    Int64 = 4,
    Single = 5,
    Double = 6,
    Byte = 7,
    Char = 8,
    String = 9,
    String_Indexed = 10,
    String_Empty = 11,
    Json = 12,
    Vector2 = 13,
    Vector3 = 14,
    Quaternion = 15,
    Int32_0 = 16,
    Int32_1 = 17,
    Single_0 = 18,
    Single_1 = 19,
    Vector2_00 = 20,
    Vector2_11 = 21,
    Vector3_000 = 22,
    Vector3_111 = 23,
    Quaternion_0001 = 24,
    GenericList = 100,
    Array = 101,
    ByteArray = 102,
    SmartSerialized = 250


# The localisation is english and I have to say I don't know if they are all correct and
# they are not complete, considering I mostly was in it for the items and perks and so on
# But still they may contain spoilers considering quite a few dialogues and so on are in
# them so read it at your own risk
with open("./data/locals.json") as f:
    id_to_name = load(f)

with open("./data/html/items.json") as f:
    gamedata = load(f)
