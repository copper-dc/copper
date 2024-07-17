import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
import requests


RANDOMJOKESBASEURL = "https://api.chucknorris.io/jokes/random"
class Api_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    

    @app_commands.command(name="joke",description="random jokes by chucknorris")
    async def random_jokes(Self, interaction: discord.Interaction):
        response = requests.get(RANDOMJOKESBASEURL)
        data = response.json()
        value = data['value']
        jokeEmbed = discord.Embed(title=value,colour=discord.Colour.random())
        await interaction.response.send_message(embed=jokeEmbed)
     
    
        
    async def is_nsfw(channel: discord.Interaction.channel):
        if isinstance(channel,discord.TextChannel):
            if channel.nsfw:
                return True
            else:
                return False
        else:
            return "bruh"
        
async def setup(bot: commands.Bot):
    # print("Api_commands is loaded")
    await bot.add_cog(Api_commands(bot))
