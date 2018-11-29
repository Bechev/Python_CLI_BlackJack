import random

CARD_SCORES_DICTIONNARY = {
        "AC":11, "2C":2, "3C":3, "4C":4, "5C":5, "6C":6, "7C":7, "8C":8, "9C":9, "10C":10, "JC":10, "QC":10, "KC":10,
        "AD":11, "2D":2, "3D":3, "4D":4, "5D":5, "6D":6, "7D":7, "8D":8, "9D":9, "10D":10, "JD":10, "QD":10, "KD":10,
        "AS":11, "2S":2, "3S":3, "4S":4, "5S":5, "6S":6, "7S":7, "8S":8, "9S":9, "10S":10, "JS":10, "QS":10, "KS":10,
        "AH":11, "2H":2, "3H":3, "4H":4, "5H":5, "6H":6, "7H":7, "8H":8, "9H":9, "10H":10, "JH":10, "QH":10, "KH":10
    }



class Deck:
    def __init__(self, deck_number=1):
        self.deck = [
                    "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
                    "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
                    "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
                    "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH" 
                    ]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def feed_n_cards(self, number_of_cards_fed):
        cards_fed = []
        try:
            for card in range (0, number_of_cards_fed):
                cards_fed.append(self.deck[0])
                self.deck.pop(0)
        except IndexError:
            raise IndexError("Not enough cards left in the deck")
        return cards_fed


class Player:
    def __init__(self, name="Player", funds=0):
        self.name = name
        self.funds = funds
        self.hand = []
        self.bet = 0
        self.hand_score = 0
        self.hand_status = "loosing"

    def draw_cards(self, cards_drawn):
        for card in range(0, len(cards_drawn)):
            self.hand.append(cards_drawn[card])
        return self
    
    def place_bet(self, bet):
        if bet <= self.funds:
            self.bet = bet  
            self.funds -= self.bet
        else:
            raise ValueError("Insufficient funds for the bet")

    def calculate_score(self):
        self.hand_score = 0
        number_of_aces = 0

        for card in self.hand:
            if card[0] == "A":
                number_of_aces += 1
            else:
                self.hand_score += CARD_SCORES_DICTIONNARY[card]
        
        if number_of_aces > 0:
            if self.hand_score > 10:
                self.hand_score += number_of_aces
            
            elif self.hand_score == 10:
                if number_of_aces == 1:
                    self.hand_score += 11
                else:
                    self.hand_score += number_of_aces
            
            else: # when hand_score < 10
                if (self.hand_score + 11 + (number_of_aces - 1)) > 21:
                    self.hand_score += number_of_aces
                else:
                    self.hand_score += 11 + (number_of_aces - 1)

        self.hand_score = self.hand_score

    def pay(self):
        if self.hand_status == 'blackjack':
            self.funds += self.bet * 2.5
        
        elif self.hand_status == 'winning':
            self.funds += self.bet * 2
        
        elif self.hand_status == 'tie':
            self.funds += self.bet
        
        elif self.hand_status == 'losing':
            self.bet = 0



class Game:

    def __init__(self):
        pass        

    def play_game(self):
        self.players = []
        self.play = True

        self.welcome()
        self.prepare_deck()
        self.create_dealer()
        self.create_players()

        while self.play == True:
            self.turn()


    def welcome(self):
        welcome ="""
        ####################################
        #                                  #
        #                                  #
        #    Welcome to CLI Py-BlackJack   #
        #                                  #
        #                                  #
        ####################################
        """
        print(welcome)
    
    def prepare_deck(self):
        self.deck = Deck()
        self.deck.shuffle_deck()

    
    def create_dealer(self):
        self.dealer = Player()
        self.dealer.name = "Dealer"
        self.dealer.funds = 10000000
    
    
    def create_players(self):
        self.number_of_players = int(input("How many players tonight? (1-5)\n"))
        for player_number in range(0, self.number_of_players):
            player = Player()
            self.players.append(player)
            self.ask_players_info(player, player_number)
    

    def ask_players_info(self, player, index):
        player.name = str(input("Player " + str(index + 1) +", what is your name?\n"))
        player.funds = int(input("Welcome "+ player.name+ ", what is your buy-in tonight?\n")) 


    def turn(self):

        for player in self.players:
            self.collect_bets(player)
        
        for player in self.players:
            self.draw_cards(player)

        self.dealer.draw_cards(self.deck.feed_n_cards(2))
        self.tease_dealer_hand()
        self.display_players_cards()
        self.hit_cards()
        self.display_dealer_hand()
        self.hit_dealer_cards()
        self.determine_winners()
        self.pay_players()

        if str(input("Play another turn? (y/n)\n")) == "y":
            self.reset_table()
        else: 
            self.play = False


    def collect_bets(self, player):
        if player.funds > 0:
            player.bet = int(input(player.name + ", please place your bet (0 - " + str(player.funds) + ")\n"))
            player.funds -= player.bet
        else:
            player.bet = 0

    def draw_cards(self, player):
        if player.bet == 0:
            pass
        else:
            player.draw_cards(self.deck.feed_n_cards(2))


    def tease_dealer_hand(self):
        print("Dealer's hand: "+ str(self.dealer.hand[1]))


    def display_dealer_hand(self):
        self.dealer.calculate_score()
        print("Dealer's hand: "+ str(self.dealer.hand)+". "+ str(self.dealer.hand_score) + " points")


    def hit_dealer_cards(self):
        while self.dealer.hand_score < 16:
            self.dealer.draw_cards(self.deck.feed_n_cards(1))
            self.dealer.calculate_score()
            self.display_dealer_hand()

    
    def display_players_cards(self):
        for player in self.players:
            player.calculate_score()
            if player.bet > 0:
                print(player.name + ": " + str(player.hand) + str(player.hand_score) + " points")


    def hit_cards(self):
        for player in self.players:
            if player.bet == 0:
                pass
            else:
                while player.hand_score < 21 and str(input(player.name + ", hit a card? (y/n)\n")) == "y":
                    player.draw_cards(self.deck.feed_n_cards(1))
                    player.calculate_score()
                    self.display_players_cards()


    def determine_winners(self):
        for player in self.players:
            if player.hand_score > 21:
                player.hand_status = 'losing'
            else:
                if player.hand_score == 21 and len(player.hand) == 2:
                    player.hand_status = 'blackjack'
                elif self.dealer.hand_score <= 21:
                    if player.hand_score > self.dealer.hand_score:
                        player.hand_status = 'winning'
                    elif player.hand_score == self.dealer.hand_score:
                        player.hand_status = "tie"
                    else:
                        player.hand_status = 'losing'
                elif self.dealer.hand_score > 21:
                    if player.hand_score <= 21:
                        player.hand_status = 'winning'
                    else:
                        player.hand.status = 'losing'


    def pay_players(self):
        for player in self.players:
            if player.bet != 0:
                player.pay()
            print(player.funds)


    def reset_table(self):
        self.prepare_deck()
        self.create_dealer()
        for player in self.players:
            player.hand = []
            player.bet = 0
            player.hand_score = 0
            player.hand_status = "loosing"

game = Game()
game.play_game()