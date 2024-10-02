import discord
import ollama
import requests
from discord import app_commands
from discord.ext import commands
import asyncio
from ollama import AsyncClient, embed

RANDOMJOKESBASEURL = "https://api.chucknorris.io/jokes/random"
class Api_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="joke",description="random jokes by chucknorris")
    async def random_jokes(self, interaction: discord.Interaction):
        response = requests.get(RANDOMJOKESBASEURL)
        data = response.json()
        value = data['value']
        jokeEmbed = discord.Embed(title=value,colour=discord.Colour.random())
        await interaction.response.send_message(embed=jokeEmbed)



        
async def setup(bot: commands.Bot):
    await bot.add_cog(Api_commands(bot))
