from src.deck import Deck


# Player Class (Score, Hand, Name, Hand Length)
class Player:
    def __init__(self, player_name):
        self.score = 0
        self.hand = ""
        self.player = player_name
        self.bj = False
        self.hand_length = 1

    def player_hand(self, hand):
        self.hand = hand
        return self.hand
    
    def get_hand_length(self):
        return self.hand_length
    
    def get_player_hand(self):
        return self.hand
    
    def create_player_score(self, hand):
        self.score=0
        for c in self.player_hand(hand):
            # if there is an ace in the hand, add the user's specified value
            if c.value > 0:
                self.score+=c.value
            else:
                self.score += c.card_value()
        return self.score
    
    def player_score(self):
        return int(self.score)
    
    def player_name(self):
        return self.player

class ActiveDeck():
    def __init__(self, active_deck):
        self.deck = active_deck

    def active_deck(self):
        return self.deck

def play(current_players, deck):
    create_player_hands(current_players, deck)

#return list of players
def create_players(players=1, list_of_names=[]):
    player_objects = []

    for player in list_of_names:
        new_player = Player(player)
        player_objects.append(new_player)
    
    return player_objects

def create_player_hands(current_players, deck):
        # for every player, create a new hand and assign it to the player
        for p in current_players:
            # create new hand for the player
            curr_hand = get_hand(deck)

            # Uses the Player class to assign the hand to the player
            p.player_hand(curr_hand)

            # calculate Player's score
            if check_for_blackjack(curr_hand) == True:
                p.score = 21
                p.bj = True
                print(f"{p.player_name()} has BlackJack!")
            
            elif check_for_AA(curr_hand) == True:
                p.score = 12
            elif p.score != 21:
                p.create_player_score(curr_hand)

def get_hand(deck):
    new_hand = []
    for i in range(2):
        card= deck.next_card()
        new_hand.append(card)
    return new_hand

# Function to calculate the player's score after a new card has been drawn.
def calculate_new_score(deck, player):
    new_score = 0
    card = deck.next_card()

    #if card is an ace, ignore for now.
    if card.card_value() == 0:
        pass

    else:
        new_score = player.player_score() + card.card_value()

    if new_score > 21:
        update_score(player, card)
    
    elif new_score == 21:
        update_score(player, card)

    else:
        update_score(player, card)

    return card

# Function takes the old hand and adds the new card, updating the player's score.
def update_score(player, new_card):
    old_hand = player.get_player_hand()
    old_hand.append(new_card)
    player.player_hand(old_hand)
    player.create_player_score(old_hand)

# function if ace is High
def ace_high(player, new_card, rnd_num):
    new_card.value = 11
    old_hand = player.get_player_hand()
    player.player_hand(old_hand)
    player.create_player_score(old_hand)

# function if ace is Low
def ace_low(player, new_card, rnd_num):
    new_card.value = 1
    old_hand = player.get_player_hand()
    player.player_hand(old_hand)
    player.create_player_score(old_hand)

# Function to get user's hit or stick decision.
def hit_or_stick(p, deck):
    while True:
        # input parametres
        hit_or_stick = ["hit", "stick"]

        # main user input - hit or stick
        p_input = input(f"Your current score is: {p.player_score()}.\nDo you wish to 'hit' or 'stick'?\n")

        # logic behind user input
        if p_input in hit_or_stick:
            if p_input == "stick":
                if p.player_score() == 21:
                    p.bj = True
                print(f"final score: {p.player_score()}")

            else:
                calculate_new_score(deck, p)
            break

def hit(p, deck):
    return calculate_new_score(deck, p)

def stick(p, deck):
    if p.player_score() == 21:
        p.bj = True
    print(f"final score: {p.player_score()}")

def evaluate(player):
    if player.score > 21:
        return False
    return True

# Functions to check for exceptions
def check_for_blackjack(hand):
    bj_score = 0

    for c in hand:
        
        if c.name == "A":
            bj_score += 11
        if c.name in ["K", "Q" "J"]:
            bj_score += 10

    if bj_score == 21:
        return True
    else: 
        return False

def check_for_AA(hand):
    x=0
    for c in hand:
        if c.name == "A":
            x += 1
    if x == 2:
        return True
        
if __name__ == '__main__':
    play()