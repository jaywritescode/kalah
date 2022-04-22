from unittest import mock
from assertpy import assert_that
from more_itertools import consume
import pytest

from src.kalah import Kalah, Outcome
from src.move import Move


@pytest.fixture
def initial_state():
    return Kalah()


@pytest.fixture
def after_one_ply():
    """
    The board after 1. c, b ...
    """
    k = Kalah()
    for idx, value in enumerate([4, 0, 1, 6, 6, 6]):
        k.player1.houses[idx].count = value
        k.player1.store.count = 1
    consume(k.players, n=1)
    return k


@pytest.fixture
def after_six_plies():
    """
    The board after 1. c, f c 2. e a, d 3. f, d a
    """
    k = Kalah()
    for (seedable, count) in zip(k.board, [3, 6, 5, 1, 0, 1, 1, 5, 1, 8, 3, 0, 7, 7]):
        seedable.count = count
    consume(k.players, 6)
    return k


@pytest.fixture
def after_seven_plies():
    """
    The board after 1. d a 2. a c 3. e c 4. c ...
    If player two plays at a, they will end in an empty house.
    """
    k = Kalah()
    for (seedable, count) in zip(k.board, [1, 1, 5, 0, 2, 1, 7, 3, 2, 6, 0, 8, 6, 6]):
        seedable.count = count
    consume(k.players, 7)
    return k


@pytest.fixture
def after_nine_plies():
    """
    The board after 1. e e 2. c, b, f d 3. c b 4. b a, b 5. d ...
    """
    k = Kalah()
    for (seedable, count) in zip(k.board, [4, 7, 0, 0, 0, 3, 1, 7, 1, 1, 9, 2, 4, 9]):
        seedable.count = count
    consume(k.players, 9)
    return k


@pytest.fixture
def full_game():
    """
    The board after 1. a f 2. f b, a 3. b c 4. f, c b 5. f, a f 6. a c
    7. b d 8. e e 9. d a 10. e, c c 11. b e 12. d f #
    Player two has only one move available: f. After playing at f, all of
    player two's houses are empty and the game is over.
    """
    k = Kalah()
    for (seedable, count) in zip(k.board, [9, 3, 1, 1, 1, 0, 4, 29, 0, 0, 0, 0, 0, 0]):
        seedable.count = count
    consume(k.players, 23)
    return k


def test_it_plays_one_seed_in_the_next_n_houses(initial_state):
    kalah = initial_state
    player = kalah.player1

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[0])
    )

    kalah.next()
    assert_game(kalah, [0, 0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4])


def test_it_plays_seeds_in_the_opponents_houses(initial_state):
    kalah = initial_state
    player = kalah.player1

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[5])
    )

    kalah.next()
    assert_game(kalah, [0, 4, 4, 4, 4, 4, 0, 1, 5, 5, 5, 4, 4, 4])


def test_it_ends_in_the_players_store(initial_state):
    kalah = initial_state
    player = kalah.player1

    player.get_move = mock.MagicMock(
        name="get_move", side_effect=[Move(player, player.houses[x]) for x in [2, 4]]
    )

    kalah.next()
    assert_game(kalah, [0, 4, 4, 0, 5, 0, 6, 2, 5, 5, 5, 4, 4, 4])


def test_player_two_can_move(after_one_ply):
    kalah = after_one_ply
    player = kalah.player2

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[4])
    )

    kalah.next()
    assert_game(kalah, [1, 5, 1, 1, 6, 6, 6, 1, 4, 4, 4, 4, 0, 5])


def test_player_one_ends_in_their_own_empty_house(after_six_plies):
    kalah = after_six_plies
    player = kalah.player1

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[2])
    )

    kalah.next()
    assert_game(kalah, [3, 6, 5, 0, 0, 1, 1, 9, 1, 8, 0, 0, 7, 7])


def test_player_two_ends_in_their_own_empty_house(after_seven_plies):
    kalah = after_seven_plies
    player = kalah.player2

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[0])
    )

    kalah.next()
    assert_game(kalah, [4, 1, 5, 0, 0, 1, 7, 3, 0, 7, 0, 8, 6, 6])


def test_player_sows_around_the_entire_board(after_nine_plies):
    kalah = after_nine_plies
    player = kalah.player2

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[5])
    )

    kalah.next()
    assert_game(kalah, [5, 8, 1, 1, 1, 4, 2, 7, 2, 2, 9, 2, 4, 0])


def test_game_over(full_game):
    kalah = full_game
    player = kalah.player2

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[5])
    )

    kalah.next()
    assert_game(kalah, [9, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0])
    assert_that(kalah.outcome).is_equal_to(Outcome.PLAYER_ONE_WINS)


def assert_game(game, board):
    assert_that([house.count for house in iter(game.board)]).is_equal_to(board)
