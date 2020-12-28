import random
import time

class User:
    def __init__(self, name, bank=1000):
        self.name = name
        self.bank = bank
        self.bet  = 0
        self.hand = []
        self.status = ""
    
    def __repr__(self):
        return self.name

    def set_bet(self, a):
        if a <= self.bank:
            self.bet = a
            self.bank -= self.bet
        else:
            raise Exception("Insufficiant funds.")

class Dealer:
    def __init__(self):
        self.hand = []
        self.status = ""

class Deck:
    def __init__(self):
        self.cards = [f"{v}{s}" for s in "♠♣♥♦" for v in [str(i) for i in range(2, 11)] + list("JQKA")]
        random.shuffle(self.cards)
    
    def deal(self):
        try:
            return self.cards.pop()
        except IndexError:
            self.__init__() # reset cards
            return self.cards.pop()

class Game:
    def __init__(self, min_bet=100, max_bet=1000):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.players = []    

    def __repr__(self):
        return f"Game Started! Min bet: {self.min_bet}. Max bet: {self.max_bet}."    

    def add_players(self, *player:User):
        self.players.extend(player)
    
    def place_bet(self, player):
        amount = int(input(f"{player} enter a bet: \n"))
        if amount <= self.max_bet and amount >= self.min_bet:
            player.set_bet(amount)
        else:
            self.place_bet(player)
    
    def hand_value(self, hand):
        hand = [h[:-1] for h in hand] # removes suit
        value = 0

        for card in hand:
            if card in "JQK":
                value += 10
            elif card != "A":
                value += int(card)
            else: # ace case
                value += 11
        
        for card in hand:
            if card == "A" and value > 21:
                value -= 10
        return value
    
    def play(self):
        self.add_players(User("kat"), User("yamn"))
        dealer = Dealer()

        gameloop = True
        while gameloop:

            for p in self.players:
                self.place_bet(p)
            
            dealer.hand.extend((deck.deal(), deck.deal()))
            print(f"dealer hand: {dealer.hand[0]} and ????")

            for p in self.players:
                p.hand.extend((deck.deal(), deck.deal()))
                print(f"{p} hand: {p.hand}, value: {self.hand_value(p.hand)}{'. Blackjack!' if self.hand_value(p.hand) == 21 else ''}")
            
            for p in self.players:

                if self.hand_value(p.hand) == 21:
                    p.status = "blackjack"
                    continue
            
                # being able to double incorrectly is only an issue on commandline
                p.status = input(f"{p}: surrender / hit / double / stay: \n")

                if p.status == "surrender":
                    continue # half money is returned during rewawrd phase
                elif p.status == "stay":
                    continue
                elif p.status == "double":
                    p.set_bet(p.bet)
                    p.bet = p.bet * 2
                    p.hand.append(deck.deal())
                    print(f"{p} hand: {p.hand}, value: {self.hand_value(p.hand)}{'. busted!' if self.hand_value(p.hand) > 21 else ''}")

                    if self.hand_value(p.hand) > 21:
                        p.status = "bust"

                if p.status == "hit":
                    while p.status == "hit":
                        p.hand.append(deck.deal())
                        print(f"{p} hand: {p.hand}, value: {self.hand_value(p.hand)}{'. busted!' if self.hand_value(p.hand) > 21 else ''}")
                        if self.hand_value(p.hand) > 21:
                            p.status = "bust"
                            continue
                        else:
                            p.status = input(f"{p}: hit / stay: \n")
                            if p.status == "stay":
                                continue

            print(f"Dealer hand: {dealer.hand}, value: {self.hand_value(dealer.hand)}")

            for p in self.players:
                if p.status != "surrender" and p.status != "bust":
                    if self.hand_value(dealer.hand) > self.hand_value(p.hand):
                        print(f"{p} lost to the dealer...")
                    elif self.hand_value(dealer.hand) == self.hand_value(p.hand):
                        print(f"{p} matched the dealer.")
                        p.bank += p.bet
                    else:
                        print(f"{p} beat the dealer!")
                        p.bank += p.bet * 2
                elif p.status == "bust":
                    print(f"{p} busted...")
                elif p.status == "surrender":
                    print(f"{p} surrendered...")
                    p.bank += int(p.bet / 2)
                p.bet = 0 # bet is reset regardless of outcome
                p.hand = []
            dealer.hand = []

            for p in self.players:
                print(f"{p}: Bank: {p.bank}")
        

if __name__ == "__main__":
    deck = Deck()
    game = Game()
    print(game)
    game.play()