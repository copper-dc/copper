import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = data.get('url')
            self.thumbnail = data.get('thumbnail', 'https://via.placeholder.com/150')  # Default thumbnail if not present

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: Music.ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                data = data['entries'][0]

            filename = data['url'] if stream else Music.ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **Music.ffmpeg_options), data=data)

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

    @app_commands.command(name="play", description="Play a song from a YouTube URL")
    async def play(self, interaction: discord.Interaction, url: str):
        guild = interaction.guild
        voice_state = interaction.user.voice

        if voice_state is None or voice_state.channel is None:
            await interaction.response.send_message("You are not in a voice channel.", ephemeral=True)
            return

        channel = voice_state.channel

        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice_client is None:
            await channel.connect()
            voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        await interaction.response.defer(ephemeral=True)  # Defer the response to avoid timeout

        async with interaction.channel.typing():
            player = await self.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        playEmbed = discord.Embed(title="Now Playing :notes:", color=discord.Colour.random())
        playEmbed.set_thumbnail(url="https://media.tenor.com/g2q5VyGBJPcAAAAi/musica-music.gif")
        playEmbed.description = "*** " + player.title + " ***"
        await interaction.followup.send(embed=playEmbed, ephemeral=True)  

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
