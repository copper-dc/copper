import discord
from discord.app_commands import commands
from discord import app_commands

class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup-profile",description="Setup your profile")
    '''This class for setup a user profile 
    like Name,
    Gender,
    Relationship with,
    Status,
    Hobbies.'''




async def setup(bot: commands.Bot):
    await bot.add_cog(user(bot))