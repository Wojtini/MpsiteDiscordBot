from flask import Flask, jsonify, request
import json
import schedule

from bot import DiscordBot

from song import Song

app = Flask(__name__)
discord_bot: DiscordBot


@app.route("/discord/guilds", methods=['GET'])
def get_guilds():
    global discord_bot
    result = []
    for guild in discord_bot.bot.guilds:
        temp = {"gid": guild.id, "name": guild.name, "text_channels": []}
        for text_channel in discord_bot.bot.get_guild(guild.id).text_channels:
            temp['text_channels'].append({
                "name": text_channel.name,
                "tcid": text_channel.id
            })
        result.append(temp)
    return json.dumps(result)


@app.route("/discord/join_vc", methods=['PUT'])
def join_vc():
    global discord_bot
    if request.method == 'PUT':
        data = json.loads(request.get_json())
        guild_id = data["guild_id"]
        vc_id = data["vc_id"]
        discord_bot.connect_to_voice_channel_by_id(guild_id=guild_id, vc_id=vc_id)
        return "Done"


@app.route("/music/play_playlist", methods=['PUT'])
def post_music():
    global discord_bot
    if request.method == 'PUT':
        data = json.loads(request.get_json())
        playlist_name = data["playlist_name"]
        songs = data["songs"]
        final_songs = []
        for song in songs:
            final_songs.append(Song(name=song['name'], url=song['url']))
        discord_bot.set_playlist(playlist_name, final_songs)
        return "Done"


@app.route("/music/stop", methods=['GET', 'PATCH'])
def stop_music():
    global discord_bot
    discord_bot.stop_music()
    return "Done"


@app.route("/music/skip", methods=['GET', 'PATCH'])
def skip_music():
    global discord_bot
    discord_bot.skip_music()
    return "Done"


@app.route("/music/add_priority", methods=['PUT'])
def add_priority():
    global discord_bot
    if request.method == 'PUT':
        data = json.loads(request.get_json())
        name = data("song_name")
        url = data("url")
        discord_bot.add_to_priority_queue(name, url)
        return "Done"


@app.route("/music/force_priority", methods=['GET'])
def force_priority():
    global discord_bot
    if request.method == 'PUT':
        data = json.loads(request.get_json())
        name = data("song_name")
        url = data("url")
        discord_bot.add_to_priority_queue(name, url, front=True)
        return "Done"


@app.route("/discord/jobs", methods=['GET'])
def get_jobs():
    all_jobs = schedule.get_jobs()
    return str(all_jobs)


def run_api(bot: DiscordBot):
    global discord_bot
    discord_bot = bot
    app.run(host="0.0.0.0", port=8080, debug=False)
