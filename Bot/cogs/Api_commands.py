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

    @app_commands.command(name="ask_llama",description="ask llama model")
    async def askllama(self, interaction:discord.Interaction,prompt:str):
        await interaction.response.defer()
        llamaEmbed = discord.Embed(title="Copper's Response 🐐", colour=discord.Colour.random())
        response = ollama.chat(model='copper:1b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        llamaEmbed.description = response['message']['content']

        await interaction.followup.send(embed=llamaEmbed)

        
async def setup(bot: commands.Bot):
    await bot.add_cog(Api_commands(bot))
