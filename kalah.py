from itertools import cycle
from src.board import Board

from src.players import KeyboardInterfacePlayer, RandomChoicePlayer


class Kalah:
    def __init__(self):
        self.board = Board()
        self.player1 = KeyboardInterfacePlayer("Me", self.board[1:7], self.board[7], 0)
        self.player2 = RandomChoicePlayer(self.board[-6:], self.board[0], 7)

        self.players = cycle([self.player1, self.player2])
        self.outcome = None

    def play(self):
        while self.outcome is None:
            print(self.board)

            self.next()

    def next(self):
        current_player = next(self.players)
        if self.is_game_over(current_player):
            self.game_over()
            return self.outcome

        move = current_player.get_move()
        while move.apply(self.board):
            move = current_player.get_move()

    def is_game_over(self, current_player):
        return all(house == 0 for house in current_player.houses)

    def game_over(self):
        match self.player1.score - self.player2.score:
            case x if x > 0:
                self.outcome = self.player1
            case x if x < 0:
                self.outcome = self.player2
            case _:
                self.outcome = "it's a tie"

# class MinimaxPlayer(AbstractPlayer):
#     def __init__(self):
#         super().__init__("Computer")

#     def get_move(self):
#         raise NotImplemented


if __name__ == "__main__":
    k = Kalah()
    k.play()
