import os
import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
    ]
)


class Copper_Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask-copper", description="Ask AI(copper's Intelligence)")
    async def ask_copper(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer() 
        response = chat_session.send_message(prompt)
        geminiEmbed = discord.Embed(title="AI(copper's Intelligence) ", colour=discord.Colour.random())
        geminiEmbed.description = response.text
        await interaction.followup.send(embed=geminiEmbed)
    
    @app_commands.command(name="reset-copper", description="Reset AI(copper's Intelligence)")
    @app_commands.AppCommandPermissions(guild=[app_commands.PermissionType.administrator])
    async def reset_copper(self, interaction: discord.Interaction):
        chat_session.reset()
        await interaction.response.send_message("AI(copper's Intelligence) has been reset")
        print("AI(copper's Intelligence) has been reset")

async def setup(bot: commands.Bot):
    await bot.add_cog(Copper_Gemini(bot))
