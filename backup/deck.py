import random

class Deck:
    def __init__(self):
        self.cards = []
        values= ("A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2")
        suits= ("H", "S", "D", "C")

        for value in values:
            for suit in suits:
                card = Card(value, suit)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def next_card(self):
        card = self.cards.pop()
        return card

class Card():
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
    
    # returns the numberical value of the card
    def card_value(self):
        # If card is a number, return the value as an int
        if self.name.isdigit():
            return int(self.name)
        # If card is not a number and is 'A', return false (This is an Ace)
        elif self.name == "A":
            accepted_input = ["h", "l"]

            while True:
                ace = input("Ace high(H) or low(L):").lower()
                if ace in accepted_input:
                    if ace == "h":
                        return 11
                    elif ace == "l":
                        return 1
                    break
        # Otherwise, the card's value is 10.
        else:
            return 10
    
    def card_suit(self):
        return self.suit

    def print_card(self):
        print(f"{self.name}{self.suit}.png")
        return self.name + self.suit + ".png"

