import asyncio
import threading
from time import sleep
import discord
from discord.ext import commands
from discord.ext.commands import bot
import os
from api.flask_api import run_api
from cron_jobs.cron import cron_wn8

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

token = os.environ.get('DSC_TOKEN')
# ffmpeg_executable = f"./ffmpeg/bin/ffmpeg.exe"
# mc = music_cog(bot, ffmpeg_executable)
# bot.add_cog(mc)


@bot.event
async def on_ready():
    bot.loop.create_task(cron_wn8(bot))
    print('Bot Started')


def run_bot():
    print("Bot Starting")
    bot.run(token)


if __name__ == "__main__":
    t = threading.Thread(target=run_api, args=(bot,))
    t.setDaemon(True)
    t.start()
    run_bot()
    print('test')
