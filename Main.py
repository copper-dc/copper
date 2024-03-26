import discord
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable the message intent

# Define the command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Define a simple command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello! I am a Discord bot.')

# Run the bot with your token
bot.run("")
