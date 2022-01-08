from re import L
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
import blackjack_backend as bjack
from src.deck import Deck

# Keeps track of the active deck
class ActiveDeck():
    def __init__(self, active_deck=Deck()):
        self.deck = active_deck

    def get_active_deck(self):
        return self.deck


class BlackJack(FloatLayout):
    # Player specific
    p_name = StringProperty()
    p_score = StringProperty()
    player_hand = StringProperty()
    player_hand_list = ListProperty()
    current_players = ListProperty()
    text_color = (0.0, 1.0, 0.0)
    ace_high_or_low_value = 0
    round_of_betting=0
    
    # Constant for all players
    player_num = 0
    active_deck = ActiveDeck()

    # Function which takes player's name.
    def player_name(self, name=""):
        self.p_name = name
        return self.p_name
    
    # Function which updates the player's score variable within this class.
    def update_score_str(self, score):
        self.p_score = str(score)
        return self.p_score
    
    # Function which gets the player's hand from a list of players (now outdated, only one player can play)
    def get_player_hand(self, deck):
        self.active_deck=deck
        for p in self.current_players:
            self.player_name(p.player)
            self.update_score_str(p.score)
            self.active_player=p
            self.player_hand_list = p.get_player_hand()
            self.update_cards(self.player_hand_list, p)
    
    # Function which checks if the card is an ace.
    def check_for_ace(self, card):
        if card[0] == "A":
            return True

    # Popup which allows user to choose if they want the Ace to be High or low.
    # Will not show if both starting cards are Aces, or if the player starts with BlackJack
    def ace_popup(self, p, card):
        box = FloatLayout()

        high = Button(text='High', size_hint=(0.2, 0.2),pos_hint=({'center_x':0.4, 'center_y':0.3} ))
        
        lower = Button(text='Low', size_hint=(0.2, 0.2), pos_hint=({'center_x':0.6, 'center_y':0.3} ))

        close = Button(text='Close', size_hint=(0.13, 0.13), pos_hint=({'center_x':0.9, 'center_y':0.9} ))

        lbl = Label(text='Do you want it to be high or low? (5 seconds to select)', pos_hint=({'center_x':0.5, 'center_y':0.7} ) )

        box.add_widget(high)
        box.add_widget(lower)
        box.add_widget(lbl)
        box.add_widget(close)

        popup = Popup(title='You have an Ace!',content=box,
        size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        popup.open()

        high.bind(on_press=lambda *args: bjack.ace_high(p, card, self.round_of_betting))
        lower.bind(on_press=lambda *args: bjack.ace_low(p, card, self.round_of_betting))
        close.bind(on_press=popup.dismiss)

    # update cards is a function which completes the first round of giving players cards.
    # several checks are made to the cards, including whether the player has an Ace, two Aces or blackjack.
    def update_cards(self, cards,p):
        for card_pos in range(len(cards)):
            # check if both hole cards are Aces
            if self.check_for_ace(cards[0].print_card()) == True and self.check_for_ace(cards[1].print_card()) == True:
                p.score = 12
                cards[0].value = 11
                cards[1].value = 1
            
            # check for any aces 
            elif self.check_for_ace(cards[0].print_card()) == True:
                # check if player has blackjack
                if cards[1].card_value() == 10:
                    Clock.schedule_once(self.win_with_bj, 0.5)
                else:
                    self.ace_popup(p, cards[0])
                    Clock.schedule_once(lambda *args: self.wait_for_input(p, cards[0]), 5)
            elif self.check_for_ace(cards[1].print_card()) == True:
                # check if player has blackjack
                if cards[0].card_value() == 10:
                    Clock.schedule_once(self.win_with_bj, 0.5)
                else:
                    self.ace_popup(p, cards[1])
                    Clock.schedule_once(lambda *args: self.wait_for_input(p, cards[1]), 5)

            
            self.add_widget(Image(source="src/Cards/"+cards[card_pos].print_card(), pos_hint=({'center_x':.4+(card_pos/10), 'center_y':.5}), size_hint=(.800, .800)))
    
    def update_single_card(self, card, pos):
        self.add_widget(Image(source="src/Cards/"+card.print_card(), pos_hint=({'center_x':.4+(pos/10), 'center_y':.5}), size_hint=(.800, .800)))

    # Function for getting a new card.
    def hit(self):
        self.round_of_betting+=1
        deck = self.active_deck.get_active_deck()
        p = self.current_players[self.player_num]
        next_card = bjack.hit(self.current_players[self.player_num], deck)
        p.hand_length += 1

        if next_card == False or next_card == True:
            print("break")
        else:
            if self.check_for_ace(next_card.print_card()) == True:

                self.ace_popup(p, next_card)
                Clock.schedule_once(lambda *args: self.wait_for_input(p,next_card), 5)
            
            else:
                self.update_score_str(p.score)
                self.update_single_card(next_card, p.hand_length)
                self.check_score(p)

    # Function which waits for input from the Ace Popup.
    def wait_for_input(self,p, next_card):
        self.update_score_str(p.score)
        self.update_single_card(next_card, p.hand_length)
        self.check_score(p)

    # Function for ending the game if the player chooses.
    def stick(self):
        Clock.schedule_once(self.win_end_game, 0.5)

    # Function to check player's running score.
    def check_score(self, p):
        if p.score > 21:
            self.player_bust()

        elif p.score == 21:
            self.player_wins()
        else:
            print(p.score, "current")
    
    # Win and Lose Screens
    def player_bust(self):
        Clock.schedule_once(self.lose_end_game, 0.5)
    
    def player_wins(self):
        Clock.schedule_once(self.win_end_game, 0.5)

    def lose_end_game(self, dt):
        blackjack_app.screen_manager.current ='Lose'
    
    def win_end_game(self, dt):
        blackjack_app.screen_manager.current='Win'
    
    def win_with_bj(self, dt):
        blackjack_app.screen_manager.current='Win_With_Blackjack'

# Menu widget where the user enters their name.    
class menu_popup(Widget):
    menu_layout = GridLayout(cols=2)
    def menu_popup(self):
        box = FloatLayout()
        self.player_names = TextInput(text='', multiline=False, size_hint=(0.5, 0.1), pos_hint=({'center_x':0.5, 'center_y':0.59}), on_text_validate=self.submit_names)
        submit = Button(text='Submit', size_hint=(0.2, 0.2), pos_hint=({'center_x':0.5, 'center_y':0.4}), on_press=self.submit_names)
        lbl = Label(text='Enter your name', pos_hint=({'center_x':0.5, 'center_y':0.7} ) )

        box.add_widget(self.player_names)
        box.add_widget(submit)
        box.add_widget(lbl)
        
        popup = Popup(title='Main Menu',content=box,
        size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        submit.bind(on_press=popup.dismiss)
        popup.open()
        return self.menu_layout

    def submit_names(self, obj):
        def create_deck_class(deck):
            active_deck=ActiveDeck(deck)
            return active_deck

        try:
            list_of_names = []
            list_of_names.append(self.player_names.text.split(" "))
            BlackJack.current_players=bjack.create_players(1, list_of_names[0])

            # Form Deck
            deck = Deck()
            deck.shuffle()

            active_deck = create_deck_class(deck)

            bjack.play(BlackJack.current_players, deck)

            def next_screen():
                blackjack_app.screen_manager.current = 'BlackJack'
                blackjack_app.blackjack_page.get_player_hand(active_deck)
            Clock.schedule_once(next_screen(), 1)
            
        except ValueError:
            print("Please enter a number between 1 and 7.")

# Screen for if the player wins with BlackJack
class win_with_blackjack(Widget):
    layout = FloatLayout()

    def build_endgame(self):
        label_win = Label(text="You Won with BlackJack!", pos_hint=({'center_x':0.5, 'center_y':0.5}), font_size=30)
        self.layout.add_widget(label_win)
        return self.layout

# Screen for if the player wins with 21 or by sticking.
class Win(Widget):
    layout = FloatLayout()

    def build_endgame(self):
        label_win = Label(text="You Win!", pos_hint=({'center_x':0.5, 'center_y':0.5}), font_size=30)
        self.layout.add_widget(label_win)
        return self.layout
# Screen for if the player loses.
class Lose(Widget):
    layout = FloatLayout()

    def build_endgame(self):
        label_lose = Label(text="You Lose!", pos_hint=({'center_x':0.5, 'center_y':0.5}), font_size=30)
        self.layout.add_widget(label_lose)
        return self.layout

# Contains all screens
class BlackJackApp(App):
    def build(self):

        self.screen_manager = ScreenManager()

        # Main Screen
        self.blackjack_page = BlackJack()
        screen_main = Screen(name='BlackJack')
        screen_main.add_widget(self.blackjack_page)
        self.screen_manager.add_widget(screen_main)
        
        # Loss Screen
        self.lose_end_game_page = Lose().build_endgame()
        screen_lose = Screen(name='Lose')
        screen_lose.add_widget(self.lose_end_game_page)
        self.screen_manager.add_widget(screen_lose)
        
        # Win Screen
        self.win_end_game_page = Win().build_endgame()
        screen_win = Screen(name='Win')
        screen_win.add_widget(self.win_end_game_page)
        self.screen_manager.add_widget(screen_win)

        # BlackJack Screen
        self.bj_win_end_game_page = win_with_blackjack().build_endgame()
        screen_win_bj = Screen(name='Win_With_Blackjack')
        screen_win_bj.add_widget(self.bj_win_end_game_page)
        self.screen_manager.add_widget(screen_win_bj)

        # Menu Screen
        self.menu_page =  menu_popup().menu_popup()
        screen_menu = Screen(name='menu')
        screen_menu.add_widget(self.menu_page)
        self.screen_manager.add_widget(screen_menu)

        self.screen_manager.current='menu'
        return self.screen_manager

if __name__ == '__main__':
   blackjack_app = BlackJackApp()
   blackjack_app.run()