from flask import *
from . import app
from threading import Thread
from airplay import AirPlay
import os, glob

def airplay_background(video):
    ap = AirPlay('10.0.0.22')
    print(ap.play(app.config['MEDIA_URL'] + video))
    print(ap.playback_info())
    while True:
        for ev in ap.events(block = False):
            newstate = ev.get('state', None)
            if newstate == 'stopped':
                return

@app.route('/')
@app.route('/home')
def home():
    movies = glob.glob(app.config['FILES_DIR'] + '*.mp4')
    movies = [movie.rsplit("/", 1)[-1] for movie in movies]
    print(movies)
    return render_template('home.html', movies = movies)

@app.route('/play')
def play():
    video = request.args.get('video', '')
    video_thread = Thread(target = airplay_background, args = (video, ))
    video_thread.start()
    return render_template('play.html', video = video)
