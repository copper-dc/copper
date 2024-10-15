import discord
from discord.ext import commands
from discord import app_commands

class Setup_User_Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup-profile", description="testing modals")
    async def choose(self, interaction: discord.Interaction):
        modal = NameModal()
        await interaction.response.send_modal(modal)

class NameModal(discord.ui.Modal, title="Enter your name"):
    name_input = discord.ui.TextInput(label="Name", placeholder="Enter your name")

    async def on_submit(self, interaction: discord.Interaction):
        view = MyView(name=self.name_input.value)
        await interaction.response.send_message("Please choose a gender:", view=view)

class MyView(discord.ui.View):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @discord.ui.select(
        placeholder="Gender",
        options=[
            discord.SelectOption(label="Male", value="Male"),
            discord.SelectOption(label="Female", value="Female"),
        ],
        row=1
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.gender = select.values[0]

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary)
    async def submit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Acknowledge the interaction
        await interaction.response.defer()  # Acknowledge the interaction
        
        gender = getattr(self, 'gender', 'Not selected')  # Default if no gender selected
        
        # Send a follow-up message with the submitted information
        await interaction.followup.send(f"Submitted! Name: {self.name}, Gender: {gender}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup_User_Profile(bot))
