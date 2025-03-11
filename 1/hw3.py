"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"

Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"

    [[-, -, o],
     [-, o, o],
     [x, x, x]]

     Return value should be "x wins!"

"""

from typing import List
import unittest


def tic_tac_toe_checker(board: List[List]) -> str:
    if check(board, "x"):
        return "x wins!"
    elif check(board, "o"):
        return "o wins!"
    else:
        for row in board:
            if "-" in row:
                return "unfinished!"
        return "draw!"


def check(b, char):
    # Строки
    for row in b:
        if all(cell == char for cell in row):
            return True
    # Столбцы
    for col in range(3):
        if all(b[row][col] == char for row in range(3)):
            return True
    # Диагонали
    if all(b[i][i] == char for i in range(3)):
        return True
    if all(b[i][2 - i] == char for i in range(3)):
        return True
    return False


class TestTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_unfinished(self):
        self.assertEqual(
            tic_tac_toe_checker([["-", "-", "o"], ["-", "x", "o"], ["x", "o", "x"]]),
            "unfinished!",
        )

    def test_x_wins(self):
        self.assertEqual(
            tic_tac_toe_checker([["-", "-", "o"], ["-", "o", "o"], ["x", "x", "x"]]),
            "x wins!",
        )


if __name__ == "__main__":
    unittest.main()
