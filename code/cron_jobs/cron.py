import asyncio

from site_connector.api import mpsite_api


async def cron_wn8(bot, guild_id, channel_id):
    while True:
        guild = bot.get_guild(guild_id)
        text_channel = guild.get_channel(channel_id)
        mpsite_api.get_wn8()
        msg = ""
        for user, data in mpsite_api.get_wn8().items():
            msg += f'{user}\n'
            for tank in data:
                msg += f'            {tank.tank.tank_name} | WN8:'
                msg += f'{tank.wn8}\n'
        # print(msg)
        await text_channel.send(msg)
        await asyncio.sleep(6*60*60*60)
