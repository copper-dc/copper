import discord
import os
from typing import Final
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# BARDTOKEN: Final[str] = os.getenv('GEMINI_TOKEN')


global strings
strings = ["hello","hi","yahallo","yo","yooo","good morning","good night","good afternoon","good evening","bye","goodbye","cya"]

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True  # Enable message events


bot = commands.Bot(command_prefix='+', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync() #slash tree
        print(f"synced {len(synced)} command(s)")
    #syncing slash commands? something like that
    except Exception as e:
        print(e)





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
        
async def load():
    for filename in os.listdir("../Bot/cogs"):
        if filename.endswith('.py'):
            print(f"loading {filename}")
            await bot.load_extension(f"cogs.{filename[:-3]}")





# Run the bot with your token
async def main():
    await load()
    await bot.start(TOKEN)
    