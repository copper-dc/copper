import typing
import discord
from discord.ext import commands
from discord import app_commands
from g4f.client import Client


class Aiko_AI(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="ask_aiko",description="Ask aiko about anything...")
    async def Ask_Aiko(self,interaction:discord.Interaction, prompt: str):
        await interaction.response.defer(thinking=True)
        try:
            client = Client()
            full_prompt = f"Please respond in English. {prompt}"
            response =client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": full_prompt}],
            )
            await interaction.followup.send(content=response.choices[0].message.content)
        except discord.NotFound:
            await interaction.followup.send(content="Failed to send a response, the webhook is unknown or deleted.")
        except Exception as e:
            await interaction.followup.send(content=f"An error occurred: {str(e)}")
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Aiko_AI(bot))