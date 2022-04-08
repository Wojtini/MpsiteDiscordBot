import threading
import discord
from discord.ext import commands
from discord.ext.commands import bot
import os
from api.flask_api import run_api
from bot import DiscordBot
from cron_jobs.cron import scheduler

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='^', intents=intents)

default_guild_id = 436894631578566676
default_voice_channel_id = 609423805726851129
default_music_url = "https://www.youtube.com/watch?v=se4U_LTeVAE"

DscBot = DiscordBot(bot)

@bot.event
async def on_ready():
    bot.loop.create_task(scheduler(DscBot))
    await DscBot.connect_to_voice_channel_by_id(default_guild_id, default_voice_channel_id)
    DscBot.play_music(default_music_url)
    print('Bot Started')


def run_bot():
    print("Bot Starting")
    token = os.environ.get('DSC_TOKEN')
    bot.run(token)


def run_flask_api():
    t = threading.Thread(target=run_api, args=(DscBot,))
    t.setDaemon(True)
    t.start()


if __name__ == "__main__":
    run_flask_api()
    run_bot()
