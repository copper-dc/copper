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


class Aiko_Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask-aiko", description="Ask AI(Aiko's Intelligence)")
    async def ask_aiko(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer() 
        response = chat_session.send_message(prompt)
        geminiEmbed = discord.Embed(title="AI(Aiko's Intelligence) ", colour=discord.Colour.random())
        geminiEmbed.description = response.text
        geminiEmbed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThr7qrIazsvZwJuw-uZCtLzIjaAyVW_ZrlEQ&s")
        await interaction.followup.send(embed=geminiEmbed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Aiko_Gemini(bot))
