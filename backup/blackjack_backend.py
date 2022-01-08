from src.deck import Deck

# to play black jack you need to hands
# first of all we will get a system working where we get given a hand

class Player:
    def __init__(self, player_name):
        self.score = 0
        self.hand = ""
        self.player = player_name
        self.bj = False

    def player_hand(self, hand):
        self.hand = hand
        return self.hand
    
    def get_player_hand(self):
        return self.hand

    def create_player_score(self, hand):
        self.score=0
        for c in self.player_hand(hand):
                self.score += c.card_value()
        return self.score
    
    def player_score(self):
        return int(self.score)
    
    def player_name(self):
        return self.player

def play():
    num_players = input("Enter Number of Players:")
    if num_players.isnumeric() == False:
        print("Please enter a number between 1 and 7.")
        play()
    
    elif int(num_players) < 7 and int(num_players) > 0:
        current_players = create_players(int(num_players))
        deck = Deck()
        deck.shuffle()
        create_player_hands(current_players, deck)

        # round begins - asking each player if they want to hit until they bust or choose to stick.
        for p in current_players:
            # prints player's hand to console
            print(f"{p.player_name()}\'s hand: {' '.join([''.join([i.name, i.suit]) for i in p.hand])}")
            if p.player_score == 21:
                print(f"{p.player_name()} has 21!")
            elif p.bj == True:
                print(f"{p.player_name()} has BlackJack!")
            else:
                hit_or_stick(p, deck)

        for p in current_players:
            if evaluate(p) == True and p.bj == False:
                print(f"Congratulations {p.player_name()}, your final score was {p.score}.")
            if evaluate(p) == True and p.bj == True:
                print(f"Congratulations {p.player_name()}, you got BlackJack!")
            else:
                print(f"How unfortunate {p.player_name()}, your final score was {p.score}. \nBetter luck next time!")
            
    else:
        print("invalid player number please enter a number between 1 and 7.")
        play()

#return list of players
def create_players(players=1):
    player_list = []
    player_objects = []

    if players == 1:
        player_list.append(input("Enter player's name:"))
    else:
        for i in range(players):
            p_name = input(f"Enter player {i+1}'s name:")
            player_list.append(p_name)

    for player in player_list:
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
            

                # prints player's hand to console
                #print(f"{p.player_name()}\'s hand: {' '.join([''.join([i.name, i.suit]) for i in curr_hand])}")

def get_hand(deck):
    new_hand = []
    for i in range(2):
        card= deck.next_card()
        new_hand.append(card)
    return new_hand

# Function to calculate the player's score after a new card has been drawn.
def calculate_new_score(deck, player):
    card = deck.next_card()
    new_score = player.player_score() + card.card_value()
    print(f"{player.player_name()} gets a {card.name} of {card.suit}")

    if new_score > 21:
        update_score(player, card)
        print(f"{player.player_name()} gets a {card.card_value()} of {card.card_suit()} and BUSTS with a score of {new_score}")
    
    elif new_score == 21:
        update_score(player, card)
        print(f"{player.player_name()} gets a {card.card_value()} of {card.card_suit()} and has 21!")

    else:
        update_score(player, card)
        hit_or_stick(player, deck)

# Function takes the old hand and adds the new card, updating the player's score.
def update_score(player, new_card):
    old_hand = player.get_player_hand()
    old_hand.append(new_card)
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