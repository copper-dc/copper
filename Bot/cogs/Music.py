import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import requests
import yt_dlp as youtube_dl
from discord.ui import Button, View
from googletrans import Translator

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

    @app_commands.command(name="disconnect", description="Disconnect the bot from the voice channel")
    async def leave(self, interaction: discord.Interaction):
        guild = interaction.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        if voice_client is None:
            await interaction.response.send_message("I am not in a voice channel.", ephemeral=True)
            return

        await voice_client.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel.", ephemeral=True)

    @app_commands.command(name="lyrics", description="get lyrics of the song you want")
    async def get_lyrics(self, interaction: discord.Interaction, artist: str, song: str):
        base_lyrics_url = "https://api.lyrics.ovh/v1/"+artist+"/"+song
        response = requests.get(base_lyrics_url)
        data = response.json()
        lyrics = data.get("lyrics","")
        first_line = lyrics.split('\n')[0]

        main_line = ""
        for i in lyrics[1:]:
            main_line+=i
        translator = Translator()


        first_line_translated = translator.translate(first_line, src='fr', dest='en').text

        lyricsEmbed = discord.Embed(title=first_line_translated,colour=discord.Colour.random())

        lyricsEmbed.description = main_line
        await interaction.response.send_message(embed=lyricsEmbed)

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

        await interaction.response.defer()  # Defer the response to avoid timeout

        try:
            async with interaction.channel.typing():
                player = await self.YTDLSource.from_url(song, loop=self.bot.loop, stream=True)
                voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

            # Create the embed with the music info
            play_embed = discord.Embed(title="Now Playing :notes:", color=discord.Colour.random())
            play_embed.set_thumbnail(url="https://media.tenor.com/ZViDCL9tx_QAAAAi/set-diet-sound-bars.gif")
            play_embed.set_image(url=player.thumbnail)
            play_embed.description = "*** " + player.title + " ***"

            # Create buttons for pause and resume
            pause_button = Button(label="❚❚", style=discord.ButtonStyle.green)
            
            async def pause_callback(interaction: discord.Interaction):
                if voice_client.is_playing():
                    voice_client.pause()
                    pause_button.label = "▶"
                    pause_button.style = discord.ButtonStyle.red
                    
                elif voice_client.is_paused():
                    voice_client.resume()
                    pause_button.label = "❚❚"
                    pause_button.style = discord.ButtonStyle.green
                
                await interaction.response.edit_message(view=view)
                    
            pause_button.callback = pause_callback

            
            view = View()
            view.add_item(pause_button)
            

            await interaction.followup.send(embed=play_embed, view=view)  # Send follow-up message
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
