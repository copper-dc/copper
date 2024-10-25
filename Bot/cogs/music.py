import discord
from discord import app_commands
from discord.ext import commands
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = Spotify(client_credentials_manager=credentials)

class music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="song-info",description="song info from spotify")
    async def searchtrack(self, interaction: discord.Interaction, track_name: str):
        """Fetches track info from Spotify."""
        results = spotify.search(q=track_name, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_info = (
            f"**{track['name']}** by {', '.join([artist['name'] for artist in track['artists']])}\n"
            f"Album: {track['album']['name']}\n"
            f"Release Date: {track['album']['release_date']}\n"
            f"[Listen here]({track['external_urls']['spotify']})"
        )
        await interaction.response.send_message(track_info)
    
    @app_commands.command(name="play",description="play tracks from spotify")
    async def play(self, interaction: discord.Interaction, track_name: str):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            
            results = spotify.search(q=track_name, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                await interaction.response.send_message(f"You can listen to **{track['name']}** by {', '.join([artist['name'] for artist in track['artists']])} here: {track['external_urls']['spotify']}")
            else:
                await interaction.response.send_message("Track not found.")
        else:
            await interaction.response.send_message("You need to be in a voice channel to use this command.")

    # @app_commands.command(name="leave",description="leave the music channel")
    # async def leave(interaction: discord.Interaction):
    #     """Disconnects the bot from the voice channel."""
    #     if interaction.guild.voice_client:
    #         await interaction.guild.voice_client.disconnect()
    #         await interaction.response.send_message("Disconnected from the voice channel.")
    #     else:
    #         await interaction.response.send_message("I'm not in a voice channel.")
        



        
async def setup(bot: commands.Bot):
    await bot.add_cog(music(bot))
