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
    kalah.player1.get_move = mock.MagicMock(
        name="get_move", return_value=Move(kalah.player1, 1)
    )

    kalah.next()
    assert_game(
        kalah,
        player1_houses=[0, 5, 5, 5, 5, 4],
        player1_score=0,
        player2_houses=[4, 4, 4, 4, 4, 4],
        player2_score=0,
    )


def test_it_plays_seeds_in_the_opponents_houses(initial_state):
    kalah = initial_state
    kalah.player1.get_move = mock.MagicMock(
        name="get_move", return_value=Move(kalah.player1, 6)
    )

    kalah.next()
    assert_game(
        kalah,
        player1_houses=[4, 4, 4, 4, 4, 0],
        player1_score=1,
        player2_houses=[5, 5, 5, 4, 4, 4],
        player2_score=0,
    )


def test_it_ends_in_the_players_store(initial_state):
    kalah = initial_state
    kalah.player1.get_move = mock.MagicMock(
        name="get_move", side_effect=[Move(kalah.player1, x) for x in [3, 5]]
    )

    kalah.next()
    assert_game(
        kalah,
        player1_houses=[4, 4, 0, 5, 0, 6],
        player1_score=2,
        player2_houses=[5, 5, 5, 4, 4, 4],
        player2_score=0,
    )


def test_player_two_can_move(second_move):
    kalah = second_move
    kalah.player2.get_move = mock.MagicMock(
        name="get_move", return_value=Move(kalah.player2, 5)
    )

    kalah.next()
    assert_game(
        kalah,
        player1_houses=[5, 1, 1, 6, 6, 6],
        player1_score=1,
        player2_houses=[4, 4, 4, 4, 0, 5],
        player2_score=1
    )

def assert_game(game, *, player1_houses, player1_score, player2_houses, player2_score):
    # TODO: assert that it's the correct player's turn
    assert_that(game.player1.state._asdict()).has_houses(player1_houses).has_score(
        player1_score
    )
    assert_that(game.player2.state._asdict()).has_houses(player2_houses).has_score(
        player2_score
    )
