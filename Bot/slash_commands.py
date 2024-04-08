import aiohttp
import discord
import random


# waifuBaseURL = "https://api.waifu.pics/"
# RPS = ['rock','paper','scissors']

# embedMessage = discord.Embed(colour=discord.Colour.random())

# try:
#     async def hello(interaction: discord.Interaction):
#         await interaction.response.send_message(f"Hey yo,{interaction.user.mention}")

#     async def slashgirls(interaction:discord.Integration, imgCategory: str, girltype: str):
#         slashgirlsEmbeds = discord.Embed(title="Enjoy your slash girl 🤤",colour=discord.Colour.random())
        
#         if (girltype== 'neko'):
#             imageCategory = "sfw" if imgCategory == "sfw" else "nsfw"
#             updatedURL = waifuBaseURL+imageCategory+"/neko"
#             data = await fetch_json(updatedURL)
#             imgurl = data['url']
#             slashgirlsEmbeds.set_image(url=imgurl)
#             await interaction.response.send_message(embed=slashgirlsEmbeds)
#         elif (girltype == 'waifu'):
#             imageCategory = "sfw" if imgCategory == "sfw" else "nsfw"
#             updatedURL = waifuBaseURL+imageCategory+"/waifu"
#             data = await fetch_json(updatedURL)
#             imgurl = data['url']
#             slashgirlsEmbeds.set_image(url=imgurl)
#             await interaction.response.send_message(embed=slashgirlsEmbeds)
#         elif (girltype=='megumin'):
#             try:
#                 imageCategory = "sfw" if imgCategory == "sfw" else "nsfw"
#                 updatedURL = waifuBaseURL+imageCategory+"/megumin"
#                 data = await fetch_json(updatedURL)
#                 imgurl = data['url']
#                 slashgirlsEmbeds.set_image(url=imgurl)
#                 await interaction.response.send_message(embed=slashgirlsEmbeds)
#             except Exception as e:
#                 await interaction.response.send_message("There is no NSFW image for megumin")
#         elif (girltype == 'shinobu'):
#             try:
#                 imageCategory = "sfw" if imgCategory == "sfw" else "nsfw"
#                 updatedURL = waifuBaseURL+imageCategory+"/shinobu"
#                 data = await fetch_json(updatedURL)
#                 imgurl = data['url']
#                 slashgirlsEmbeds.set_image(url=imgurl)
#                 await interaction.response.send_message(embed=slashgirlsEmbeds)
#             except Exception as e:
#                 await interaction.response.send_message("There is no NSFW image for shinobu")


# Games in Slash Commands
#  1. RPS (Rock, Paper and Scissors)
#  2. Gamble
#  3. Slot Machine
            
    # async def rps(interaction:discord.Interaction, choices: str):
    #     user_id = interaction.user.id
    #     username = interaction.user.name

    #     bot_choice = random.choice(RPS)
    #     if (choices.value == bot_choice):
    #         counter = 'That\'s a tie! Once more!!.'
    #         await interaction.response.send_message(f"{bot_choice}. {counter}")
    #     elif (choices.value == 'rock'):
    #         if bot_choice == 'paper':
    #             counter = 'Hehe, I win, Better luck next time~'
    #             await interaction.response.send_message(f"{bot_choice}. {counter}")
    #         else:
    #             counter = 'Aw... , Lucky you!📈'
    #             award_points(user_id,username,10)
    #             await interaction.response.send_message(f"{bot_choice}. {counter}")

    #     elif (choices.value == 'paper'):
    #         if bot_choice == 'scissors':
    #             counter = 'Hehe, I win, Better luck next time~'
    #             await interaction.response.send_message(f"{bot_choice}. {counter}")
    #         else:
    #             counter = 'Aw... , Lucky you!📈'
    #             award_points(user_id,username,1)
    #             await interaction.response.send_message(f"{bot_choice}. {counter}")

    #     elif (choices.value == 'scissors'):
    #         if bot_choice == 'rock':
    #             counter = 'Hehe, I win, Better luck next time~'
    #             await interaction.response.send_message(f"{bot_choice}. {counter}")
    #         else:
    #             counter = 'Aw... , Lucky you!📈'
    #             award_points(user_id,username,1)
    #             await interaction.response.send_message(f"{bot_choice}. {counter}")
        
            
    #     else:
    #         counter = 'Enter Valid Input Bozo'
    #         await interaction.response.send_message(counter)





    # async def say(interaction: discord.Interaction, describe: str):
    #     await interaction.response.send_message(f"{interaction.user.mention} said: `{describe}`")

# except discord.errors.NotFound:
#     print('Try again!')



# async def fetch_json(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.json()
#             return data