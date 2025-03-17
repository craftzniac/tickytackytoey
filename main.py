from Board import Board, gen_empty_board_state
from typing import cast
from Player import Player
from utils import get_string_input, SlotValue, GameExitCondition


class Game:
    def __init__(self):
        self.board = Board(gen_empty_board_state())
        self.player_o = self.create_player("o")
        self.player_x = self.create_player("x")
        self.winner = None
        self.current_player_turn = self.player_o  # player_o will play first

    def create_player(self, id) -> Player:
        """Get player name from stdin and use that to create new player"""
        slot_value: "o" | "x"
        match id:
            case "o":
                slot_value = SlotValue.PLAYER_O
            case "x":
                slot_value = SlotValue.PLAYER_X
            case _:
                raise Exception("not valid slot value")

        return Player(
            name=get_string_input(prompt=f"Enter player name ({id}): "),
            board=self.board,
            slot_value=slot_value,
        )

    def set_next_player_turn(self):
        if self.current_player_turn is self.player_o:
            self.current_player_turn = self.player_x
        else:
            self.current_player_turn = self.player_o

    def start(self):
        exit_condition: GameExitCondition | None = None
        while True:
            """
            game play is on, so long as there isn't a winner or the board isn't filled up yet
            """
            self.board.display()
            self.current_player_turn.play()
            # break the loop if there's a winner or board is filled
            if self.check_for_winner() == True:
                exit_condition = GameExitCondition.WIN
                break
            if self.board.is_filled == True:
                exit_condition = GameExitCondition.FILLED_BOARD
                break
            self.set_next_player_turn()

        if exit_condition == GameExitCondition.WIN:
            self.board.display()
            print(f"Game over: {self.winner} has won!")
        else:
            self.board.display()
            print("Game Over: It's a Draw!")

    def check_for_winner(self) -> bool:
        res = self.board.got_a_match
        if res != False:  # we have a winner
            # not doing anything with the _coords for now but maybe later?
            _coords, slot_value = res

            # get player from slot value
            match slot_value:
                case SlotValue.PLAYER_O:
                    player = self.player_o
                case SlotValue.PLAYER_X:
                    player = self.player_x
                case _:
                    raise Exception("invalid slot value")

            self.winner = player
            return True
        return False


if __name__ == "__main__":
    game = Game()
    game.start()
