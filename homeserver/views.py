from flask import *
from . import app
from threading import Thread
from airplay import AirPlay
import os, glob, subprocess

def transcode(path):
    if os.path.isfile(app.config['TEMP_DIR'] + "converted.mp4"):
        os.remove(app.config['TEMP_DIR'] + "converted.mp4")
    return subprocess.run(("ffmpeg -loglevel quiet -i " + path + " -vcodec copy -acodec copy -scodec copy -f mp4 " + app.config['TEMP_DIR'] + "converted.mp4"), shell=True)

def airplay_background(video):
    ap = AirPlay('10.0.0.22')
    if video[-4:] != ".mp4":
        transcode(app.config['FILES_DIR'] + video)
        video = 'Temp/converted.mp4'
    print(ap.play(app.config['MEDIA_URL'] + video))
    print(ap.playback_info())
    while True:
        for ev in ap.events(block = False):
            newstate = ev.get('state', None)
            if newstate == 'stopped':
                return

def localplay(video):
    if video[-4:] != ".mp4":
        transcode(app.config['FILES_DIR'] + video)
        video = 'Temp/converted.mp4'
    return (app.config['MEDIA_URL'] + video)


@app.route('/')
@app.route('/home')
def home():
    movies = glob.glob(app.config['FILES_DIR'] + '*')
    movies = [movie.rsplit("/", 1)[-1] for movie in movies]
    print(movies)
    return render_template('home.html', movies = movies)

@app.route('/play')
def play():
    video = request.args.get('video', '')
    video_thread = Thread(target = airplay_background, args = (video, ))
    video_thread.start()
    return render_template('play.html', video = video)

@app.route('/playlocal')
def playlocal():
    video = request.args.get('video', '')
    url = localplay(video)
    print(url)
    return render_template('playlocal.html', url = url, video = video)
