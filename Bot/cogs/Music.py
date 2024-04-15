import asyncio
import discord
from discord.ext import commands
from numpy import true_divide
import youtube_dl
from discord import FFmpegPCMAudio, app_commands
import sqlite3

vc = discord.VoiceClient

class Music(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.is_playing = False
        self.in_vc = False
        self.is_queue_empty = True
        self.music_queue = []

    @app_commands.command(name='play', description='plays music!')
    async def play_(self, interaction: discord.Interaction, url: str):
        self.is_playing = True
        self.in_vc = True
        
        title= await play_music(interaction,interaction.response,url)
        if title is not None:
            await interaction.followup.send(content=f"Now playing: {title}")
        while True:
            if vc.is_playing():
        # If the bot is playing something, continue waiting
                await asyncio.sleep(1)
            else:
        # If the bot is not playing anything, disconnect from the voice channel
                await vc.disconnect()
                break 
        
        
        
        @app_commands.command(name='pause', description='pauses/ resumes current track!')
        async def pause_music(self):
            pass

        @app_commands.command(name='next', description='skips to next track!')
        async def next_music(self):
            pass

        @app_commands.command(name='queue', description='list tracks!')
        async def show_queue(self):
            pass

    @app_commands.command(name='stop', description='stops current session!')
    async def stop_session(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if self.is_playing | self.in_vc:
            self.is_playing= False
            self.in_vc = False
            await voice_client.disconnect()
            await interaction.response.send_message(('oke'))
            await voice_client.cleanup()
        else:
            await interaction.response.send_message(('I am not in vc baka!'))

        @app_commands.command(name='fav', description='add the current track to favourites!')
        async def fav_music(self):
            pass

        @app_commands.command(name='resume', description='resumes current track!')
        async def resume_music(self):
            pass

        @app_commands.command(name='remove', description='removes the current track or given track!')
        async def remove_music(self):
            pass

        @app_commands.command(name='show fav', description='shows saved favs!')
        async def show_fav_music(self):
            pass

        @app_commands.command(name='play fav', description='plays fav music!')
        async def play_fav_music(self):
            pass

        @app_commands.command(name='pause', description='pauses/ resumes current track!')
        async def pause_music(self):
            pass

        @app_commands.command(name='del fav', description='delete a fav track!')
        async def delete_fav_music(self):
            pass

        @app_commands.command(name='now playing', description='info about current track!')
        async def now_playing(self):
            pass

        @app_commands.command(name='previous', description='plays previous track!')
        async def previous_music(self):
            pass

        @app_commands.command(name='clear queue', description='plays current track and clers queue!')
        async def pause_music(self):
            pass

music_var = Music(bot=commands.Bot(command_prefix='+', intents=discord.Intents.all()))


async def play_music(interaction: discord.Interaction,inter:discord.InteractionResponse, url: str):
    if interaction.user.voice:
        await inter.defer(thinking=True)
        voice_channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client:
            await voice_client.move_to(voice_channel)
        else:
            voice_client = await voice_channel.connect()

        ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
        }
        options = '-vn'
        before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            title = info["title"]

            audio_source = FFmpegPCMAudio(url2, options=options, before_options=before_options)
        
            voice_client.play(audio_source)
            
        return title
            
    else:
        await interaction.response.send_message(content="You are not connected to a voice channel.")

async def leave_empty(interaction:discord.Interaction):
    vc = interaction.guild.voice_client
    if not music_var.is_playing | music_var.in_vc:
                music_var.is_playing = False
                music_var.in_vc = False

                await vc.disconnect()
                
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))