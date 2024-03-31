import aiohttp
import discord
import random


waifuBaseURL = "https://api.waifu.pics/sfw/"
RPS = ['rock','paper','scissors']

try:
    async def hello(interaction: discord.Integration):
        await interaction.response.send_message(f"Hey yo,{interaction.user.mention}")


    # async def neko(interaction: discord.Integration):
    #     url = 'https://api.waifu.pics/sfw/neko'
    #     data = await fetch_json(url)
    #     url = data['url']
    #     await interaction.response.send_message(url)


    # async def waifu(interaction: discord.Integration):
    #     url = 'https://api.waifu.pics/sfw/waifu'
    #     data = await fetch_json(url)
    #     url = data['url']
    #     await interaction.response.send_message(url)


    # async def shinobu(interaction: discord.Integration):
    #     url = 'https://api.waifu.pics/sfw/shinobu'
    #     data = await fetch_json(url)
    #     url = data['url']
    #     await interaction.response.send_message(url)


    # async def megumin(interaction: discord.Integration):
    #     url = 'https://api.waifu.pics/sfw/megumin'
    #     data = await fetch_json(url)
    #     url = data['url']
    #     await interaction.response.send_message(url)
        
    async def slashgirls(interaction:discord.Integration, choices: str):
        if (choices.value == 'neko'):
            updatedURL = waifuBaseURL+"neko"
            data = await fetch_json(updatedURL)
            url = data['url']
            await interaction.response.send_message(url)
        elif (choices.value == 'waifu'):
            updatedURL = waifuBaseURL+"waifu"
            data = await fetch_json(updatedURL)
            url = data['url']
            await interaction.response.send_message(url)
        elif (choices.value=='megumin'):
            updatedURL = waifuBaseURL+"megumin"
            data = await fetch_json(updatedURL)
            url = data['url']
            await interaction.response.send_message(url)
        elif (choices.value == 'shinobu'):
            updatedURL = waifuBaseURL+"shinobu"
            data = await fetch_json(updatedURL)
            url = data['url']
            await interaction.response.send_message(url)
        await interaction.response.send_message("Haha, Enjoy your s(f)lash girl!")

    async def rps(interaction:discord.Integration, choices: str):
        bot_choice = random.choice(RPS)
        if (choices.value == bot_choice):
            counter = 'That\'s a tie! Once more!!.'
            await interaction.response.send_message(f"{bot_choice}. {counter}")
        elif (choices.value == 'rock'):
            if bot_choice == 'paper':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!'
                await interaction.response.send_message(f"{bot_choice}. {counter}")

        elif (choices.value == 'paper'):
            if bot_choice == 'scissors':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!'
                await interaction.response.send_message(f"{bot_choice}. {counter}")

        elif (choices.value == 'scissors'):
            if bot_choice == 'rock':
                counter = 'Hehe, I win, Better luck next time~'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
            else:
                counter = 'Aw... , Lucky you!'
                await interaction.response.send_message(f"{bot_choice}. {counter}")
        
            
        else:
            counter = 'Try again'
            await interaction.response.send_message(counter)


    async def say(interaction: discord.Integration, describe: str):
        await interaction.response.send_message(f"{interaction.user.mention} said: `{describe}`")

except discord.errors.NotFound:
    print('Try again!')



async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data