from typing import TypeAlias, Tuple, Literal, cast
from utils import SlotValue, flatten_list

BoardState: TypeAlias = list[list[SlotValue]]


def gen_empty_board_state() -> BoardState:
    """Generate an empty board state"""
    board_state = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(SlotValue.EMPTY)
        board_state.append(row)
    return board_state


class Board:
    def __init__(self, initial_data: BoardState):
        self.state = initial_data
        self.is_filled = False
        self.got_a_match = False
        self.slots = {
            "ar": (0, 0),
            "as": (0, 1),
            "at": (0, 2),
            "br": (1, 0),
            "bs": (1, 1),
            "bt": (1, 2),
            "cr": (2, 0),
            "cs": (2, 1),
            "ct": (2, 2),
        }

    def slot_val_from_coords(self, coords: Tuple[int, int]) -> SlotValue:
        """Get a slot's value from its coordinates"""
        i, j = coords
        return self.state[i][j]

    def slot_val_from_name(self, slot_name: str) -> SlotValue:
        """Get a slot's value from its name"""
        # get coords from name
        coords = self.slots[slot_name]
        return self.slot_val_from_coords(coords)  # get value from coords

    def __str__(self):
        """Empty column -- ""  -- -1
        Player 1 piece  -- "o" -- 0
        Player 2 piece  -- "x" -- 1
        """
        return f"""       r   s   t

a    | {self.state[0][0]} | {self.state[0][1]} | {self.state[0][2]} |
b    | {self.state[1][0]} | {self.state[1][1]} | {self.state[1][2]} |
c    | {self.state[2][0]} | {self.state[2][1]} | {self.state[2][2]} |

move syntax: <row><col> e.g ar"""

    def validate_slot(self, user_input: str) -> str | Tuple[int, int]:
        """Check that user_input corresponds to a slot on the board. If it does, you return the
        coordinates of the slot, otherwise, you return an error message
        """
        # check that user_input represents a slot position
        if not user_input in self.slots:
            return f"'{user_input}' is not a valid move. Try again"
        # check if the slot has already been played
        i, j = self.slots[user_input]
        if self.state[i][j] != SlotValue.EMPTY:
            return f"slot '{user_input}' has already been played, choose another one"
        return i, j

    def check_slot_already_played(self, slot_name: str) -> bool:
        """Checks whether the slot represented by "slot" has already been played or not"""
        return True if self.slot_val_from_name(slot_name) != SlotValue.EMPTY else False

    def update(self, slot_coord: Tuple[int, int], slot_value: SlotValue):
        """Updates the board state to reflect the move made by the player."""
        i, j = slot_coord
        self.state[i][j] = slot_value

        # after updating the state of the board with a player's move, you have to
        # 1. check to see if there is any match on the board,
        if self.check_win_conditions() == False:
            # 2. if there is no match, check whether the board is filled
            # if so, set the board.is_filled to true
            slots = []
            slots = flatten_list(self.state, slots)
            for slot in slots:
                if slot == SlotValue.EMPTY:
                    self.is_filled = False
                    break
            else:
                self.is_filled = True

    def check_win_conditions(self):
        """There are 8 possible comparisons to find a match and therefore a winner"""
        res = self.comp_coords("ar", "as", "at")  # "ar", "as" and "at"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("br", "bs", "bt")  # "br", "bs" and "bt"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("cr", "cs", "ct")  # "cr", "cs" and "ct"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("ar", "br", "cr")  # "ar", "br" and "cr"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("as", "bs", "cs")  # "as", "bs" and "cs"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("at", "bt", "ct")  # "at", "bt" and "ct"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("ar", "bs", "ct")  # "ar", "bs" and "ct"
        if res != False:
            self.got_a_match = res
            return res

        res = self.comp_coords("at", "bs", "cr")  # "at", "bs" and "cr"
        if res != False:
            self.got_a_match = res
            return res

        return False

    def comp_coords(
        self, *slot_names
    ) -> Literal[False] | Tuple[Literal[True], SlotValue]:
        """Given a list of slot names, get their corresponding values and compare to see if they all have the same value."""
        prev, curr = None, None
        for (
            slot_name
        ) in slot_names:  # e.g i = "ar" , i_coords = (0, 0) , i_val = SlotValue.EMPTY
            slot_value = self.slot_val_from_name(slot_name)
            if prev == None:
                prev = slot_value
                continue
            curr = slot_value

            # empty slots should be considered unequal even though they technically are equal
            if curr == SlotValue.EMPTY or prev == SlotValue.EMPTY or curr != prev:
                return False
            prev = curr
        # they're all the same value, so return True, and the value of the slot
        return True, cast(SlotValue, curr)

    def display(self):
        """Draw the board in it's current state, to the terminal"""
        print(self)
