import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import bot
import os
from cron_jobs.cron import cron_wn8
from site_connector.api import mpsite_api

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

# os.environ.get('POSTGRES_NAME')
token = os.environ.get('DSC_TOKEN')
guild_id = int(os.environ.get('GUILD_ID'))
channel_id = int(os.environ.get('CHANNEL_ID'))


@bot.event
async def on_ready():
    bot.loop.create_task(cron_wn8(bot, guild_id, channel_id))
    print('Bot Started')

if __name__ == "__main__":
    print("Bot Starting")
    bot.run(token)
