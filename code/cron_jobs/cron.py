import asyncio
import requests
from site_connector.api import mpsite_api
import os
import logging


async def cron_wn8(bot):
    while True:
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
            # print(msg)
            await text_channel.send(msg)
        else:
            logging.warning(f'Skipping WN8 discord update: Found no config on website {url}')
        await asyncio.sleep(6*60*60)
