import pytest, mock, copy
from blackjack import Deck, Player, Game

@pytest.fixture
def my_deck():
    my_deck = Deck(1)
    return my_deck
    
@pytest.fixture
def alice(): 
    alice = Player("Alice", 100)
    return alice

@pytest.fixture
def bob(): 
    bob = Player("Alice", 100)
    return bob

@pytest.fixture
def game():
    game = Game()
    return game


################ Tests of the deck ##################
# Test the number of cards and uniqueness of the deck
def test_deck_creation(my_deck):
    assert len(my_deck.deck) ==  52
    assert len(my_deck.deck) == len(set(my_deck.deck))

# Test the randomization of the deck
def test_deck_randomization(my_deck):
    for x in range(1,10000):
        prev_deck = copy.deepcopy(my_deck.deck)
        my_deck.shuffle_deck()
        assert my_deck.deck != prev_deck

@pytest.mark.parametrize("number_of_cards_drawn, expected_output",[
    (2,2),
    (3,3),
    (5,5),
    (51,51),
    (52,52),
])

def test_cart_drawn(my_deck, number_of_cards_drawn, expected_output):
    assert len(my_deck.feed_n_cards(number_of_cards_drawn)) == expected_output

def test_raises_exception_on__number_of_cards_drawn_superior_to_rest_of_deck(my_deck):
    with pytest.raises(IndexError):
        my_deck.feed_n_cards(53)
#######################################################


################ Test the players ####################
def test_player_bets(alice):
    with pytest.raises(ValueError):
        alice.place_bet(alice.funds + 10)
 
@pytest.mark.parametrize("hand, score",[
    (["AS", "KS"], 21),
    (["3D", "5D"], 8),
    (["9S", "KS", "2S"], 21),
    (["AS", "AC", "AD"], 13),
    (["AS", "AC", "AD","9D"], 12),
    (["AS", "AC", "AD","QD", "KD"], 23),
])

def test_scores(alice, hand, score):
    alice.hand = hand
    alice.calculate_score()
    assert alice.hand_score  ==  score

@pytest.mark.parametrize("status, player_funds",[
    ('blackjack', 1150),
    ('winning', 1100),
    ('tie', 1000),
    ('losing', 900),
])

def test_payments(alice, status, player_funds):    
    alice.funds = 1000
    alice.place_bet(100)
    alice.hand_status = status
    alice.pay()
    assert alice.funds == player_funds
######################################################