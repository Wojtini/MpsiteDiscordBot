# Mile pogawedki - Discord bot
Discord bot that connects to MPSite (https://github.com/Wojtini/MpsiteDocker)
and does stuff on discord based on it:
### Current bot jobs
cron job - displaying wn8 every n hours (improving)
### Current endpoints
/discord/guilds - guilds and text_channels the bot is connected on discord<br /><br />

/discord/join_vc - connects to given voice channel<br />
data:<br />
   guild_id: int - guild id<br />
   vc_id: int - voice channel id<br /><br />

/music/play_playlist - plays playlist given in data<br />
data:<br />
   playlist_name: str,<br />
   songs: [{"name": str, "url": str}, {"name": str, "url": str}]<br />
disclaimer:<br />
url might be also a search query but results can vary over time<br /><br />

/music/stop - clears queue and stops music completly<br /><br />

/music/skip - skips current song in active playlist<br /><br />

/music/add_priority - adds song to the end of priority queue<br />
  song_name: str,<br />
  url: str,<br /><br />
  
/music/force_priority - same as above but add in the front of priority queue<br /><br />

/discord/jobs - returns current cron jobs<br /><br />
