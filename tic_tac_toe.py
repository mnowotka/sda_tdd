import random
from typing import List, Tuple, Optional


class Board:

    def __init__(self, rows: int, cols: int) -> None:
        self._fields = None
        self.rows = rows
        self.cols = cols
        self.clear_board()

    def get_field(self, row: int, column: int) -> Optional[str]:
        return self._fields[row][column]

    def set_field(self, value: Optional[str], row: int, column: int) -> None:
        self._fields[row][column] = value

    def __str__(self) -> str:
        return '\n'.join(['|'.join([y or ' ' for y in x]) for x in self._fields])

    def clear_board(self) -> None:
        self._fields = []
        for row in range(self.rows):
            row = [None] * self.cols
            self._fields.append(row)


def find_free_fields(board: Board) -> List[Tuple[int, int]]:
    free_fields = []
    for row in range(board.rows):
        for col in range(board.cols):
            if not board.get_field(row, col):
                free_fields.append((row, col))
    return free_fields


class Player:
    def __init__(self, mark: str, board: Board) -> None:
        self._mark = mark
        self._board = board

    def play(self) -> None:
        free_fields = self._find_free_fields()
        random_free_row, random_free_column = random.choice(free_fields)
        self._board.set_field(self._mark, random_free_row, random_free_column)

    def _find_free_fields(self) -> List[Tuple[int, int]]:
        return find_free_fields(self._board)


class RealPlayer(Player):

    def play(self) -> None:
        user_row, user_col = None, None
        free_fields = self._find_free_fields()
        while user_row not in {0, 1, 2} or user_col not in {0, 1, 2} or (user_row, user_col) not in free_fields:
            coordinates = input(f'Where should I place {self._mark}? In "row col" format: ')
            try:
                user_row, user_col = [int(x) - 1 for x in coordinates.strip().split()]
            except:
                print("Incorrect format, please use two numbers, separated by space.")
        if user_row is not None and user_col is not None:
            self._board.set_field(self._mark, user_row, user_col)


class TicTacToeGame:
    def __init__(self, board, players) -> None:
        self._board = board
        self._players = players

    def play(self) -> None:
        turn = 0
        while True:
            print(self._board)
            print("\n")
            active_player = self._players[turn % 2]
            active_player.play()
            turn += 1
            finished, winner = self._check_game_state()
            if finished:
                break
        print(self._board)
        print("\n")
        print(f"The winner is {winner}")

    def _check_game_state(self) -> Tuple[bool, Optional[str]]:
        for row in range(3):
            actual_row = [self._board.get_field(row, x) for x in range(3)]
            if len(set(actual_row)) == 1 and actual_row[0]:
                return True, actual_row[0]
        for column in range(3):
            actual_column = [self._board.get_field(x, column) for x in range(3)]
            if len(set(actual_column)) == 1 and actual_column[0]:
                return True, actual_column[0]
        diagonal = [self._board.get_field(x, x) for x in range(3)]
        if len(set(diagonal)) == 1 and diagonal[0]:
            return True, diagonal[0]
        diagonal_2 = [self._board.get_field(x, 2 - x) for x in range(3)]
        if len(set(diagonal_2)) == 1 and diagonal_2[0]:
            return True, diagonal_2[0]
        if not find_free_fields(self._board):
            return True, None
        return False, None


if __name__ == '__main__':
    my_board = Board(3, 3)
    my_players = (RealPlayer('X', my_board), Player('O', my_board))
    TicTacToeGame(my_board, my_players).play()


