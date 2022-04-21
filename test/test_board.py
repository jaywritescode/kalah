import pytest

from src.kalah import Kalah


def test_the_zeroth_element_is_player_twos_store():
    kalah = Kalah()
    assert kalah.board[0] is kalah.player2.store

def test_the_first_element_is_player_ones_leftmost_house():
    kalah = Kalah()
    assert kalah.board[1] is kalah.player1.houses[0]

def test_the_sixth_element_is_player_ones_rightmost_house():
    kalah = Kalah()
    assert kalah.board[6] is kalah.player1.houses[-1]

def test_the_seventh_element_is_player_ones_store():
    kalah = Kalah()
    assert kalah.board[7] is kalah.player1.store

def test_the_seventh_element_is_player_twos_leftmost_house():   # from their perspective
    kalah = Kalah()
    assert kalah.board[8] is kalah.player2.houses[0]

    