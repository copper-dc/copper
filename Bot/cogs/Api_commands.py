import asyncio
import base64
from datetime import date
from io import BytesIO
from operator import ge
import random
import aiohttp
from click import prompt
import discord
import os
from discord.ext import commands
from discord import InteractionResponse, app_commands
import requests
from translate import Translator
from craiyon import Craiyon, craiyon_utils


waifuBaseURL = "https://api.waifu.pics/"
RANDOMGIRLBASEURL = "https://randomuser.me/api/?gender=female"
RANDOMCATBASEURL = "https://api.thecatapi.com/v1/images/search"
RANDOMDOGBASEURL = "https://api.thedogapi.com/v1/images/search"
GITHUBBASEAPI = "https://api.github.com/users/"

class Api_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name="github-profile",description="Get the github descriptions of the user.")
    async def github_profile(self, interaction: discord.Interaction, username:str):
        updatedGITHUBAPIURL = GITHUBBASEAPI+username
        response = requests.get(updatedGITHUBAPIURL)
        if response.status_code == 200:
            data = response.json()
            avatar_url = data['avatar_url']
            followers = data['followers']
            following = data['following']
            bio = data['bio']
            user = data['login']
            GithubEmbed = discord.Embed(title="**"+user+"**",colour=discord.Colour.random())
            GithubEmbed.description = bio
            GithubEmbed.add_field(name="Followers: ",value=followers,inline=True)
            GithubEmbed.add_field(name="Following: ",value=following,inline=True)
            GithubEmbed.set_thumbnail(url=avatar_url)
            await interaction.response.send_message(embed=GithubEmbed)
        else:
            await interaction.response.send_message("User not found!")

    
    @app_commands.command(name="random-cat",description="Generate random cat pictures....")
    async def random_cat(self, interaction: discord.Interaction):
        catEmbed = discord.Embed(title="Meow :cat:",colour=discord.Colour.random())
        response = requests.get(RANDOMCATBASEURL)
        if response.status_code == 200:
            data = response.json()
            img_url = data[0]['url']
            catEmbed.set_image(url=img_url)
        await interaction.response.send_message(embed=catEmbed)

    @app_commands.command(name="random-dog",description="Generate random dog pictures....")
    async def random_cat(self, interaction: discord.Interaction):
        dogEmbed = discord.Embed(title="Bow Wow Wow :dog:",colour=discord.Colour.random())
        response = requests.get(RANDOMDOGBASEURL)
        if response.status_code == 200:
            data = response.json()
            img_url = data[0]['url']
            dogEmbed.set_image(url=img_url)
        await interaction.response.send_message(embed=dogEmbed)
     
    
    @app_commands.command(name="slash-girls",description='Slash Girls? More like smashgirls; Generates random waifu image of your choice.')
    
    @app_commands.choices(girltype =[
        app_commands.Choice(name="Waifu", value="waifu"),
        app_commands.Choice(name="Neko", value="neko"),
        app_commands.Choice(name="Shinobu", value="shinobu"),
        app_commands.Choice(name="Megumin", value="megumin")
    ])
    @app_commands.choices(category =[
    app_commands.Choice(name="NSFW", value="nsfw")
    ])
    async def slashgirls(self,interaction: discord.Interaction, girltype: str, category: str = "sfw"):
        channel = interaction.channel
        
        if (girltype== 'neko'):
            imageCategory = "sfw" if category == "sfw" else "nsfw"
            if imageCategory == "nsfw":
                if await is_nsfw(channel=channel):
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)
                else:
                    await interaction.response.send_message("Try in a NSFW channel!")
            elif imageCategory == "sfw":
                await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)
            
        elif (girltype == 'waifu'):
            imageCategory = "sfw" if category == "sfw" else "nsfw"
            if imageCategory == "nsfw":
                if await is_nsfw(channel=channel):
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)
                else:
                    await interaction.response.send_message("Try in a NSFW channel!")
            elif imageCategory == "sfw":
                await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)

        elif (girltype=='megumin'):
                imageCategory = "sfw" if category == "sfw" else "nsfw"
                if imageCategory == "nsfw":
                    if await is_nsfw(channel=channel):
                        await interaction.response.send_message("Realy? No megumin nsfw!")
                    else:
                        await interaction.response.send_message("Try in a NSFW channel!")
                elif imageCategory == "sfw":
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)

        elif (girltype == 'shinobu'):
                imageCategory = "sfw" if category == "sfw" else "nsfw"
                if imageCategory == "nsfw":
                    if await is_nsfw(channel=channel):
                        await interaction.response.send_message("Really? No shinobu nsfw!")
                    else:
                        await interaction.response.send_message("Try in a NSFW channel!")
                elif imageCategory == "sfw":
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)






async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
        
        
async def fetch_img(imageCat: str, girltype:str, interaction: discord.Interaction):
    slashgirlsEmbeds = discord.Embed(title="Enjoy your slash girl 🤤",colour=discord.Colour.random())
    updatedURL = waifuBaseURL+imageCat+"/"+girltype
    data = await fetch_json(updatedURL)
    imgurl = data['url']
    slashgirlsEmbeds.set_image(url=imgurl)
    await interaction.response.send_message(embed=slashgirlsEmbeds)
        
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
