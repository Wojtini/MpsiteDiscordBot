# Mile pogawedki - Discord bot
Discord bot that connects to MPSite (https://github.com/Wojtini/MpsiteDocker)
and does stuff on discord based on it:
### Current bot jobs
cron job - displaying wn8 every n hours (improving)
### Current endpoints
/discord/guilds - guilds and text_channels the bot is connected on discord

/discord/join_vc - connects to given voice channel
data:
   guild_id: int - guild id
   vc_id: int - voice channel id

/music/play_playlist - plays playlist given in data
data:
   playlist_name: str,
   songs: [{"name": str, "url": str}, {"name": str, "url": str}]
disclaimer:
url might be also a search query but results can vary over time

/music/stop - clears queue and stops music completly

/music/skip - skips current song in active playlist

/music/add_priority - adds song to the end of priority queue
  song_name: str,
  url: str,
  
/music/force_priority - same as above but add in the front of priority queue

/discord/jobs - returns current cron jobs
