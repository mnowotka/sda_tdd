import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value_of_card(self):
        rank_value = ([str(n) for n in range(2, 11)] + list('JOKA')).index(self.rank)
        suit_value = ["♠️", "♦️", "♣️", "❤️"].index(self.suit)
        return rank_value, suit_value

    def __lt__(self, other):
        print("calling lt!!")
        print(f"other is {other}")
        return self.value_of_card() < other.value_of_card()

    def __eq__(self, other):


    def __str__(self):
        return f"Card({self.rank}, {self.suit})"


class JapaneseCard(Card):

    def __lt__(self, other):
        return self.value_of_card() > other.value_of_card()


`class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JOKA')
    suits = "♠️ ♦️ ♣️ ❤️".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks
                       for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]

    def __setitem__(self, key, value):
        self._cards[key] = value`


class Player:
    def __init__(self, cards):
        self._hand = cards

    def play(self):
        return self._hand.pop() if self._hand else None


class WarGame:
    def __init__(self, no_of_players):
        self.no_of_players = no_of_players
        self._score = [0] * no_of_players
        hands = self._deal_hands()
        self._players = [Player(hand) for hand in hands]

    def _deal_hands(self):
        hands = [list() for _ in range(self.no_of_players)]
        deck = FrenchDeck()
        random.shuffle(deck)
        for idx, card in enumerate(deck):
            hands[idx % self.no_of_players].append(card)
        return hands

    def _compare_cards(self, cards):
        return max([(idx, card) for idx, card in enumerate(cards)], key=lambda x: x[1])

    def play(self):
        turn = 1
        while True:
            print(f"Turn {turn}:")
            cards = [player.play() for player in self._players]
            if not all(cards):
                print("No more cards, game has ended")
                break
            print("Players played the following cards:")
            for idx, card in enumerate(cards):
                print(f"Player {idx} played {card}")
            winner, winning_card = self._compare_cards(cards)
            print(f"This turn won player {winner} with card {winning_card}")
            self._score[winner] += 1
            turn += 1

        ultimate_winner, winning_score = max([(idx, score) for idx, score in enumerate(self._score)], key=lambda x: x[1])
        print(f"The winner is Player number {ultimate_winner} with the score {winning_score}")


if __name__ == '__main__':
    my_game = WarGame(4)
    my_game.play()

