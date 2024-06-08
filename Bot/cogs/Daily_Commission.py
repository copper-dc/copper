import asyncio
import base64
from datetime import date
import discord
import os
from discord.ext import commands
from discord import app_commands
from Utils.DataBase import findlastactive, update_db



class Daily_Commission(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="daily-credit",description="Checkin the daily credit points.")
    async def daily_credit(self,interaction: discord.Interaction):
        daily_rewardEmbed = None
        last_active_date = await findlastactive(user_id= interaction.user.id, flag=1)
        current_date = str(date.today())
        if last_active_date == current_date:
            daily_rewardEmbed = discord.Embed(title="You already collected your daily reward :white_check_mark:")
        else:
            daily_rewardEmbed = discord.Embed(title="Your daily reward successfully collected :white_check_mark:")
            daily_rewardEmbed.set_thumbnail(url="https://media.tenor.com/8McIGu0Tf_QAAAAi/fire-joypixels.gif")
            daily_rewardEmbed.description = "Your earned $50 from Aiko's daily reward."
            await update_db(user_id=interaction.user.id,points=50)
        await interaction.response.send_message(embed=daily_rewardEmbed)
    
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Daily_Commission(bot))
   