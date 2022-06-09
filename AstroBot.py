############################# [ IMPORTS ] #############################

import os,discord
from discord import *
from discord.ext import commands
from dotenv import load_dotenv

############################# [ VARIABLES ] #############################

load_dotenv('token.env')  # Get the environment variables
astrobot = commands.Bot(command_prefix="$", description="AstoBot",intents=Intents.default())  # Create an instance of a bot with a command prefix
token = os.getenv('TOKEN')  # Get the token

astrobot.load_extension("cogs.ab")

############################# [ FUNCTIONS ] #############################
@astrobot.event
async def on_ready():  # Callback to announce the status of the bot
    print('\nAstroBot is ready !')
    print('-------------------')
    # Activity of the bot
    await astrobot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="M104 with naked eyes"))


############################# [ LAUNCH ] #############################

astrobot.run(token)
token.close()
