"""Defines views and routes for app."""

from flask import render_template, request
from homeserver import app, db
from homeserver.models import videofile, moviedata
from homeserver.streaming import airplay_background, localplay
import os
from threading import Thread


@app.route('/')
@app.route('/home')
def home():
    """Route for homepage."""
    return render_template('home.html')


@app.route('/movies')
def movies():
    """List movies available."""
    MovieTypes = ('.mkv', '.mp4', '.mov', '.m4v')
    Movies = {}
    for root, dirs, files in os.walk(app.config['FILES_DIR']):
        for file in files:
            if file[0] == ".":
                continue
            MovieName = file.rsplit("/", 1)[-1]
            if file.endswith(MovieTypes) and root == app.config['FILES_DIR']:
                Movies[root + file] = MovieName
            elif file.endswith(MovieTypes):
                Movies[(root + "/" + file)] = MovieName

    db_data = {}
    for k, v in enumerate(Movies):
        if db.session.query(db.exists().where(videofile.file_path == v)).scalar() is False:
            temp = videofile(v)
            db.session.add(temp)
            db.session.commit()
        temp = videofile.query.get(v)
        print(temp)
        db_data[v] = moviedata.query.get(temp.imdb_key)
    print(db_data)
    return render_template('movies.html', movies=db_data)


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
    return render_template('playlocal.html', url=url, video=video)
