import random
import discord
from discord.ext import commands
from discord import app_commands
import sys

sys.path.append('Bot/')
from Utils.Rewards import award_points,view_points

RPS = ['rock','paper','scissors']

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name='rps',description='Feeling lucky? Try Rock/Paper/Scissors with Aiko')
    @app_commands.choices(choices=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ]
    )
    async def rps(self,interaction:discord.Interaction,choices: str):
        user_id = interaction.user.id
        username = interaction.user.name

        bot_choice = random.choice(RPS)
        if (choices == bot_choice):
            counter = 'That\'s a tie! Once more!!.'
            await interaction.response.send_message(f"{bot_choice}. {counter}")
        elif (choices== 'rock'):
            if bot_choice == 'paper':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!📈'
                award_points(user_id,username,10)
                await interaction.response.send_message(f"{bot_choice}. {counter}")

        elif (choices == 'paper'):
            if bot_choice == 'scissors':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!📈'
                award_points(user_id,username,10)
                await interaction.response.send_message(f"{bot_choice}. {counter}")

        elif (choices == 'scissors'):
            if bot_choice == 'rock':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!📈'
                award_points(user_id,username,10)
                await interaction.response.send_message(f"{bot_choice}. {counter}")
        
            
        else:
            counter = 'Enter Valid Input Bozo'
            await interaction.response.send_message(counter)

    @app_commands.command(name='view_points',description='Shows the points you earned from the games you won against the bot')
    async def view_points_cmd(self, interactions:discord.Interaction,member:discord.Member =None):
        if member is None:
            member = interactions.user.id
        elif member is not None:
            member = member.id
        points_info = view_points(member)
        await interactions.response.send_message(points_info)

    

async def setup(bot: commands.Bot):
    # print("Games is loaded")
    await bot.add_cog(Games(bot))