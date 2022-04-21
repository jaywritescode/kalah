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
def second_move():
    """
    The board after 1. c, b ...
    """
    k = Kalah()
    for idx, value in enumerate([4, 0, 1, 6, 6, 6]):
        k.player1.houses[idx].count = value
        k.player1.store.count = 1
    consume(k.players, n=1)
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


def test_player_two_can_move(second_move):
    kalah = second_move
    player = kalah.player2

    player.get_move = mock.MagicMock(
        name="get_move", return_value=Move(player, player.houses[4])
    )

    kalah.next()
    assert_game(kalah, [1, 5, 1, 1, 6, 6, 6, 1, 4, 4, 4, 4, 0, 5])


def assert_game(game, board):
    assert_that([house.count for _, house in iter(game.board)]).is_equal_to(board)