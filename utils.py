import sys
from enum import Enum

class GameExitCondition(Enum):
    WIN = "win"
    FILLED_BOARD = "fullboard"

def slot_val_to_string(column_state) -> str:
    """Convert SlotValue enum variants to appropriate representation for the board ( , x or o)
    """
    match column_state:
        case SlotValue.EMPTY:
            return " "
        case SlotValue.PLAYER_O: 
            return "o"
        case SlotValue.PLAYER_X:
            return "x"
        case _:
            raise Exception("Invalid slot state")

def flatten_list(items, dest_list):
    """Flatten items. Put all the stuff inside dest_list (destination list)
    """
    for i in items:
        if isinstance(i, list): # check if i is a list
            flatten_list(i, dest_list)
        else:
            dest_list.append(i) 
    return dest_list


def TODO(msg: str):
    sys.exit(f"TODO: {msg}")


def get_string_input(*, prompt: str) -> str:
    """
    get player name from cmdline
    """
    while True:
        name = input(prompt)
        if not name:
            print("invalid input, try again")
        else:
            return name

class SlotValue(Enum):
    EMPTY = -1
    PLAYER_O = 0
    PLAYER_X = 1

    def __str__(self):
        return slot_val_to_string(self)
