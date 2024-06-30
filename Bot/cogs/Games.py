import asyncio
import dis
import json
import random
import discord
from discord.ext import commands
from discord import app_commands
import requests
from Utils.DataBase import create_db, find, update_db,find

RPS = ['rock','paper','scissors']
SLOT_MACHINE =[":8ball:",":moneybag:",":coin:",":gem:",":cherries:",":money_with_wings:"]
GUESS_URL = "http://127.0.0.1:8000/get-quiz"

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.current_guess = None
        self.current_interaction = None
    
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
        rpsEmbeds = discord.Embed(title="Rock Paper Shoot!!!",colour = discord.Colour.random())
        rpsEmbeds.add_field(name="You chose: **" + choices + "**", value="**Bot chose: " + bot_choice + "**", inline=False)
        if((choices==bot_choice=="rock") or (choices==bot_choice=="scissors") or (choices==bot_choice=="paper")):
            rpsEmbeds.add_field(name="Your reward for this round",value="$25", inline=False)
            rpsEmbeds.description = "**Sorry, Tie**"
            await award_points(user_id,username,25)
        elif(choices=="rock"):
            rpsEmbeds.set_image(url="https://media.tenor.com/5XuwpvROzEoAAAAi/rock-paper-scissors-roshambo.gif")
            if(bot_choice== "scissors"):
                rpsEmbeds.description = "**you won** :grin:"
                rpsEmbeds.add_field(name="Your reward for this round",value="$50", inline=False)
                await award_points(user_id,username,50)
            else:
                rpsEmbeds.description = "**You Lost** :sob:"
                rpsEmbeds.add_field(name="Your reward for this round",value="$0", inline=False)
                await award_points(user_id, username, 0)
        elif(choices=="scissors"):
            rpsEmbeds.set_image(url="https://media.tenor.com/NyHqrePBRAEAAAAi/rock-paper-scissors-roshambo.gif")
            if(bot_choice == "paper"):
                rpsEmbeds.description = "**You Won** :grin:"
                rpsEmbeds.add_field(name="Your reward for this round",value="$50", inline=False)
                await award_points(user_id, username, 50)
            else:
                rpsEmbeds.description = "**You Lost** :sob:"
                rpsEmbeds.add_field(name="Your reward for this round",value="$0", inline=False)
                await award_points(user_id, username, 0)
        elif(choices == "paper"):
            rpsEmbeds.set_image(url="https://media.tenor.com/iXeUwKbISiQAAAAi/rock-paper-scissors-roshambo.gif")
            if(bot_choice == "rock"):
                rpsEmbeds.description = "**You Won** :grin:"
                rpsEmbeds.add_field(name="Your reward for this round",value="$50", inline=False)
                await award_points(user_id, username, 50)
            else:
                rpsEmbeds.description = "**You Lost** :sob:"
                rpsEmbeds.add_field(name="Your reward for this round",value="$0", inline=False)
                await award_points(user_id, username, 0)
        await  interaction.response.send_message(embed = rpsEmbeds)

    @app_commands.command(name="transfer",description="Transfer money to your friends, waifu, business partner too...")
    async def transfer_money(self, interactions: discord.Interaction, user: discord.Member, amount: int):
        new_total_point = await find(interactions.user.id,1) -  amount
        user_id = user.id
        username = user.name
        current_points = await find(user_id= interactions.user.id, flag=1)
        if (amount > 0 and interactions.user != user):
            if (str(user_id) == "1180739731890380861"):
                await interactions.response.send_message("hmph i dont need it!")
                return
            if (current_points >= amount):
                await update_db(user_id=interactions.user.id, points=new_total_point, flag="update hehe")
                await award_points(user_id,username,amount)
                transferEmbed = discord.Embed(title="Transaction Successfull :white_check_mark:",colour=discord.Colour.green())
                transferEmbed.description = interactions.user.mention+f" transferred ${amount}, to "+ user.mention
                await interactions.response.send_message(embed=transferEmbed)
            else:
                await interactions.response.send_message("you dont have enough baka! ")
        else:
            await interactions.response.send_message("CHEATING")




    @app_commands.command(name='slot',description="Let's see, How much luck do you have...")
    async def slot(self,interaction:discord.Interaction, money: int):
        if(money==100):
            user_id = interaction.user.id
            username = interaction.user.name
            special_emoji = ":money_with_wings:"
            first_box = random.choice(SLOT_MACHINE)
            second_box = random.choice(SLOT_MACHINE)
            third_box = random.choice(SLOT_MACHINE)

            jackpot = "500"
            winningpoint = "250"
            loserpoint = "0"

            slotMachineEmbeds = discord.Embed(title="Jungle Jackpot: Spin Your Way to Riches in the Wild!",colour=discord.Colour.random())
            slotMachineEmbeds.set_thumbnail(url="https://media.tenor.com/QMfaVm3kNy0AAAAi/moneda-girando-spinning.gif")
            if(first_box == second_box == third_box == special_emoji):
                winning_line = first_box+"  "+second_box+"  "+third_box
                slotMachineEmbeds.description = winning_line
                slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + jackpot)
                slotMachineEmbeds.set_footer(text="JACKPOT BITCH! You're a winner with this fantastic slot line!✨")
                slotMachineEmbeds.set_image(url="https://c.tenor.com/CSWyS926r04AAAAd/tenor.gif")
                await award_points(user_id,username,500)
            elif(first_box == second_box or first_box == third_box or second_box == third_box):
                winning_line = first_box+"  "+second_box+"  "+third_box
                slotMachineEmbeds.description = winning_line
                slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + winningpoint)
                slotMachineEmbeds.set_footer(text="You have less luck than meee!")
                slotMachineEmbeds.set_image(url="https://media.tenor.com/2euepBwORpgAAAAi/diluc-kaeya.gif")
                await award_points(user_id,username,250)
            else:
                winning_line = first_box+"  "+second_box+"  "+third_box
                slotMachineEmbeds.description = winning_line
                slotMachineEmbeds.add_field(name="Your Reward for this slot", value=":coin: " + loserpoint)
                slotMachineEmbeds.set_footer(text="You are a loser bitch...")
                slotMachineEmbeds.set_image(url="https://c.tenor.com/nNQa-ZjLAzgAAAAC/tenor.gif")
                await award_points(user_id,username,0)
            await interaction.response.send_message(embed=slotMachineEmbeds)
        else:
            await interaction.response.send_message("The base maoney to play this game is $100")

    
    @app_commands.command(name="character_guess",description="Guess the anime character name by their pics")
    async def character_guess(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        username = interaction.user.name
        if self.current_interaction:
            await interaction.response.send_message("A game is already in progress. Please wait for it to finish.", ephemeral=True)
            return

        self.current_interaction = interaction

        anime_guess_embed = discord.Embed(title="Guess the Character?", colour=discord.Colour.random())
        timegoingEmbed = discord.Embed(title="Time is going :timer: only 15 seconds left!", colour=discord.Colour.random())
        winnerEmbed = discord.Embed(title="Winner is", colour=discord.Colour.random())
        answerEmbed = discord.Embed(title="Correct answer is ",colour=discord.Colour.random())
        data = None
        with open('JSON/anime_character.json') as f:
            data = json.load(f)
        random.shuffle(data)
        anime_char_ind = 0
        character = data[anime_char_ind]
        self.current_guess = character['name']  # List of possible names

        # Print the correct answer in the terminal
        print(f"Correct answer: {self.current_guess}")

        anime_guess_embed.set_image(url=character['img'])
        await interaction.response.send_message(embed=anime_guess_embed)

        def check(m):
            return m.channel == interaction.channel and any(map(lambda name: m.content.lower() == name.lower(), self.current_guess))

        async def notify_half_time():
            await asyncio.sleep(15)
            await interaction.followup.send(embed=timegoingEmbed)

        async def wait_for_response():
            try:
                response = await self.bot.wait_for("message", timeout=30.0, check=check)
                winnerEmbed.description = f"{interaction.user.mention}, Here is your reward $100"
                await interaction.followup.send(embed=winnerEmbed)
                await award_points(user_id,username,100)
                return True
            except asyncio.TimeoutError:
                return False

        notify_task = self.bot.loop.create_task(notify_half_time())
        response_received = await wait_for_response()

        if response_received:
            notify_task.cancel()
        else:
            answerEmbed.description = f",".join(self.current_guess)
            await interaction.followup.send(embed=answerEmbed)

        # Reset the state
        self.current_guess = None
        self.current_interaction = None

    @app_commands.command(name='balance',description='Shows the points you earned from the games you won against the bot')
    async def view_points_cmd(self, interactions:discord.Interaction,user:discord.Member =None):
        BalanceEmbed = discord.Embed(title="Your wallet balance",colour=discord.Colour.random())
        BalanceEmbed.set_thumbnail(url="https://media.tenor.com/QMfaVm3kNy0AAAAi/moneda-girando-spinning.gif")
        if user is not None:
            user_id = user.id
            points = await find(user_id,1)
        else:
            user_id = interactions.user.id
            user = interactions.user
            points = await find(user_id,1)

        if type(points) == str:
            BalanceEmbed.description = f"{user.mention} hasnt participated in any games yet."
        else:
            BalanceEmbed.description = f"{user.mention}'s points ${points}" 
        await interactions.response.send_message(embed=BalanceEmbed)

async def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
async def award_points(user_id,username,points):
    if (await find(user_id)):
        await update_db(user_id=user_id,points=points)
    else:
        await create_db(user_id,username)
        await update_db(user_id=user_id,points=points)

async def setup(bot: commands.Bot):
    # print("Games is loaded")
    await bot.add_cog(Games(bot))