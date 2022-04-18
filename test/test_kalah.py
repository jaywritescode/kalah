from unittest import mock
from assertpy import assert_that
import pytest

from src.kalah import Kalah
from src.move import Move


@pytest.fixture
def initial_state():
    return Kalah()


def test_it_plays_one_seed_in_the_next_n_houses(kalah):
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


def test_it_plays_seeds_in_the_opponents_houses(kalah):
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


def test_it_ends_in_the_players_store(kalah):
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


def assert_game(game, *, player1_houses, player1_score, player2_houses, player2_score):
    assert_that(game.player1.state._asdict()).has_houses(player1_houses).has_score(
        player1_score
    )
    assert_that(game.player2.state._asdict()).has_houses(player2_houses).has_score(
        player2_score
    )
