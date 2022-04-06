from flask import Flask, jsonify
import json
app = Flask(__name__)
discord_bot = None


@app.route("/discord/guilds", methods=['GET'])
def get_guilds():
    global discord_bot
    result = []
    for guild in discord_bot.guilds:
        temp = {"gid": guild.id, "name": guild.name, "text_channels": []}
        for text_channel in discord_bot.get_guild(guild.id).text_channels:
            temp['text_channels'].append({
                "name": text_channel.name,
                "tcid": text_channel.id
            })
        result.append(temp)
    return json.dumps(result)


def run_api(bot):
    global discord_bot
    discord_bot = bot
    app.run(host="0.0.0.0", port=8080, debug=False)
