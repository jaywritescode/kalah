from collections import namedtuple
import random

from src.move import Move

PlayerState = namedtuple("PlayerState", ["houses", "score"])


class AbstractPlayer:
    def __init__(self, name, houses, store):
        self.name = name
        self.houses = houses
        self.store = store

    def get_move(self):
        raise NotImplemented

    @property
    def score(self):
        return self.store.count

    @property
    def state(self):
        return PlayerState(houses=[h.count for h in self.houses], score=self.score)

    def __repr__(self):
        return self.name

    @classmethod
    def create(cls, houses, store, **kwargs):
        return cls(houses, store, **kwargs)


class KeyboardInterfacePlayer(AbstractPlayer):
    def __init__(self, houses, store, *, name="Default player"):
        super().__init__(name, houses, store)

    def get_move(self):
        while True:
            i = ord(input("Which house? ")) - ord("a")
            if 0 <= i < 6 and self.houses[i].count > 0:
                return Move(self, self.houses[i])


class RandomChoicePlayer(AbstractPlayer):
    def __init__(self, houses, store):
        super().__init__("Computer", houses, store)

    def get_move(self):
        choice = random.choice([house for house in self.houses if house.count > 0])
        return Move(self, choice)
