import logging
import time
import discord
from discord import ClientException
from youtube_dl import YoutubeDL
from youtube_dl.utils import UnsupportedError


class DiscordBot:
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

        ## Music bot options
        self.is_playing = False
        self.current_playlist = None # Just info
        self.priority_playlist = [] # []
        self.playlist_song_list = [] # [Song1, Song2...]
        self.current_playlist_index = 0
        self.current_guild = None
        self.current_voice_channel = None

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        discord.opus.load_opus("/usr/lib/libopus.so.0.8.0")

    def set_playlist(self, name, songs):
        self.stop_music()
        while self.is_playing:
            pass
        self.current_playlist = name
        self.playlist_song_list = songs
        self.play_music()

    def add_to_priority_queue(self, title, url, front=False):
        if front:
            self.priority_playlist.insert(0, [title, url])
        else:
            self.priority_playlist.append([title, url])

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                if "youtube.com" in item:
                    info = ydl.extract_info(item, download=False)
                else:
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                return {'source': info['formats'][0]['url'], 'title': info['title']}
            except UnsupportedError:
                return None

    async def connect_to_voice_channel_by_id(self, guild_id, voice_channel_id):
        self.current_guild = self.bot.get_guild(guild_id)
        self.current_voice_channel = self.current_guild.get_channel(voice_channel_id)
        await self.connect_to_voice_channel_by_object(self.current_voice_channel)

    async def connect_to_voice_channel_by_object(self, voice_channel):
        self.current_voice_channel = voice_channel
        self.current_voice_channel = voice_channel.guild

        if self.voice_client is not None:
            await self.voice_client.move_to(voice_channel)
        else:
            self.voice_client = await voice_channel.connect()

    def play_music(self):
        if len(self.playlist_song_list) == 0:
            self.is_playing = False
            return
        self.is_playing = True
        if len(self.priority_playlist) == 0:
            song = self.search_yt(
                self.playlist_song_list[self.current_playlist_index].url
            )
            self.current_playlist_index = (self.current_playlist_index + 1) % len(self.playlist_song_list)
        else:
            song_info = self.priority_playlist.pop(0)
            song = self.search_yt(song_info.url)
        if song is None:
            logging.warning("Error do loga na dsc? moze")
            return
        print("Robie cos")
        try:
            self.voice_client.play(discord.FFmpegPCMAudio(song['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_music())
        except ClientException:
            print("RIPDASKJDHSjkh")
            return

    def stop_music(self):
        self.current_playlist = "None"
        self.current_playlist_index = 0
        self.playlist_song_list = []
        self.voice_client.stop()

    def skip_music(self):
        self.voice_client.stop()
