import aiohttp
import discord
import os
from discord.ext import commands
from discord import app_commands

waifuBaseURL = "https://api.waifu.pics/"

class Api_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @app_commands.command(name="slashgirls",description='Slash Girls? More like smashgirls; Generates random waifu image of your choice.')
    
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
