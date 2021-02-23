from   discord.ext import commands
import asyncio

class Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):

        if   isinstance(err, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("❌")
        elif isinstance(err, commands.ExtensionNotLoaded):
            await ctx.message.add_reaction("❌")
        elif isinstance(err, commands.ExtensionNotFound):
            await ctx.message.add_reaction("🚫")
        elif isinstance(err, commands.MissingPermissions):
            await ctx.message.add_reaction("👮")
        else:
            print(err)
            await ctx.message.add_reaction("❓")
    
        await asyncio.sleep(3)
        # await ctx.message.delete() # debugshit
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction("✅")
        await asyncio.sleep(3)
        await ctx.message.delete()

    @commands.command(pass_context=True)
    async def unload(self, ctx, ext=None):
        ext = f"cogs.{ext}" if not '.' in ext else ext
        self.bot.unload_extension(ext)
        
    @commands.command(pass_context=True)
    async def load(self, ctx, ext):
        ext = f"cogs.{ext}" if not '.' in ext else ext
        self.bot.load_extension(ext)

    @commands.command(pass_context=True)
    async def reload(self, ctx, ext):
        ext = f"cogs.{ext}" if not '.' in ext else ext
        self.bot.reload_extension(ext)   

def setup(bot):
    print("Loaded cogs module.")
    bot.add_cog(Cogs(bot))

def teardown(bot):
    print("Unloaded cogs module")
    bot.remove_cog(Cogs(bot))