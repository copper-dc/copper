from io import BytesIO

import PyPDF2
import discord
import ollama
import requests
from discord import app_commands
from discord.ext import commands


class copperllama(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="ask_copper", description="ask llama model")
    async def askllama(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        llamaEmbed = discord.Embed(title="Llama's Response 🐐", colour=discord.Colour.random())
        response = ollama.chat(model='copper:1b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        llamaEmbed.description = response['message']['content']

        await interaction.followup.send(embed=llamaEmbed)

    @app_commands.command(name="summarize_file", description="Summarize docs and pdf using llama3.2:1b")
    async def summarizefile(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()
        if not file.filename.endswith('.pdf'):
            await interaction.response.send_message("Please upload a valid PDF file.", ephemeral=True)
            return
        file_bytes = await file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))

        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()


        prompt = f"Summarize the following content:\n{pdf_text}"
        response = ollama.chat(model='copper:1b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        summary = response['message']['content']

        llamaEmbed = discord.Embed(
            title="Summary of " + file.filename,
            description=summary,
            colour=discord.Colour.random()
        )

        await interaction.followup.send(embed=llamaEmbed)



async def setup(bot: commands.Bot):
    await bot.add_cog(copperllama(bot))