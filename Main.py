import discord
import os
from typing import Final
from discord.ext import commands
from discord import Client, Message
from dotenv import load_dotenv
from discord import app_commands



load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

global strings
strings = ["hello","hi","yahallo","yo","yooo","good morning","good night","good afternoon","good evening","bye","goodbye","cya"]

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True  # Enable message events

# Create a bot instance with intents
# bot: Client = Client(intents=intents) <- this or below one will do
bot = commands.Bot(command_prefix='/', intents=intents)
# tree = app_commands.CommandTree(bot)

# @tree.command(
#     name="hello",
#     description="My first application Command",
#     guild=discord.Object(id=12417128931)
# )
async def first_command(interaction):
    await interaction.response.send_message("Hello!")



# Define event for when the bot is ready
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
@bot.tree.command(name = "hello")
async def hello(interaction: discord.Integration):
    await interaction.response.send_message(f"Hey yo,{interaction.user.mention}")

@bot.tree.command(name = "say")
@app_commands.describe(describe = "What should i say?")
async def say(interaction: discord.Integration, describe: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{describe}`")

#slash command ends
# Define event for when a message is received
@bot.event
async def on_message(message):
    # Check if the message starts with strings[]
    for string in strings:
        if ((message.content.startswith("?"))): #private 
                if message.author != bot.user:
                 await message.author.send(f"{message.content} {message.author.mention}!")
                 break


        elif message.content.lower().startswith(string): #in any channel
            if message.author != bot.user:
                await message.channel.send(f'{string.capitalize()} {message.author.mention}!')
            break
        # Send a response mentioning the user who sent the message
        
        



        
        


# Run the bot with your token
bot.run(TOKEN)