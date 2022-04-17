from itertools import islice

from src.board import Store


class Move:
    def __init__(self, player, selection):
        self.player = player
        self.selection = selection

    def apply(self, board):
        """
        Performs the player's move.

        return: True if the same player should go again, otherwise False
        """
        it = islice(enumerate(iter(board)), self.selection, None)
        
        (position, seedable) = next(it)

        while True:
            seeds = seedable.take_all()
            while seeds > 0:
                (position, seedable) = next(it)
                if isinstance(seedable, Store) and seedable is not self.player.store:
                    continue

                seedable.seed_sown()
                seeds -= 1
            
            if seedable is self.player.store:
                return True
            elif seedable in self.player.houses and seedable.count == 1:
                self.store.seed_sown(seedable.take_all())
                self.store.seed_sown(board.get_opposite_house(position).take_all())

            return False