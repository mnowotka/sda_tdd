import random
class Board:
    def __init__(self):
        self.board = [[" ", " ", " "] for _ in range(3)]
    def __str__(self):
        result = ""
        for row in range(3):
            result += ("|".join(self.board[row])) + "\n"
            if row != 2:
                result += ("-" * 5) + "\n"
        return result
    def __getitem__(self, item):
        return self.board[item[0]][item[1]]
    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value
    def is_it_the_end(self):
        for row in self.board:
            if len(set(row)) == 1 and row[0] != " ":
                return row[0]
        for i in range(3):
            column = [row[i] for row in self.board]
            if len(set(column)) == 1 and column[0] != " ":
                return column[0]
        left_cross = [self.board[i][i] for i in range(3)]
        if len(set(left_cross)) == 1 and left_cross[0] != " ":
            return left_cross[0]
        right_cross = [self.board[i][2-i] for i in range(3)]
        if len(set(right_cross)) == 1 and right_cross[0] != " ":
            return right_cross[0]
        empty_place = False
        for row in self.board:
            if " " in row:
                empty_place = True
                break
        if not empty_place:
            return "It's a tie"
        return False
class Player:
    def __init__(self, turns):
        self.turns = turns
        self.sign = "O" if turns == 0 else "X"
    def find_empty_spot(self, board):
        row = random.randrange(3)
        column = random.randrange(3)
        while board[row, column] != " ":
            row = random.randrange(3)
            column = random.randrange(3)
        return row, column
class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.players = [Player(0), Player(1)]
    def play(self):
        while True:
            player = self.players[self.turn % 2]
            row, column = player.find_empty_spot(self.board)
            self.board[row, column] = player.sign
            print(self.board)
            winner = self.board.is_it_the_end()
            if winner:
                break
            self.turn += 1
        print(winner)
if __name__ == "__main__":
    game = Game()
    game.play()