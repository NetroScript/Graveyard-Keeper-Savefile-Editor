from enum import IntEnum
from json import load


# The possible serialisation types the game uses and their binary value (as int)
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
with open("./data/locals.json", encoding="utf8") as f:
    id_to_name = load(f)

# Generic game information
with open("./data/html/items.json") as f:
    gamedata = load(f)

with open("./data/data.json") as f:
    jsongamedata = load(f)

# A example item in the case of the inventory being empty and people wanting to add items to it
fallback_item = {
    "type": 250,
    "v": {
        "value": {
            "type": 3,
            "v": 6
        },
        "linked_id": {
            "type": 3,
            "v": -1
        },
        "self_chance": {
            "type": 250,
            "v": {
                "_simpified_float": {
                    "type": 18,
                    "v": 0
                },
                "_simplified": {
                    "type": 2,
                    "v": False
                },
                "_expression": {
                    "type": 11,
                    "v": ""
                },
                "default_value": {
                    "type": 18,
                    "v": 0
                }
            }
        },
        "15320842": {
            "type": 100,
            "v": []
        },
        "equipped_as": {
            "type": 250,
            "v": {
                "1826761547": {
                    "type": 16,
                    "v": 0
                }
            }
        },
        "_params": {
            "type": 250,
            "v": {
                "_hp": {
                    "type": 18,
                    "v": 0
                },
                "_progress": {
                    "type": 18,
                    "v": 0
                },
                "_durability": {
                    "type": 19,
                    "v": 1
                },
                "_res_v": {
                    "type": 100,
                    "v": []
                },
                "_money": {
                    "type": 18,
                    "v": 0
                },
                "_res_type": {
                    "type": 100,
                    "v": []
                }
            }
        },
        "chance_group": {
            "type": 3,
            "v": -1
        },
        "sub_name": {
            "type": 11,
            "v": ""
        },
        "is_unique": {
            "type": 2,
            "v": False
        },
        "max_value": {
            "type": 0,
            "v": None
        },
        "id": {
            "type": 10,
            "v": "wooden_plank"
        },
        "min_value": {
            "type": 0,
            "v": None
        },
        "common_chance": {
            "type": 250,
            "v": {
                "_simpified_float": {
                    "type": 18,
                    "v": 0
                },
                "_simplified": {
                    "type": 2,
                    "v": False
                },
                "_expression": {
                    "type": 11,
                    "v": ""
                },
                "default_value": {
                    "type": 18,
                    "v": 0
                }
            }
        },
        "multiquality_items": {
            "type": 100,
            "v": []
        },
        "_serialize_depth": {
            "type": 16,
            "v": 0
        },
        "1068875674": {
            "type": 11,
            "v": ""
        }
    }
}
