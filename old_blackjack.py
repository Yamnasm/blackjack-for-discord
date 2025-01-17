import random

'''/
This code is for the commandline version of the blackjack bot that was used to learn the game logic
it probably works, though there are some small things missing

keeping this file to use as reference now.

'''

class User:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.bet  = 0
        self.hand = []
        self.status = ""
    
    def __repr__(self):
        return self.name

class Dealer:
    def __init__(self):
        self.hand = []
        self.status = ""
    def __repr__(self):
        return "Dealer"

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
    def __init__(self, min_bet=100, max_bet=5000):
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
            if amount <= player.chips:
                player.bet = amount
                player.chips -= amount
            else:
                print("Insufficient chips to bet.")
                self.place_bet(player)
        else:
            print("Bet not within table limits.")
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

    def print_hand(self, target):
        hand = target.hand
        value = self.hand_value(hand)
        if len(hand) == 2 and value == 21:
            blackjack = " Blackjack!"
        else:
            blackjack = ""
        if value > 21:
            bust = " Busted!"
        else:
            bust = ""
        return f"{target} hand: {hand}. Value: {value}.{blackjack}{bust}"
    
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
                print(self.print_hand(p))
            
            for p in self.players:

                if self.hand_value(p.hand) == 21:
                    p.status = "blackjack"
                    continue
            
                # being able to double without adequate chips is only an issue on commandline
                p.status = input(f"{p}: surrender / hit {'/ double ' if p.bet <= p.chips else ''}/ stay: \n")

                if p.status == "surrender":
                    continue # half money is returned during rewawrd phase

                elif p.status == "stay":
                    continue

                elif p.status == "double":
                    p.chips -= p.bet
                    p.bet = p.bet * 2
                    p.hand.append(deck.deal())
                    print(self.print_hand(p))
                    p.status = "stay"

                    if self.hand_value(p.hand) > 21:
                        p.status = "bust"

                if p.status == "hit":
                    while p.status == "hit":
                        p.hand.append(deck.deal())
                        print(self.print_hand(p))
                        if self.hand_value(p.hand) > 21:
                            p.status = "bust"
                            continue
                        elif self.hand_value(p.hand) == 21:
                            print(f"{p} stays.")
                            p.status = "stay"
                        else:
                            p.status = input(f"{p}: hit / stay: \n")
                            if p.status == "stay":
                                continue

            print(self.print_hand(dealer))
            for p in self.players:
                if p.status == "stay":
                    while self.hand_value(dealer.hand) < 17:
                        print("Dealer hits.")
                        dealer.hand.append(deck.deal())
                        print(self.print_hand(dealer))
                        if self.hand_value(dealer.hand) > 21:
                            dealer.status = "bust"
                    break                

            # this is a fucking mess...
            for p in self.players:
                if p.status == "bust":
                    pass
                elif p.status == "surrender":
                    pass
                elif p.status != "surrender" and p.status != "bust" and dealer.status != "bust":
                    if self.hand_value(dealer.hand) > self.hand_value(p.hand):
                        print(f"{p} lost to the dealer...")
                    elif self.hand_value(dealer.hand) == self.hand_value(p.hand):
                        print(f"{p} matched the dealer.")
                        p.chips += p.bet
                    else:
                        print(f"{p} beat the dealer!")
                        p.chips += p.bet * 2
                elif p.status == "blackjack":
                    if dealer.status == "blackjack":
                        p.chips += p.bet
                    else:
                        p.chips += p.bet * 2.5                        
                elif dealer.status == "bust":
                    print(f"{p} beat the dealer!")
                    p.chips += p.bet * 2
                p.bet = 0 # bet is reset regardless of outcome
                p.hand = []
            dealer.hand = []

            for p in self.players:
                print(f"{p}: chips: {p.chips}")
            
            if input(f"Continue? Y/N \n").lower() == "n":
                gameloop = False
        
if __name__ == "__main__":
    deck = Deck()
    game = Game()
    print(game)
    game.play()