from itertools import cycle

class Board:
    def __init__(self):
        self.board = [Store()] + [House() for _ in range(6)] + [Store()] + [House() for _ in range(6)]

    def __iter__(self):
        return cycle(self.board)

    def __len__(self):
        return len(self.board)

    def __getitem__(self, index):
        return self.board[index]

    def get_opposite_house(self, position):
        return len(self.board) - position


class Seedable:
    def __init__(self, initial_count=0):
        self.count = initial_count


class House(Seedable):
    def __init__(self):
        super().__init__(4)

    def take_all(self):
        seeds = self.count
        self.count = 0
        return seeds

    def seed_sown(self):
        self.count += 1


class Store(Seedable):
    def __init__(self):
        super().__init__()

    def seed_sown(self, amount=1):
        self.count += amount