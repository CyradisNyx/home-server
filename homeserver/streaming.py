"""Defines Functions for Streaming (Airplay, Transcoding, etc)."""

from airplay import AirPlay
from homeserver import app
import os
import subprocess


def transcode(path):
    """
    Transmux videos into mp4.

    Check if temp converted file already exists (using temp to seed back),
    and delete. Call shell subprocess, using ffmpeg to remux into mp4 container
    At the moment, it's not using a temp directory, to save space on my
    harddrive, however, it's fairly easy to re-implement. Change the subprocess
    call to save to app.config['TEMP_DIR'] + converted.mp4, like in the check.

    @str path: Path to Video File (abspath? file name?)

    @return none
    """
    if os.path.isfile(app.config['TEMP_DIR'] + "converted.mp4"):
        os.remove(app.config['TEMP_DIR'] + "converted.mp4")
    subprocess.call(("ffmpeg -i " +
                    path + " -vcodec copy -acodec copy -scodec copy -f mp4 " +
                    path[0:-3] + "mp4 && rm " + path), shell=True)
    return


def airplay_background(video):
    """
    Stream videos to Airplay device. MAYBE DOESNT WORK ANYMORE BECAUSE DB!!!!!.

    Currently hardcoding the AirPlay IP, rather than finding it dynamically.
    Check if transmuxing is required, if so, call transcode(). If using
    TEMP_DIR in transmuxing, make sure video is changed to that path. Play
    using MEDIA_URL. While loop to check for any device interferences, since
    it's running in a background thread.

    @str video: Path to Video File (abspath? file name?)

    @return none
    """
    ap = AirPlay('10.0.0.22')
    if video[-4:] != ".mp4":
        transcode(video)
        video = video.replace(video[-4:], ".mp4")
    print(ap.play(app.config['MEDIA_URL'] + video))
    print(ap.playback_info())
    while True:
        for ev in ap.events(block=False):
            newstate = ev.get('state', None)
            if newstate == 'stopped':
                return


def localplay(video):
    """
    Get Video URL for Localplay.

    Split file abspath into path from FILES_DIR, and tack that onto MEDIA_URL.

    @str video: Abspath for video file

    @return URL for video
    """
    video = video.split(app.config['FILES_DIR'], 1)[1]
    return (app.config['MEDIA_URL'] + video)
