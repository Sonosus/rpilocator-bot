import os
import discord
from discord.utils import get
from dotenv import load_dotenv

# load discord token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# initialize discord client
client = discord.Client()


@client.event
async def on_ready():
    global ping_role, ping_channel
    print('We have logged in as {0.user}'.format(client))
    guild = client.guilds[0]
    ping_role = get(guild.roles, name="RPi Pings")
    ping_channel = get(guild.channels, name="rpi-locator")

@client.event
async def on_message(message):
    channel = message.channel
    
    # make sure we're not responding to the bot's message
    if message.author == client.user:
        return
    
    # make sure we're posting in the right channel
    if channel == ping_channel:
        await channel.send(f"See the post above! {ping_role.mention}")

# connect to discord
client.run(DISCORD_TOKEN)
