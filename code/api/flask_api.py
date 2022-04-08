from flask import Flask, jsonify, request
import json
import schedule

from bot import DiscordBot

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


@app.route("/music/play_playlist", methods=['GET'])
def post_music():
    global discord_bot
    playlist_name = request.args.get("playlist_name")
    songs = request.args.get("songs")
    print(playlist_name, songs)
    return "Done"


@app.route("/music/stop", methods=['GET'])
def post_music():
    global discord_bot
    print("stopping")
    # discord_bot.stop()
    return "Done"


@app.route("/music/add_priority", methods=['GET'])
def post_music():
    global discord_bot
    name = request.args.get("song_name")
    url = request.args.get("url")
    if url is None:
        pass
        # discord_bot.add_to_priority_queue(name, song)
    print(f"priority normal {name}, {url}")
    return "Done"


@app.route("/music/force_priority", methods=['GET'])
def post_music():
    global discord_bot
    name = request.args.get("song_name")
    url = request.args.get("url")
    if url is None:
        pass
    # discord_bot.stop()
    # discord_bot.add_to_priority_queue(name, song, True)
    print(f"priority force {name}, {url}")
    return "Done"


@app.route("/discord/jobs", methods=['GET'])
def get_jobs():
    all_jobs = schedule.get_jobs()
    return str(all_jobs)


def run_api(bot: DiscordBot):
    global discord_bot
    discord_bot = bot
    app.run(host="0.0.0.0", port=8080, debug=False)
