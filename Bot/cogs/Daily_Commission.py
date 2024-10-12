import asyncio
import base64
from datetime import date, timedelta
import discord
from discord.ext import commands
from discord import app_commands

from Utils.DataBase import findlastactive, update_db


class Daily_Commission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily-credit", description="Check-in for daily credit points.")
    async def daily_credit(self, interaction: discord.Interaction):
        daily_rewardEmbed = None
        user_id = interaction.user.id

        last_active_date = await findlastactive(user_id=user_id, flag=1)
        current_date = str(date.today())

        if last_active_date == current_date:
            daily_rewardEmbed = discord.Embed(title="You already collected your daily reward :white_check_mark:")
        else:
            streak_multiplier = 1
            if last_active_date:
                last_active_date_obj = date.fromisoformat(last_active_date)
                if last_active_date_obj == date.today() - timedelta(days=1):
                    user_streak = await find_user_streak(user_id)
                    streak_multiplier = 2 if user_streak >= 2 else 1  # Double the reward on the 3rd day

                    if streak_multiplier == 2:
                        await update_streak(user_id, reset=False)  # Reset streak to 0 after 3rd day
                else:
                    # Reset streak if they missed a day
                    await reset_streak(user_id)

            daily_rewardEmbed = discord.Embed(title="Your daily reward successfully collected :white_check_mark:")
            daily_rewardEmbed.set_thumbnail(url="https://media.tenor.com/8McIGu0Tf_QAAAAi/fire-joypixels.gif")
            earned_points = 50 * streak_multiplier
            daily_rewardEmbed.description = f"Your earned ${earned_points} from Aiko's daily reward."

            # Update the user's points and last active date in the database
            await update_db(user_id=user_id, points=earned_points, last_active=current_date)
            await update_streak(user_id, increment=True)

        await interaction.response.send_message(embed=daily_rewardEmbed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Daily_Commission(bot))



async def find_user_streak(user_id):

    pass


async def reset_streak(user_id):
    pass


async def update_streak(user_id, increment=False, reset=False):
    pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Daily_Commission(bot))