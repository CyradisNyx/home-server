"""Define models."""
from homeserver import db
import omdb
import PTN


class videofile(db.Model):
    """Store File Data."""

    __tablename__ = 'videofile'
    imdb_key = db.Column(db.String(30))
    file_path = db.Column(db.String(180), primary_key=True)
    file_type = db.Column(db.String(10))
    file_resolution = db.Column(db.String(10))
    audio_codec = db.Column(db.String(10))
    video_codec = db.Column(db.String(10))

    def __init__(self, file_path, imdb_key=None):
        """
        Constructor Method, assign instance variables.

        Set file_path based on input, parse file name to find specific metadata
        and assign to variables. Assign imdb_key to instance variable, or find
        if None. Check if videofile is a movie or an episode, then if moviedata
        or seriesdata for videofile already exists, else build.

        @str file_path: Full path to specific videofile
        @str imdb_key: IMDB Key corresponding to movie in videofile

        @return new row in db
        """
        self.file_path = file_path
        """@str Absolute Path to File."""

        data = PTN.parse(self.file_path.rsplit("/", 1)[-1])
        """@dict Parsing Result from File Path."""

        if 'container' in data:
            self.file_type = data['container']
            """@str File extension, ie ".mkv" or ".avi"."""
        if 'resolution' in data:
            self.file_resolution = data['resolution']
            """@str Video Resolution, ie "1080p" or "720p"."""
        if 'audio' in data:
            self.audio_codec = data['audio']
            """@str Audio Codec, ie "DTS" or "FLAC"."""
        if 'codec' in data:
            self.video_codec = data['codec']
            """@str Video Codec, ie "x264" or "HEVC"."""

        if imdb_key is None:
            imdb_key = self.FindID(data)

        if moviedata.query.get(imdb_key) is None and self.CheckType(imdb_key) == 'movie':
            db.session.add(moviedata(imdb_key=imdb_key))
            db.session.commit()

        elif seriesdata.query.get(imdb_key) is None and self.CheckType(imdb_key) == 'episode':
            db.session.add(seriesdata(imdb_key=imdb_key))
            db.session.commit()

        self.imdb_key = imdb_key
        """@str Key to corresponding IMDB Entry."""

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<videofile:{}, imdb_key:{}>'.format(self.file_path, self.imdb_key)

    def FindID(self, data):
        """
        Parse File Name and Output imdb_key.

        Check if videofile is a movie, or an episode in a larger series. Use
        data from parsed filename to search IMDB database and find ID.

        @dict data: Data from parsing filename

        @return str valid corresponding imdb_key
        """
        if 'season' in data:
            episode = omdb.get(episode=data['episode'], season=data['season'], title=data['title'])
            return episode.imdb_id
        else:
            if 'year' in data:
                movie = omdb.get(title=data['title'], year=data['year'])
            else:
                movie = omdb.get(title=data['title'])

            return movie.imdb_id

    def CheckType(self, imdb_key):
        """
        Check if Movie or Episode.

        Uses IMDB Api Search by imdb_key to determine video type.

        @str imdb_key: key to look up

        @return 'movie' or 'episode'
        """
        title = omdb.imdbid(imdb_key)
        return title.type


class moviedata(db.Model):
    """Store IMDB Data for Movies."""

    __tablename__ = 'moviedata'
    imdb_key = db.Column(db.String(30), primary_key=True)
    movie_title = db.Column(db.String(90))
    cover_pic = db.Column(db.String(255))
    release_date = db.Column(db.Integer)
    film_description = db.Column(db.String(255))
    star_rating = db.Column(db.Float)
    runtime = db.Column(db.Integer)
    watched = db.Column(db.Integer)

    def __init__(self, imdb_key):
        """
        Constructor Method and assign instance variables.

        Set imdb_key based on declaration input, run an imdb search for the
        key and then parse information into specific fields.

        @str imdb_key: IMDB Key Corresponding to model

        @return new row in db
        """
        self.imdb_key = imdb_key
        """@str Key to Corresponding IMDB Entry."""
        self.watched = 0
        """@int Indicator of whether or not video has been watched
        0 = unwatched, 1= in progress, 2 = watched."""

        title = omdb.imdbid(imdb_key)

        self.movie_title = title.title
        """@str Title of Movie."""
        self.cover_pic = title.poster
        """@str URL for Cover Image."""
        self.release_date = int(title.year)
        """@int Year of release."""
        self.film_description = title.plot
        """@str Short Summary Description."""
        self.star_rating = float(title.imdb_rating)
        """@float Aggregated IMDB Rating out of 10."""
        self.runtime = int(title.runtime.split(" ")[0])
        """@int Runtime in minutes."""

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<moviedata:{}>'.format(self.movie_title)


class seriesdata(db.Model):
    """Store IMDB Data for TV Shows."""

    imdb_key = db.Column(db.String(30), primary_key=True)
    SeriesTitle = db.Column(db.String(90))
    cover_pic = db.Column(db.String(180))
    SeriesDescription = db.Column(db.Text)
    star_rating = db.Column(db.Float)
    NumberOfSeasons = db.Column(db.Integer)
    # Seasons = db.Column()
    NumberOfEpisodes = db.Column(db.Integer)
    watched = db.Column(db.Integer)
