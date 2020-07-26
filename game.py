from random import shuffle
from typing import List


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value_of_card(self):
        rank_value = ([str(n) for n in range(2, 11)] + list('JOKA')).index(self.rank)
        suit_value = ["spades", "diamonds", "clubs", "hearts"].index(self.suit)
        return rank_value + suit_value / 10

    def __lt__(self, other):
        return self.value_of_card() < other.value_of_card()


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JOKA')
    suits = 'spades diamonds clubs hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, item):
        return self._cards[item]
    def __setitem__(self, key, value):
        self._cards[key] = value


class Player:
    def __init__(self, cards):
        self.points = 0
        self.cards: List[Card] = cards
    def __lt__(self, other):
        self.points < other.points

class Game:
    def __init__(self, number_of_players):
        deck = shuffle(FrenchDeck())
        number_of_cards_for_player = 52 // number_of_players
        self.players = [Player(deck[i:i+number_of_cards_for_player]) for i in range(0, 52, number_of_cards_for_player)]
    def one_round(self):
        table = enumerate([player.cards.pop() for player in self.players])
        table = sorted(table, key=lambda x: x[1], reverse=True)
        self.players[table[0][0]].points += 1
    def play(self):
        number_of_rounds = len(self.players[0].cards)
        for _ in range(number_of_rounds):
            self.one_round()
    def show_points(self):
        return [player.points for player in self.players]

if __name__ == '__main__':
    game = Game(3)
    print(game.show_points())
    game.play()
    print(game.show_points())