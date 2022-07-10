import os
import logging
import discord
from discord.utils import get
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# load discord token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# initialize discord client
client = discord.Client()


@client.event
async def on_ready():
    global ping_role, ping_channel, once_channel
    logging.info('We have logged in as {0.user}'.format(client))
    guild = client.guilds[0]
    ping_role = get(guild.roles, name="RPi Pings")
    ping_channel = get(guild.channels, name="rpi-locator")
    once_channel = get(guild.channels, name="listing")
    logging.info(f"Guild is {guild}")
    logging.info(f"Role to ping is {ping_role}")
    logging.info(f"Channel to monitor is {ping_channel}")

@client.event
async def on_message(message):
    channel = message.channel
    author = message.author
    
    # make sure we're not responding to the bot's message
    if author == client.user:
        return
    
    # make sure we're posting in the right channel
    if channel == ping_channel:
        await channel.send(f"See the post above! {ping_role.mention}")
    
    if channel == once_channel:
        perms = channel.overwrites_for(author)
        perms.send_messages = False
        await channel.set_permissions(member, overwrite=perms, reason="One post per person!")

# connect to discord
client.run(DISCORD_TOKEN)
