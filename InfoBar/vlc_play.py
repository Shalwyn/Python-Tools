from vlc import EventType, Media, MediaPlayer, MediaParseFlag, Meta
import time

import subprocess

def play_vlc():  
    def _media_cb(event, *unused):
        # XXX callback ... never called
        print(event)
    
    media_player = MediaPlayer()
    media = Media("http://electrozombies.stream.laut.fm/electrozombies?pl=pls&t302=2021-09-16_10-57-42&uuid=3008b1dc-3852-4fab-9d7e-eaa375c80504")
    media_player.set_media(media)
    media_player.play()

    e = media_player.event_manager()
    e.event_attach(EventType.MediaMetaChanged, _media_cb, media)
    e.event_attach(EventType.MediaParsedChanged, _media_cb, media)

    meta = {Meta.Album: None,
        Meta.Genre: None,
        Meta.NowPlaying: None}

    while True:
        media.parse_with_options(MediaParseFlag.network, 2)
        for k in meta.keys():
            v = media.get_meta(k)
        if v != meta[k]:
            print("{}".format(v))
            notify = "Now Playing: " + v
            subprocess.Popen(['notify-send', notify])
            meta[k] = v
        time.sleep(2)
 
play_vlc()