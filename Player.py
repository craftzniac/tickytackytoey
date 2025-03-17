from Board import Board
from utils import get_string_input, SlotValue

class Player:
    def __init__(self, *, name: str, board: Board, slot_value: SlotValue):
        self.name = name
        self.board = board
        self.slot_value =  slot_value

    def play(self):
        """
        when a player makes a move, he/she updates a specific column in the board
        """
        has_played_turn = False

        while has_played_turn == False:
            user_input = get_string_input(prompt=f"{self.name}'s turn({self.slot_value}): ")

            res: str | (int, int) = self.board.validate_slot(user_input)
            if isinstance(res, str):
                print(res)
            else:
                self.board.update(slot_coord=res, slot_value=self.slot_value)
                has_played_turn = True
