import random

class Field:
    def __init__(self):
        self._field = None
        self.clear_field()
    def clear_field(self):
        self._field = [[None, None, None], [None, None, None], [None, None, None]]
        return self._field
    def __str__(self):
        # print('\n'.join(['|'.join([y or ' ' for y in i]) for i in self._field]))
        return '\n'.join(['|'.join([y or ' ' for y in i]) for i in self._field])
    def get_item(self, row, column):
        return self._field[row][column]
    def set_item(self, value,  row, column):
        self._field[row][column] = value
    def check_whos_the_winner(self, player_one_mark, player_name, player_two_mark):
        if self._field[0][0] == self._field[0][1] == self._field[0][2] and self._field[0][0] != None:
            if self._field[0][0] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[0][0] == player_two_mark:
                print("You are looser, hahaha")
                return True
        elif self._field[0][0] == self._field[1][0] == self._field[2][0] and self._field[0][0] != None:
            if self._field[0][0] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[0][0] == player_two_mark:
                print("You are looser, hahaha")
                return True
        elif self._field[0][1] == self._field[1][1] == self._field[2][1] and self._field[0][1] != None:
            if self._field[0][1] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[0][1] == player_two_mark:
                print("You are looser, hahaha")
                return True
        elif self._field[0][2] == self._field[1][2] == self._field[2][2] and self._field[0][2] != None:
            if self._field[0][2] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[0][2] == player_two_mark:
                print("You are looser, hahaha")
                return True
        elif self._field[0][0] == self._field[1][1] == self._field[2][2] and self._field[2][2] != None:
            if self._field[0][0] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[0][0] == player_two_mark:
                print("You are looser, hahaha")
                return True
        elif self._field[1][0] == self._field[1][1] == self._field[1][2] and self._field[2][2] != None:
            if self._field[1][0] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[1][0] == player_two_mark:
                print("You are looser, hahaha")
                return True
        elif self._field[2][0] == self._field[2][1] == self._field[1][2] and self._field[2][2] != None:
            if self._field[2][0] == player_one_mark:
                print(f"The winner is you, {player_name}")
                return True
            elif self._field[2][0] == player_two_mark:
                print("You are looser, hahaha")
                return True
def finding_empty_fields(board):
        empty_list = []
        for i in range(3):
            for j in range(3):
                if not board.get_item(i, j):
                    empty_list.append((i,j))
        return empty_list
class Player:
    def __init__(self, player, mark, board):
        self._player = player
        self._mark = mark
        self._board = board
    def put_value(self,  row, column):
        free_fields = finding_empty_fields(self._board)
        for i in free_fields:
            if i == (row, column):
                    self._board.set_item(self._mark, row, column)
class Player_random:
    def __init__(self, board, mark):
        self._board = board
        self._mark = mark
    def put_value_random(self):
        free_fields = finding_empty_fields(self._board)
        random_row, random_column = random.choice(free_fields)
        self._board.set_item(self._mark, random_row, random_column)

class Play:
    def __init__(self):
        self._board = Field()
        self.player_name = input("Tell me your name: ")
        while True:
            self.player_mark = input("Tell me what you gonna play, 'O' or 'X'?: ")
            if self.player_mark != 'O' and self.player_mark != 'X':
                print("wrong input")
            else:
                break
        if self.player_mark == 'O':
            self.player_mark_random = 'X'
        else:
            self.player_mark_random = 'O'
        self.players = (Player(self.player_name, self.player_mark, self._board)), (Player_random(self._board, self.player_mark_random))
    def play(self):
        turn = 0
        print(self._board)
        while True:
            active_player_one = self.players[0]
            while True:
                player_index_row = int(input("Write your coordinate row: "))
                if player_index_row != 0 and player_index_row != 1 and player_index_row != 2:
                    print("wrong number")
                else:
                    break
            while True:
                player_index_column = int(input("write your column: "))
                if player_index_column != 0 and player_index_column != 1 and player_index_column != 2:
                    print("wrong number")
                else:
                    break
            active_player_one.put_value(player_index_row, player_index_column)
            empty_list = finding_empty_fields(self._board)
            winner = self._board.check_whos_the_winner(self.player_mark, self.player_name, self.player_mark_random)
            if winner == True:
                print(self._board)
                print("End game")
                self._board.clear_field()
                shall_continue = input("Do yuo want to play again? [y]/[n] ")
                if shall_continue.lower() != 'y':
                    break
            if not empty_list:
                print(self._board)
                print("End game")
                self._board.clear_field()
                shall_continue = input("Do yuo want to play again? [y]/[n] ")
                if shall_continue.lower() != 'y':
                    break
            active_player_two = self.players[1]
            active_player_two.put_value_random()
            print(self._board)
            winner = self._board.check_whos_the_winner(self.player_mark, self.player_name, self.player_mark_random)
            if winner == True:
                print(self._board)
                print("End game")
                self._board.clear_field()
                shall_continue = input("Do yuo want to play again? [y]/[n] ")
                if shall_continue.lower() != 'y':
                    break
            turn +=1


if __name__ == '__main__':
    a = Field()
    b = Play()
    b.play()