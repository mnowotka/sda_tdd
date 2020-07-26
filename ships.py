import random
from collections import namedtuple

def mark(field):
    if field is None:
        return " "
    if field is False:
        return "X"
    if field == "marked":
        return '-'
    return "O"


def row_repr(row):
    return "|".join([mark(field) for field in row])


Spot = namedtuple('Spot', ['row', 'column', 'horizontal_orientation'])


class Ship:
    def __init__(self, length):
        self.length = length


class See:
    ships_to_locate = [Ship(4), Ship(3), Ship(3), Ship(2), Ship(2), Ship(1), Ship(1)]

    def __init__(self):
        self.fields = [[None for _ in range(10)] for _ in range(10)]

    def __repr__(self):
        line = "\n" + "".join(['-' for _ in range(19)]) + "\n"
        result = ""
        for row in range(10):
            result += "|".join([mark(field) for field in self.fields[row]])
            if row < 9:
                result += line
        return result

    def __getitem__(self, item):
        return self.fields[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.fields[key[0]][key[1]] = value

    def populate(self):
        for ship in self.ships_to_locate:
            free_spots = self.find_spots(ship)
            spot = random.choice(free_spots)
            located_ship = LocatedShip(ship, spot)
            for ship_field in located_ship.fields:
                self.fields[ship_field.row][ship_field.column] = True

    def find_spots(self, ship):
        free_spots = []
        for horizontal in [True, False]:
            for row in range(10):
                for column in range(10):
                    spot = Spot(row, column, horizontal)
                    if self.spot_fits(spot, ship):
                        free_spots.append(spot)
        return free_spots

    def spot_fits(self, spot, ship):
        for i in range(0, ship.length):
            row = spot.row if spot.horizontal_orientation else spot.row + i
            if row > 9:
                return False
            column = spot.column + i if spot.horizontal_orientation else spot.column
            if column > 9:
                return False
        if self.nothing_around(spot, ship):
            return True
        return False

    def nothing_around(self, spot, ship):
        if spot.horizontal_orientation:
            for row_mod in [-1, 0, 1]:
                for column_mod in range(-1, ship.length + 1):
                    row = spot.row + row_mod
                    column = spot.column + column_mod
                    if row < 0 or row > 9:
                        continue
                    if column < 0 or column > 9:
                        continue
                    if self.fields[row][column] is not None:
                        return False
            return True
        else:
            for col_mod in [-1, 0, 1]:
                for row_mod in range(-1, ship.length + 1):
                    row = spot.row + row_mod
                    column = spot.column + col_mod
                    if row < 0 or row > 9:
                        continue
                    if column < 0 or column > 9:
                        continue
                    if self.fields[row][column] is not None:
                        return False
            return True


class OpponentSee(See):
    def __init__(self):
        super().__init__()

    def possible_fields(self):
        result = []
        for i in range(10):
            for j in range(10):
                if self.fields[i][j] is None:
                    result.append((i, j))
        return result


class ShipField:
    def __init__(self, row, column, sunk=False):
        self.row = row
        self.column = column
        self.sunk = sunk


class LocatedShip:
    def __init__(self, ship: Ship, spot):
        self.fields = []
        for i in range(ship.length):
            row = spot.row if spot.horizontal_orientation else spot.row + i
            column = spot.column + i if spot.horizontal_orientation else spot.column
            self.fields.append(ShipField(row, column))


class Player:
    def __init__(self):
        self.my_board = See()
        self.my_board.populate()
        self.opponent_board = OpponentSee()

    def play(self):
        possible_fields = self.opponent_board.possible_fields()
        shot = random.choice(possible_fields)
        return shot


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.turn = 0
        self.current_player = self.players[0]
        self.attacked_player = self.players[1]
        self.game_over = False

    def set_players(self):
        self.current_player = self.players[self.turn % 2]
        self.attacked_player = self.players[(self.turn + 1) % 2]

    def play(self):
        while not self.game_over:
            coordinates = self.current_player.play()
            self.response(coordinates)
        return f"player {self.turn % 2} wins"

    def response(self, coordinates):
        shot = self.attacked_player.my_board[coordinates]
        if shot is None:
            print(f"You missed at coords: {coordinates}")
            self.current_player.opponent_board[coordinates] = "marked"
            print(self.current_player.opponent_board)
            self.turn += 1
            self.set_players()
        elif shot == "marked":
            print("Why you even try this place")
        elif shot is False:
            print("This was already sunken")
        else:
            print(f"You got me at coords: {coordinates}")
            self.current_player.opponent_board[coordinates] = False
            self.attacked_player.my_board[coordinates] = False
            self.game_over = self.is_the_game_over()

    def is_the_game_over(self):
        count = 0
        for i in range(10):
            for j in range(10):
                if self.current_player.opponent_board[(i, j)] == False:
                    count += 1
        if count == 16:
            return True
        return False


if __name__ == "__main__":
    game = Game()
    print(game.play())
