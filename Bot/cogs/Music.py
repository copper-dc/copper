import asyncio
import json
import logging
import discord
from discord.ext import commands
from discord import app_commands
import requests
import yt_dlp as youtube_dl
from discord.ui import Button, View

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currently_playing = {}
        self.queues = {}
        self.history = {}
        self.previous_song = {}
        self.artist_search = ""
        self.song_search = ""


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
            self.thumbnail = data.get('thumbnail', 'https://via.placeholder.com/150')

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: Music.ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                data = data['entries'][0]

            filename = data['url'] if stream else Music.ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **Music.ffmpeg_options), data=data)

    async def play_next(self, voice_client):
        guild = voice_client.guild
        queue = self.queues.get(guild.id, [])

        if queue:
            # Get and remove the next song from the queue
            song = queue.pop(0)
            player = await self.YTDLSource.from_url(song['url'], loop=self.bot.loop, stream=True)

            # Store the currently playing song as the previous song
            self.previous_song[guild.id] = self.currently_playing.get(guild.id, None)

            # Update currently playing song
            self.currently_playing[guild.id] = song
            self.history[guild.id] = song

            # Create new embed with song info
            play_embed = discord.Embed(title="Now Playing :notes:", color=discord.Colour.random())
            play_embed.description = f" `{player.title}` \nRequested by {song['requester'].mention}"

            # Create and set buttons for new song
            buttons = self.create_buttons(guild.id)
            message = await voice_client.channel.send(embed=play_embed, view=buttons)
            self.currently_playing[guild.id]['message_id'] = message.id
            
            # Play the new song
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(voice_client), self.bot.loop).result())
        else:
            self.currently_playing[guild.id] = None
            await voice_client.disconnect()
            await voice_client.channel.send("Queue has ended. Session closed.")

    def create_buttons(self, guild_id):

        pause_button_icon = "▐▐ "  # Pause emoji
        play_button_icon = "▶"   # Play emoji
        forward_button_icon = "▶▶"  # Forward emoji
        backward_button_icon = "◀◀" # Backward emoji
        stop_button_icon = "◼"   # Stop emoji
        info_button_icon = "🛈"  # Info emoji
        queue_button_icon = "☰" # Queue emoji

        pause_button = Button(label=pause_button_icon, style=discord.ButtonStyle.green)
        skip_button = Button(label=forward_button_icon, style=discord.ButtonStyle.blurple)
        stop_button = Button(label=stop_button_icon, style=discord.ButtonStyle.red)
        info_button = Button(label=info_button_icon, style=discord.ButtonStyle.gray)
        prev_button = Button(label=backward_button_icon, style=discord.ButtonStyle.blurple)
        queue_button = Button(label=queue_button_icon, style=discord.ButtonStyle.green)
        lyrics_button = Button(label="Lyrics", style=discord.ButtonStyle.green)

        async def pause_callback(interaction: discord.Interaction):
            voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            if voice_client.is_playing():
                voice_client.pause()
                pause_button.label = pause_button_icon
                pause_button.style = discord.ButtonStyle.red
            elif voice_client.is_paused():
                voice_client.resume()
                pause_button.label = play_button_icon
                pause_button.style = discord.ButtonStyle.green
            await interaction.response.edit_message(view=self.create_buttons(guild_id))

        async def skip_callback(interaction: discord.Interaction):
            voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            voice_client.stop()
            await interaction.response.edit_message(view=self.create_buttons(guild_id))

        async def stop_callback(interaction: discord.Interaction):
            guild = interaction.guild
            voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
            if voice_client:
                self.queues[guild.id] = []
                voice_client.stop()
                await voice_client.disconnect()
                await interaction.response.send_message("Stopped playing and cleared the queue.")
                await interaction.channel.send("Session ended. Queue has been cleared.")
            else:
                await interaction.response.send_message("No song is currently playing.")

        async def info_callback(interaction: discord.Interaction):
            song_info = self.currently_playing.get(interaction.guild.id, None)
            if song_info:
                info_embed = discord.Embed(title="Currently Playing", color=discord.Colour.blue())
                info_embed.set_thumbnail(url=song_info["thumbnail"])
                info_embed.description = f"**Title:** {song_info['title']}\n**Requested by:** {song_info['requester'].mention}"
                await interaction.response.send_message(embed=info_embed, ephemeral=True)
            else:
                await interaction.response.send_message("No song is currently playing.", ephemeral=True)

        async def prev_callback(interaction: discord.Interaction):
            guild = interaction.guild
            voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
            prev_song = self.previous_song.get(guild.id)
            if prev_song:
                self.queues[guild.id].insert(0, prev_song)
                voice_client.stop()
                await interaction.response.send_message("Playing the previous song.", ephemeral=True)
            else:
                await interaction.response.send_message("No previous song to play.", ephemeral=True)

        async def queue_callback(interaction: discord.Interaction):
            queue = self.queues.get(interaction.guild.id, [])
            if queue:
                queue_embed = discord.Embed(title="Song Queue", color=discord.Colour.green())
                for idx, song in enumerate(queue, 1):
                    queue_embed.add_field(name=f"{idx} - ", value="`"+song['title']+"`", inline=False)
                await interaction.response.send_message(embed=queue_embed)
            else:
                await interaction.response.send_message("The queue is currently empty.")

        async def lyrics_callback(interaction: discord.Interaction):
            try:
                with open("JSON/playerdata.json", 'r') as file:
                    player_data = json.load(file)

                artist = player_data.get('uploader', 'Unknown Artist')

                if self.artist_search == "":
                    artist = self.artist_search
                
                song = self.song_search
                
                lyricsEmbed = discord.Embed(title=f"Lyrics of {song} :notes:", colour=discord.Colour.random())

                URL = f"https://api.lyrics.ovh/v1/{artist}/{song}"
                response = requests.get(url=URL)
                data = response.json()

                if 'lyrics' not in data:
                    await interaction.response.send_message("Lyrics not found")
                    return
                
                lyricsEmbed.description = data['lyrics']
                await interaction.response.send_message(embed=lyricsEmbed)
            
            except FileNotFoundError:
                print(f"Error: Could not find file 'playerdata.json'")
            except json.JSONDecodeError:
                print("Error: Could not decode JSON from the file")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            

        pause_button.callback = pause_callback
        skip_button.callback = skip_callback
        stop_button.callback = stop_callback
        info_button.callback = info_callback
        prev_button.callback = prev_callback
        queue_button.callback = queue_callback
        lyrics_button.callback = lyrics_callback

        view = View()
        view.add_item(info_button)
        view.add_item(prev_button)
        view.add_item(pause_button)
        view.add_item(skip_button)
        view.add_item(stop_button)
        view.add_item(queue_button)
        view.add_item(lyrics_button)
        return view

    @app_commands.command(name="play", description="Play a song from a YouTube URL")
    async def play(self, interaction: discord.Interaction, song: str, artist: str=None):
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

        try:
            await interaction.response.defer()

            async with interaction.channel.typing():
                if artist:
                    self.artist_search = artist
                    self.song_search = song
                    song_query = song + " by "+ artist+" official audio"
                else:
                    self.song_search = song
                    song_query = song + " official audio"
                # Extract song info
                player = await self.YTDLSource.from_url(song_query, loop=self.bot.loop, stream=True)

                # Store the currently playing song
                song_info = {
                    'title': player.title,
                    'url': player.url,
                    'thumbnail': player.thumbnail,
                    'requester': interaction.user
                }
                self.currently_playing[guild.id] = song_info
                with open('JSON/playerdata.json', 'w') as file:
                    json.dump(player.data, file, indent=4)

                # Add the song to the queue
                if voice_client.is_playing():
                    self.queues.setdefault(guild.id, []).append(song_info)
                    queuEmbed = discord.Embed(title="Song Queued", color=discord.Colour.green())
                    queuEmbed.description = f"`{player.title}` added to the queue."
                    await interaction.followup.send(embed=queuEmbed)
                else:
                    # Start playing the song
                    voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(voice_client), self.bot.loop).result())
                    
                    # Create and send embed for the currently playing song
                    play_embed = discord.Embed(title="Now Playing :notes:", color=discord.Colour.random())
                    play_embed.description = f"` {player.title}` \nRequested by {interaction.user.mention}"
                    
                    message = await interaction.followup.send(embed=play_embed)
                    self.currently_playing[guild.id]['message_id'] = message.id

        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    @app_commands.command(name="player-panel", description="Show the currently playing song")
    async def nowplaying(self, interaction: discord.Interaction):
        try:
            logging.info(f"Received 'player-panel' command from {interaction.user} in guild {interaction.guild.name}")

            guild = interaction.guild
            song_info = self.currently_playing.get(guild.id, None)

            if song_info:
                logging.info(f"Currently playing song found: {song_info['title']}")

                now_playing_embed = discord.Embed(title="Currently Playing", color=discord.Colour.blue())
                now_playing_embed.description = f"**Title:** {song_info['title']}\n**Requested by:** {song_info['requester'].mention}"
                now_playing_embed.set_image(url="https://cdn.dribbble.com/users/1770290/screenshots/6164788/bg_76.gif")
                buttons = self.create_buttons(guild.id)

                await interaction.response.send_message(embed=now_playing_embed, view=buttons)
                logging.info("Successfully sent 'Currently Playing' message")
            else:
                logging.warning("No song is currently playing.")
                await interaction.response.send_message("No song is currently playing.")
        except Exception as e:
            logging.error(f"An error occurred in 'player-panel' command: {e}")
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)


    @app_commands.command(name="queue", description="Show the current song queue")
    async def queue(self, interaction: discord.Interaction):
        guild = interaction.guild
        queue = self.queues.get(guild.id, [])

        if queue:
            queue_embed = discord.Embed(title="Song Queue", color=discord.Colour.green())
            for idx, song in enumerate(queue, 1):
                title = song['title'][:12] + '...' if len(song['title']) > 12 else song['title']
                queue_embed.add_field(name=f" `{idx}` - `{title}`", value=f"Requested by {song['requester'].mention}", inline=False)
            await interaction.response.send_message(embed=queue_embed)
        else:
            await interaction.response.send_message("The queue is currently empty.")

    @app_commands.command(name="stop", description="Stop the currently playing song and clear the queue")
    async def stop(self, interaction: discord.Interaction):
        guild = interaction.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)

        if voice_client:
            self.queues[guild.id] = []
            voice_client.stop()
            await voice_client.disconnect()
            await interaction.response.send_message("Stopped playing and cleared the queue.")
            await interaction.channel.send("Session ended. Queue has been cleared.")
        else:
            await interaction.response.send_message("No song is currently playing.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
