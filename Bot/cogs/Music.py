import typing
import discord
from discord.ext import commands
from discord import app_commands



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name="join", description="Bot joins the voice channel")
    async def join(self, interaction: discord.Interaction):
        guild = interaction.guild
        voice_state = interaction.user.voice

        if voice_state is None or voice_state.channel is None:
            await interaction.response.send_message("You are not in a voice channel.", ephemeral=True)
            return

        channel = voice_state.channel

        if guild is None or channel is None:
            await interaction.response.send_message("Failed to join the voice channel.", ephemeral=True)
            return

        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice_client is not None:
            await voice_client.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message(f"Joined {channel.name}", ephemeral=True)
    
    
        
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))