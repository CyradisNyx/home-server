"""Defines Functions for Streaming (Airplay, Transcoding, etc)."""

from airplay import AirPlay
from homeserver import app
import os
import subprocess


def transcode(path):
    """Transmux videos into mp4."""
    if os.path.isfile(app.config['TEMP_DIR'] + "converted.mp4"):
        os.remove(app.config['TEMP_DIR'] + "converted.mp4")
    subprocess.call(("ffmpeg -i " +
                    path + " -vcodec copy -acodec copy -scodec copy -f mp4 " +
                    path[0:-3] + "mp4"), shell=True)  # && rm + path if needed
    return


def airplay_background(video):
    """Stream videos to Airplay device."""
    ap = AirPlay('10.0.0.22')
    if video[-4:] != ".mp4":
        transcode(video)
    print(ap.play(app.config['MEDIA_URL'] + "temp/converted.mp4"))
    print(ap.playback_info())
    while True:
        for ev in ap.events(block=False):
            newstate = ev.get('state', None)
            if newstate == 'stopped':
                return


def localplay(video):
    """Stream videos to client device."""
    if video[-4:] != ".mp4":
        transcode(video)
        video = video.replace(video[-4:], ".mp4")
    video = video.split(app.config['FILES_DIR'], 1)[1]
    return (app.config['MEDIA_URL'] + video)
