import random

from src.move import Move


class AbstractPlayer:
    def __init__(self, name, houses, store, offset):
        self.name = name
        self.houses = houses
        self.store = store
        self.offset = offset

    def get_move(self):
        raise NotImplemented

    @property
    def score(self):
        return self.store.count

    def __repr__(self):
        return self.name


class KeyboardInterfacePlayer(AbstractPlayer):
    def __init__(self, name, houses, store, offset):
        super().__init__(name, houses, store, offset)

    def get_move(self):
        while True:
            i = int(input("Which house (left-most is #1)? "))
            if 0 <= i <= 6 and self.houses[i].count > 0:
                return Move(self, i)


class RandomChoicePlayer(AbstractPlayer):
    def __init__(self, houses, store, offset):
        super().__init__("Computer", houses, store, offset)

    def get_move(self):
        choice = random.choice([idx for (idx, val) in enumerate(self.houses) if val.count > 0])
        return Move(self, choice)