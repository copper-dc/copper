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

@bot.tree.command(name="neko",description='For furries- i mean catgril lovers; Generates random catgirl image')
async def neko(interaction: discord.Integration):
    await slash_commands.neko(interaction)

@bot.tree.command(name="waifu",description='Generates random waifu image.')
async def waifu(interaction: discord.Integration):
    await slash_commands.waifu(interaction)

@bot.tree.command(name="shinobu",description='For shinobu shrimps; Generates random shinobu image')
async def shinobu(interaction: discord.Integration):
    await slash_commands.shinobu(interaction)

@bot.tree.command(name="megumin",description='For megumin shrimps; Generates random megumin image')
async def megumin(interaction: discord.Integration):
    await slash_commands.megumin(interaction)

@bot.tree.command(name = "say",description='Say something for the world will ya')
@app_commands.describe(describe = "What should i say?")
async def say(interaction: discord.Integration, describe: str):
    await slash_commands.say(interaction)


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