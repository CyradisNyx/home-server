"""Defines views and routes for app."""

from airplay import AirPlay
from flask import render_template
from flask import request
import glob2
from homeserver import app
import os
import subprocess
from threading import Thread


def transcode(path):
    """Transmux videos into mp4."""
    if os.path.isfile(app.config['TEMP_DIR'] + "converted.mp4"):
        os.remove(app.config['TEMP_DIR'] + "converted.mp4")
    return subprocess.call(("avconv -loglevel quiet -i " +
                            path +
                            " -vcodec copy -acodec copy -scodec copy -f mp4 " +
                            app.config['TEMP_DIR'] +
                            "converted.mp4"), shell=True)


def airplay_background(video):
    """Stream videos to Airplay device."""
    ap = AirPlay('10.0.0.22')
    if video[-4:] != ".mp4":
        transcode(app.config['FILES_DIR'] + video)
        video = 'temp/converted.mp4'
    print(ap.play(app.config['MEDIA_URL'] + video))
    print(ap.playback_info())
    while True:
        for ev in ap.events(block=False):
            newstate = ev.get('state', None)
            if newstate == 'stopped':
                return


def localplay(video):
    """Stream videos to client device."""
    if video[-4:] != ".mp4":
        transcode(app.config['FILES_DIR'] + video)
        video = 'temp/converted.mp4'
    return (app.config['MEDIA_URL'] + video)


@app.route('/')
@app.route('/home')
def home():
    """Route for homepage."""
    return render_template('home.html')


@app.route('/movies')
def movies():
    """List movies available."""
    MovieTypes = ('.mkv', '.avi', '.mp4')
    movies = glob2.glob(app.config['FILES_DIR'] + '/**/*.*')
    movies = [movie.rsplit("/", 1)[-1]
              for movie in movies
              if movie.endswith(MovieTypes) and ("/temp/") not in movie]
    print(movies)
    return render_template('movies.html', movies=movies)


@app.route('/play')
def play():
    """Play movie on Airplay Device."""
    video = request.args.get('video', '')
    video_thread = Thread(target=airplay_background, args=(video, ))
    video_thread.start()
    return render_template('play.html', video=video)


@app.route('/playlocal')
def playlocal():
    """Play movie on client device."""
    video = request.args.get('video', '')
    url = localplay(video)
    print(url)
    return render_template('playlocal.html', url=url, video=video)
