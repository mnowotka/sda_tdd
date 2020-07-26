import random


class BattleField:
    def __init__(self):
        self._fields = None
        self.clear_battlefield()

    def __str__(self):
        return '\n'.join(['|'.join([y or ' ' for y in x]) for x in self._fields])

    def clear_battlefield(self):
        self._fields = [["00", "A", "B", "C", "D", "E", "F", "G", "H", "i", "J"],
                        ["01", None, None, None, None, None, None, None, None, None, None],
                        ["02", None, None, None, None, None, None, None, None, None, None],
                        ["03", None, None, None, None, None, None, None, None, None, None],
                        ["04", None, None, None, None, None, None, None, None, None, None],
                        ["05", None, None, None, None, None, None, None, None, None, None],
                        ["06", None, None, None, None, None, None, None, None, None, None],
                        ["07", None, None, None, None, None, None, None, None, None, None],
                        ["08", None, None, None, None, None, None, None, None, None, None],
                        ["09", None, None, None, None, None, None, None, None, None, None],
                        ["10", None, None, None, None, None, None, None, None, None, None]]

    def get_field(self, row, column):
        return self._fields[row][column]

    def set_field(self, value, row, column):
        self._fields[row][column] = value


def find_free_field(board):
    free_field = []
    for row in range(1, 11):
        for column in range(1, 11):
            if not board.get_field(row, column):
                free_field.append((row, column))
    return free_field


class Ships:
    def __init__(self, ship):
        # (1*4 , 2*3, 3*2, 4*1)
        self._ship = ship


class Player:
    def __init__(self, mark, board):
        self._mark = mark
        self._board = board

    def play(self):
        free_field = self._find_free_field()
        random_free_row, random_free_column = random.choice(free_field)
        self._board.set_field(self._mark, random_free_row, random_free_column)

    def _find_free_field(self):
        return find_free_field(self._board)


class BattleShipsGame:
    def __init__(self):
        self._board = BattleField()
        self._board2 = BattleField()
        self._players = (Player("+", self._board), Player("+", self._board))
