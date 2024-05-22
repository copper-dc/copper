import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import wavelink


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_listener(self.on_ready, 'on_ready')  # Add on_ready listener

    async def on_ready(self):
        await self.start_lavalink()

    async def start_lavalink(self):
        node = await wavelink.NodePool.create_node(bot=self.bot,
                                                   host='127.0.0.1',
                                                   port=2333,
                                                   password='youshallnotpass')

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

    @app_commands.command(name="leave", description="Bot leaves the voice channel")
    async def leave(self, interaction: discord.Interaction):
        guild = interaction.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        if voice_client is None:
            await interaction.response.send_message("I am not in a voice channel.", ephemeral=True)
            return

        await voice_client.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel.", ephemeral=True)

    @app_commands.command(name="play", description="Play a song from a URL")
    async def play(self, interaction: discord.Interaction, url: str):
        player = self.get_player(interaction.guild)
        track = await wavelink.YouTubeTrack.search(query=url, return_first=True)

        if player.is_connected:
            await player.play(track)
            await interaction.response.send_message(f"Now playing: {track.title}", ephemeral=True)
        else:
            await interaction.response.send_message("I am not connected to a voice channel.", ephemeral=True)

    def get_player(self, guild: discord.Guild) -> wavelink.Player:
        return self.bot.wavelink.get_player(guild.id, cls=wavelink.Player)


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
