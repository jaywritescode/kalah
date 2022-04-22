from unittest import mock
from assertpy import assert_that
from more_itertools import consume
import pytest

from src.kalah import Kalah
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
    for (seedable, count) in zip(k.board,  [3, 6, 5, 1, 0, 1, 1, 5, 1, 8, 3, 0, 7, 7]):
        seedable.count = count
    consume(k.players, 6)
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

def test_player_two_ends_in_their_own_empty_house():
    pass

def test_player_sows_around_the_entire_board():
    pass


def assert_game(game, board):
    assert_that([house.count for house in iter(game.board)]).is_equal_to(board)
