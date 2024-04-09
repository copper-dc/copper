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
        slashgirlsEmbeds = discord.Embed(title="Enjoy your slash girl 🤤",colour=discord.Colour.random())
        
        if (girltype== 'neko'):
            imageCategory = "sfw" if category == "sfw" else "nsfw"
            updatedURL = waifuBaseURL+imageCategory+"/neko"
            data = await fetch_json(updatedURL)
            imgurl = data['url']
            slashgirlsEmbeds.set_image(url=imgurl)
            await interaction.response.send_message(embed=slashgirlsEmbeds)
        elif (girltype == 'waifu'):
            imageCategory = "sfw" if category == "sfw" else "nsfw"
            updatedURL = waifuBaseURL+imageCategory+"/waifu"
            data = await fetch_json(updatedURL)
            imgurl = data['url']
            slashgirlsEmbeds.set_image(url=imgurl)
            await interaction.response.send_message(embed=slashgirlsEmbeds)
        elif (girltype=='megumin'):
            try:
                imageCategory = "sfw" if category == "sfw" else "nsfw"
                updatedURL = waifuBaseURL+imageCategory+"/megumin"
                data = await fetch_json(updatedURL)
                imgurl = data['url']
                slashgirlsEmbeds.set_image(url=imgurl)
                await interaction.response.send_message(embed=slashgirlsEmbeds)
            except Exception as e:
                await interaction.response.send_message("There is no NSFW image for megumin")
        elif (girltype == 'shinobu'):
            try:
                imageCategory = "sfw" if category == "sfw" else "nsfw"
                updatedURL = waifuBaseURL+imageCategory+"/shinobu"
                data = await fetch_json(updatedURL)
                imgurl = data['url']
                slashgirlsEmbeds.set_image(url=imgurl)
                await interaction.response.send_message(embed=slashgirlsEmbeds)
            except Exception as e:
                await interaction.response.send_message("There is no NSFW image for shinobu")
    

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
        
async def setup(bot: commands.Bot):
    # print("Api_commands is loaded")
    await bot.add_cog(Api_commands(bot))