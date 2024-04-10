import random
import discord
from discord.ext import commands
from discord import app_commands
import sys

sys.path.append('Bot/')
from Utils.Rewards import award_points,view_points

RPS = ['rock','paper','scissors']
SLOT_MACHINE =[":8ball:",":moneybag:",":coin:",":gem:",":cherries:",":money_with_wings:"]

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

    @app_commands.command(name='slot',description="Let's see, How much luck do you have...")
    async def slot(self,interaction:discord.Interaction):
        user_id = interaction.user.id
        username = interaction.user.name
        special_emoji = ":money_with_wings:"
        first_box = random.choice(SLOT_MACHINE)
        second_box = random.choice(SLOT_MACHINE)
        third_box = random.choice(SLOT_MACHINE)

        jackpot = "500"
        winningpoint = "250"
        secondwinningpoint = "100"
        loserpoint = "0"

        slotMachineEmbeds = discord.Embed(title="Jungle Jackpot: Spin Your Way to Riches in the Wild!",colour=discord.Colour.random())
        slotMachineEmbeds.set_thumbnail(url="https://media.tenor.com/QMfaVm3kNy0AAAAi/moneda-girando-spinning.gif")
        if(first_box == special_emoji and second_box == special_emoji and third_box == special_emoji):
            winning_line = first_box,"  ",second_box,"  ",third_box
            slotMachineEmbeds.description = winning_line
            slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + jackpot)
            slotMachineEmbeds.set_footer(text="JACKPOT BITCH! You're a winner with this fantastic slot line!✨")
            slotMachineEmbeds.set_image(url="https://c.tenor.com/CSWyS926r04AAAAd/tenor.gif")
            award_points(user_id,username,int(jackpot))
        elif(((first_box == second_box)!= special_emoji) and ((first_box==third_box)!=special_emoji) and ((second_box==third_box)!= special_emoji)):
            winning_line = first_box,"  ",second_box,"  ",third_box
            slotMachineEmbeds.description = winning_line
            slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + winningpoint)
            slotMachineEmbeds.set_footer(text="You're a winner with this fantastic slot line!✨")
            slotMachineEmbeds.set_image(url="https://media.tenor.com/2euepBwORpgAAAAi/diluc-kaeya.gif")
            award_points(user_id,username,int(winningpoint))
        elif(((first_box == second_box)!= special_emoji) or ((first_box==third_box)!=special_emoji) or ((second_box==third_box)!= special_emoji)):
            winning_line = first_box,"  ",second_box,"  ",third_box
            slotMachineEmbeds.description = winning_line
            slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + secondwinningpoint)
            slotMachineEmbeds.set_footer(text="You have less luck than meee!✨")
            slotMachineEmbeds.set_image(url="https://media.tenor.com/2euepBwORpgAAAAi/diluc-kaeya.gif")
            award_points(user_id,username,int(secondwinningpoint))
        else:
            winning_line = first_box,"  ",second_box,"  ",third_box
            slotMachineEmbeds.description = winning_line
            slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + loserpoint)
            slotMachineEmbeds.set_footer(text="You are a loser bitch...")
            slotMachineEmbeds.set_image(url="https://c.tenor.com/nNQa-ZjLAzgAAAAC/tenor.gif")
            award_points(user_id,username,0)
        await interaction.response.send_message(embed=slotMachineEmbeds)

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