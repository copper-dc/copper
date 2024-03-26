import discord
from discord.ext import commands

global strings
strings = ["hello","hi","yahallo","yo","yooo","good morning","good night"]

# Define the intents your bot will use
intents = discord.Intents.default()
intents.messages = True  # Enable message events

# Create a bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define event for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Define event for when a message is received
@bot.event
async def on_message(message):
    # Check if the message starts with '!hello'
    for string in strings:
        if message.content.startswith(string):
            if message.author != bot.user:
                await message.channel.send(f'{string} {message.author.mention}!')
            break
        # Send a response mentioning the user who sent the message
        



# Run the bot with your token
bot.run('')