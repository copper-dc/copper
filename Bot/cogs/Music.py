import asyncio
from code import interact
import discord
from discord.ext import commands
from discord import Interaction, app_commands
import requests
import yt_dlp as youtube_dl
from discord.ui import Button, View
import json
from collections import deque

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = deque() 

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

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: Music.ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                data = data['entries'][0]

            filename = data['url'] if stream else Music.ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **Music.ffmpeg_options), data=data)

    @app_commands.command(name="disconnect", description="Disconnect the bot from the voice channel")
    async def leave(self, interaction: discord.Interaction):
        guild = interaction.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        if voice_client is None:
            await interaction.response.send_message("I am not in a voice channel.", ephemeral=True)
            return

        await voice_client.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel.", ephemeral=True)

    @app_commands.command(name="play", description="Play a song from a YouTube URL")
    async def play(self, interaction: discord.Interaction, song: str):
        guild = interaction.guild
        voice_state = interaction.user.voice

        if voice_state is None or voice_state.channel is None:
            await interaction.response.send_message("You are not in a voice channel.")
            return

        channel = voice_state.channel

        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        if voice_client is None:
            await channel.connect()
            voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        await interaction.response.defer()

        try:
            async with interaction.channel.typing():
                song = song + " official audio"
                player = await self.YTDLSource.from_url(song, loop=self.bot.loop, stream=True)
                player.volume = 0.5  

                if voice_client.is_playing() or voice_client.is_paused():
                    self.queue.append(player)
                    queue_playerEmbed = discord.Embed(title = "Upcoming Songs")
                    queue_playerEmbed.description = "`"+player.title+"` is added to queue."
                    await interaction.followup.send(embed=queue_playerEmbed)

                else:
                    voice_client.play(player, after=lambda e: self.play_next(guild, voice_client))

                    play_embed = discord.Embed(title="Copper Music Box :notes:", color=discord.Colour.random())
                    play_embed.set_image(url="https://images.unsplash.com/photo-1634893661513-d6d1f579fc63?q=80&w=2128&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
                    play_embed.description = "Playing `" + player.title + "`"

                    with open('JSON/player_data.json', 'w') as file:
                        json.dump(player.data, file, indent=4)

                    followup_channel = self.bot.get_channel(interaction.channel_id)  
                    await followup_channel.send(embed=play_embed)

        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    def play_next(self, guild, voice_client):
        if len(self.queue) > 0:
            next_player = self.queue.popleft()

            async def play_next_song():
                voice_client.play(next_player, after=lambda e: self.play_next(guild, voice_client))

                play_embed = discord.Embed(title="Copper Music Box :notes:", color=discord.Colour.random())
                play_embed.set_image(url="https://images.unsplash.com/photo-1634893661513-d6d1f579fc63?q=80&w=2128&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
                play_embed.description = "Now playing `" + next_player.title + "`"

                with open('JSON/player_data.json', 'w') as file:
                    json.dump(next_player.data, file, indent=4)

                interaction = discord.Interaction
                followup_channel = self.bot.get_channel(interaction.channel_id)
                message = await followup_channel.send(embed=play_embed)

                while voice_client.is_playing() or voice_client.is_paused():
                    if voice_client.is_playing():
                        play_embed.description = "Now playing `" + next_player.title + "`"
                    elif voice_client.is_paused():
                        play_embed.description = "Paused `" + next_player.title + "`"

                    await message.edit(embed=play_embed)
                    await asyncio.sleep(5)  

            asyncio.run_coroutine_threadsafe(play_next_song(), self.bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop)


    @app_commands.command(name="lyrics", description="Get the lyrics of the song you want.")
    async def get_lyrics(self, interaction: discord.Interaction, artist: str, song: str):
        lyrics_embed = discord.Embed(title="Lyrics of " + song, colour=discord.Colour.random())
        URL = f"https://api.lyrics.ovh/v1/{artist}/{song}"
        response = requests.get(url=URL)
        data = response.json()
        if 'lyrics' not in data:
            await interaction.response.send_message("Lyrics not found.")
            return
        lyrics_embed.description = data['lyrics']
        await interaction.response.send_message(embed=lyrics_embed)

    async def send_play_message(self, embed):
        interaction = discord.Interaction
        followup_channel = self.bot.get_channel(interaction.channel_id)  
        await followup_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
