import random
import discord
from discord.ext import commands
from discord import app_commands

RPS = ['rock','paper','scissors']

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name='rps',description='Feeling lucky? Try Rock/Paper/Scissors with Aiko')
    @app_commands.choices(choices=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ]
    )
    async def rps(self,interaction:discord.Interaction,choices: app_commands.Choice[str]):
        user_id = interaction.user.id
        username = interaction.user.name

        bot_choice = random.choice(RPS)
        if (choices.value == bot_choice):
            counter = 'That\'s a tie! Once more!!.'
            await interaction.response.send_message(f"{bot_choice}. {counter}")
        elif (choices.value == 'rock'):
            if bot_choice == 'paper':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!📈'
                # award_points(user_id,username,10)
                await interaction.response.send_message(f"{bot_choice}. {counter}")

        elif (choices.value == 'paper'):
            if bot_choice == 'scissors':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!📈'
                # award_points(user_id,username,1)
                await interaction.response.send_message(f"{bot_choice}. {counter}")

        elif (choices.value == 'scissors'):
            if bot_choice == 'rock':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!📈'
                # award_points(user_id,username,1)
                await interaction.response.send_message(f"{bot_choice}. {counter}")
        
            
        else:
            counter = 'Enter Valid Input Bozo'
            await interaction.response.send_message(counter)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))