import discord
import os
from typing import Final
from discord.ext import commands
from discord import Client, Message
from dotenv import load_dotenv
from discord import app_commands
import slash_commands

load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


global strings
strings = ["hello","hi","yahallo","yo","yooo","good morning","good night","good afternoon","good evening","bye","goodbye","cya"]

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True  # Enable message events


bot = commands.Bot(command_prefix='+', intents=intents)

async def first_command(interaction):
    await interaction.response.send_message("Hello!")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync() #slash tree
        print(f"synced {len(synced)} command(s)")
    #syncing slash commands? something like that
    except Exception as e:
        print(e)

# slash command starts
@bot.tree.command(name = "hello",description='Just hello for programmers who loves to print Hello World')
async def hello(interaction: discord.Integration):
    await slash_commands.hello(interaction)

@bot.tree.command(name="slashgirls",description='Slashgirls? More like smashgirls; Generates random waifu image of your choice.')
@app_commands.choices(choices=[
    app_commands.Choice(name="Waifu", value="waifu"),
    app_commands.Choice(name="Neko", value="neko"),
    app_commands.Choice(name="Shinobu", value="shinobu"),
    app_commands.Choice(name="Megumin", value="megumin"),
]
)
async def slashgirls(interaction:discord.Integration,choices: app_commands.Choice[str]):
    await slash_commands.slashgirls(interaction,choices)

@bot.tree.command(name="rps",description='Feeling lucky? Try Rock/Paper/Scissors with Aiko.')
@app_commands.choices(choices=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
]
)
async def rps(interaction:discord.Integration,choices: app_commands.Choice[str]):
    await slash_commands.rps(interaction,choices)

#slash command ends

# Define event for when a message is received
@bot.event
async def on_message(message):
    # Check if the message starts with strings[]
    for string in strings:
        if ((message.content.startswith("?"))): # response in private 
                if message.author != bot.user:
                 await message.author.send(f"{message.content[1:]} {message.author.mention}!")
                 break


        elif message.content.lower().startswith(string): #in any channel
            if message.author != bot.user:
                await message.channel.send(f'{string.capitalize()} {message.author.mention}!')
            break
        # Send a response mentioning the user who sent the message
        


# Run the bot with your token
def main():
    bot.run(TOKEN)