import asyncio
import requests
from site_connector.api import mpsite_api
import os
import logging
import schedule


async def cron_wn8_helper(bot):
    url = f"{os.environ.get('API_URL')}environmentvariables/?name=discordWOTCronChannel"
    r = requests.get(url)
    data = r.json()[0]

    guild_id = data['value']['gid']
    text_channel_id = data['value']['tcid']
    if guild_id and text_channel_id:
        guild_id = int(guild_id)
        text_channel_id = int(text_channel_id)

        guild = bot.get_guild(guild_id)
        text_channel = guild.get_channel(text_channel_id)

        mpsite_api.get_wn8()
        msg = ""
        for user, data in mpsite_api.get_wn8().items():
            msg += f'{user}\n'
            for tank in data:
                msg += f'            {tank.tank.tank_name} | WN8:'
                msg += f'{tank.wn8}\n'
        await text_channel.send(msg)
    else:
        logging.warning(f'Skipping WN8 discord update: Found no config on website {url}')


def create_task(bot, task):
    bot.loop.create_task(task(bot))


async def scheduler(bot):
    schedule.every(1).hours.do(create_task, bot=bot, task=cron_wn8_helper)

    while True:
        schedule.run_pending()
        await asyncio.sleep(10)
