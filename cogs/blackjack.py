from discord import client
from discord.ext import commands
import random, asyncio

from discord.ext.commands import bot

class User:
    def __init__(self, author, chips):
        self.id = author.id
        self.name = author.name
        self.chips = chips
        self.bet = 0
        self.hand = []
        self.status = ""

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
    def __init__(self, bot, ctx):
        self.bot = bot
        self.player = User(ctx.author, 1000)
        self.ctx = ctx
        self.deck = Deck()
        self.dealer = Dealer()

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
        return f"{', ' .join([h for h in hand])}. Value: {value}.{blackjack}{bust}"
        
    async def place_bet(self, ctx):
        def check(m):
            return m.content.isdigit() and m.author == ctx.author and m.channel == ctx.channel
        await ctx.send(f"Place bet, {ctx.author.name} (total chips: {self.player.chips}):")
        return await self.bot.wait_for("message", check = check)

    async def start_game(self):
        self.player.bet = await self.place_bet(self.ctx)
        self.dealer.hand.extend((self.deck.deal(), self.deck.deal()))
        self.player.hand.extend((self.deck.deal(), self.deck.deal()))
        await self.ctx.send(f"Dealer hand: {self.dealer.hand[0]} and ??????")
        await self.ctx.send(f"{self.ctx.author.name}, your hand: {self.print_hand(self.player)}")
        await self.player_choice()

    async def player_choice(self):
        def check(m):
            return (m.content.lower() == "hit" or m.content.lower() == "stay") and m.author == self.ctx.author
        await self.ctx.send(f"{self.ctx.author.name}, hit / stay")
        choice = await self.bot.wait_for("message", check = check)
        if choice.content.lower() == "hit":
            self.player.hand.append(self.deck.deal())
            await self.ctx.send(f"{self.ctx.author.name}, your hand: {self.print_hand(self.player)}")
            if self.hand_value(self.player.hand) > 21:
                await self.ctx.send(f"{self.ctx.author.name}, you have busted. Dealer Wins")

            else:
                await self.player_choice()
        else: #if choice is "stay"
            await self.dealer_logic()
        
    async def dealer_logic(self):
        await self.ctx.send(f"Dealer hand: {self.print_hand(self.dealer)}")
        while self.hand_value(self.dealer.hand) < 17:
            await asyncio.sleep(2)
            self.dealer.hand.append(self.deck.deal())
            is_busted = ""
            if self.hand_value(self.dealer.hand) > 21:
                is_busted = " Dealer has busted."
            await self.ctx.send(f"Dealer hits: {self.print_hand(self.dealer)}{is_busted}")
        await self.end_game()

    async def end_game(self):
        if self.hand_value(self.player.hand) < self.hand_value(self.dealer.hand):
            await self.ctx.send(f"Dealer has beaten {self.ctx.author.name}")
        elif self.hand_value(self.player.hand) == self.hand_value(self.dealer.hand):
            await self.ctx.send(f"{self.ctx.author.name} has matched the dealer.")
        elif self.hand_value(self.player.hand) > self.hand_value(self.dealer.hand):
            await self.ctx.send(f"{self.ctx.author.name} has beaten the dealer!")

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx):
        game = Game(self.bot, ctx)
        await game.start_game()

def setup(bot):
    print("Loaded blackjack module.")
    bot.add_cog(Blackjack(bot))

def teardown(bot):
    print("Unloaded blackjack module.")
    bot.remove_cog(Blackjack(bot))