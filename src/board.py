from itertools import cycle


class Board:
    def __init__(self):
        self.board = (
            [Store()]
            + [House() for _ in range(6)]
            + [Store()]
            # for both players p, p.houses[0] is their leftmost house, so
            # the following array needs to be reversed when printing the board
            # to the screen
            + [House() for _ in range(6)]
        )

    def __iter__(self):
        return enumerate(self.board)

    def __len__(self):
        return len(self.board)

    def __getitem__(self, index):
        return self.board[index]

    def get_opposite_house(self, position):
        return len(self.board) - position

    def __str__(self):
        lines = [
            "   {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}".format(
                *[house.count for house in self.board[:-7:-1]]
            ),
            "{:>2}                   {:>2}".format(
                self.board[0].count, self.board[7].count
            ),
            "   {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}".format(
                *[house.count for house in self.board[1:7]]
            ),
        ]
        return "\n".join(lines)


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
