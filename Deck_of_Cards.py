import random


class Card:
    allowed_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    allowed_values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if self.suit not in Card.allowed_suits:
            raise ValueError(f'Suit not recognized. Should be one of the {Card.allowed_suits}')

        if self.value not in Card.allowed_values:
            raise ValueError(f'Value of the card not recognized. Should be one of the {Card.allowed_suits}')

    def __repr__(self):
        return f'{self.value} of {self.suit}'


class Deck:
    def __init__(self):
        allowed_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        allowed_values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, value) for value in allowed_values for suit in allowed_suits]

    def __repr__(self):
        return f'Deck of {self.count()} cards'

    def count(self):
        return len(self.cards)

    def _deal(self, number):
        card_count = self.count()
        if card_count == 0:
            raise ValueError('All cards have been dealt.')
        dealt_cards = self.cards[-min(card_count, number):]
        del self.cards[-min(card_count, number):]
        return dealt_cards

    def shuffle(self):
        if self.count() != 52:
            raise ValueError('Only full decks can be shuffled')
        return random.shuffle(self.cards)

    def deal_card(self):
        return self._deal(1)[0]

    def deal_hand(self, number):
        return self._deal(number)


my_deck = Deck()
print(my_deck)
my_deck.shuffle()
card = my_deck.deal_card()
print(card)
hand = my_deck.deal_hand(5)
print(hand)
print(my_deck)

