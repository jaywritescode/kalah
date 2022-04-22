from enum import Enum, auto
from itertools import cycle

from more_itertools import spy
from src.board import Board

from src.players import KeyboardInterfacePlayer, RandomChoicePlayer


class Kalah:
    def __init__(
        self, player1_class=KeyboardInterfacePlayer, player2_class=RandomChoicePlayer
    ):
        self.board = Board()
        self.player1 = player1_class.create(
            self.board[1:7], self.board[7], name="Me"
        )
        self.player2 = player2_class.create(self.board[-6:], self.board[0])

        self.players = cycle([self.player1, self.player2])
        self.outcome = None

    def play(self):
        while self.outcome is None:
            print(self.board)
            self.next()

    def next(self):
        current_player = next(self.players)
        if self.is_game_over():
            self.game_over()
            return self.outcome

        move = current_player.get_move()
        while move.apply(self.board):
            move = current_player.get_move()

    def is_game_over(self):
        return any(
            all(house.count == 0 for house in p.houses)
            for p in [self.player1, self.player2]
        )

    def game_over(self):
        for player in [self.player1, self.player2]:
            for house in player.houses:
                player.store.seed_sown(house.take_all())

        match self.player1.score - self.player2.score:
            case x if x > 0:
                self.outcome = Outcome.PLAYER_ONE_WINS
            case x if x < 0:
                self.outcome = Outcome.PLAYER_TWO_WINS
            case _:
                self.outcome = Outcome.TIE

    def __repr__(self):
        pieces = [str(self.board)]
        if self.outcome is not None:
            pieces.append(f"outcome: {str(self.outcome)}")
        else:
            (next_player, self.players) = spy(self.players)
            pieces.append(f"current player: {str(next_player)}")
        return "\n".join(pieces)


class Outcome(Enum):
    PLAYER_ONE_WINS = auto()
    PLAYER_TWO_WINS = auto()
    TIE = auto()


# class MinimaxPlayer(AbstractPlayer):
#     def __init__(self):
#         super().__init__("Computer")

#     def get_move(self):
#         raise NotImplemented


if __name__ == "__main__":
    k = Kalah()
    k.play()
