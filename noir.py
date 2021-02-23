from   discord.ext import commands
import discord, json

class GamesBot(commands.Bot):

    def __init__(self, token, command_prefix):
        self.token          = token
        self.command_prefix = command_prefix
        super().__init__(command_prefix=self.command_prefix)

        try:
            # for filename in os.listdir('./cogs'):
            #     if filename.endswith('.py'):
            #         self.load_extension(f'cogs.{filename[:-3]}')
            self.load_extension("cogs.cogs")
            self.load_extension("cogs.blackjack")

        except Exception as e:
            print(f"Error loading extensions: ({type(e).__name__}) {e}")
    
    async def on_ready(self):
        print("Bot is online.")
        #await self.change_presence(activity=discord.Game("games"))

    async def on_message(self, message):
        if message.author.bot or message.author == self.user:
            return False
        
        await self.process_commands(message)

    def run(self):
        super().run(self.token, reconnect=True)
    
if __name__ == "__main__":
    with open("settings.json") as settings:
        sett = json.load(settings)
        token = sett["DISCORD_TOKEN"]
        prefix = sett["DISCORD_PREFIX"]
    bot = GamesBot(token, prefix)

    try:
        bot.run()
    except Exception as e:
        print(f"Error occurred: ({type(e).__name__}) {e}")
    finally:
        print("Bot is offline.")



# import discord, time, logging, sys, json
# from discord.ext import commands
# from blackjack import Game

# with open("settings.json") as settings:
#     sett = json.load(settings)
#     token = sett["DISCORD_TOKEN"]
#     prefix = sett["DISCORD_PREFIX"]

# bot = commands.Bot(command_prefix=prefix)

# LOGGING_LEVEL = logging.INFO
# logging.basicConfig(level=LOGGING_LEVEL, datefmt="%H:%M:%S",
#                     format="[%(asctime)s] [%(levelname)8s] >>> %(message)s (%(filename)s:%(lineno)s)",
#                     handlers=[logging.FileHandler("latest.log"), logging.StreamHandler(sys.stdout)])

# logger = logging.getLogger(__name__)

# @bot.event
# async def on_ready():
#         logger.info("Blackjack ready.")

# # @bot.event
# # async def on_message(msg):
# #     await bot.process_commands(msg)

# @bot.command()
# async def play(msg):
#     await msg.channel.send("test complete")



# try:
#     self.load_extension("cogs.cogs")
#     self.load_extension("cogs.blackjack")
# except Exception as e:
#     print(f"Error loading extensions: ({type(e).__name__}) {e}")

# bot.run(token)