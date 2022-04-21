from unittest import mock
from assertpy import assert_that
import pytest

from src.kalah import Kalah
from src.players import KeyboardInterfacePlayer


@pytest.mark.parametrize(
    "input_value, expected_index",
    [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5), ("f", 6)],
)
def test_player_one_get_move(input_value, expected_index):
    with mock.patch("src.players.input", create=True) as mock_input:
        kalah = Kalah(player1_class=KeyboardInterfacePlayer)
        mock_input.return_value = input_value

        move = kalah.player1.get_move()
        assert_that(move.selection).is_same_as(kalah.board[expected_index])


@pytest.mark.parametrize(
    "input_value, expected_index",
    [("a", 8), ("b", 9), ("c", 10), ("d", 11), ("e", 12), ("f", 13)],
)
def test_player_two_get_move(input_value, expected_index):
    with mock.patch("src.players.input", create=True) as mock_input:
        kalah = Kalah(player2_class=KeyboardInterfacePlayer)
        mock_input.return_value = input_value

        move = kalah.player2.get_move()
        assert_that(move.selection).is_same_as(kalah.board[expected_index])
