"""Define models."""
from homeserver import db
import omdb
import PTN


class videofile(db.Model):
    """Store Movie Data."""

    __tablename__ = 'videofile'
    id = db.Column(db.Integer, primary_key=True)
    imdb_data = db.Column(db.String(30), db.ForeignKey('moviedata.imdb_key'))
    file_path = db.Column(db.String(180), unique=True)
    file_type = db.Column(db.String(10))
    file_resolution = db.Column(db.String(10))
    audio_codec = db.Column(db.String(10))
    video_codec = db.Column(db.String(10))

    def __init__(self, file_path, imdb_key=None):
        """Constructor Method."""
        self.file_path = file_path

        if imdb_key is None:
            imdb_key = self.FindID(file_path)

        if moviedata.query.get(imdb_key) is None:
            db.session.add(moviedata(imdb_key=imdb_key))
            db.session.commit()

        self.imdb_data = moviedata.query.get(imdb_key)

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<videofile:{}, ID:{}>'.format(self.file_path, self.id)

    def FindID(self, Path):
        """Parse File Name and Output imdb_key."""
        data = PTN.parse(self.file_path.rsplit("/", 1)[-1])
        print(data)

        self.file_type = data['container']
        if 'resolution' in data:
            self.file_resolution = data['resolution']
        if 'audio' in data:
            self.audio_codec = data['audio']
        if 'codec' in data:
            self.video_codec = data['codec']

        if 'season' in data:
            episode = omdb.get(episode=data['episode'], season=data['season'], title=data['title'])
            return episode.imdb_id
        else:
            if 'year' in data:
                moardata = omdb.get(title=data['title'], year=data['year'])
            else:
                moardata = omdb.get(title=data['title'])

            return moardata.imdb_id

    def CheckType(self, imdb_key):
        """Check if Movie or Episode."""
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
    star_rating = db.Column(db.Float)    # Out of 10
    runtime = db.Column(db.Integer)  # In Minutes
    watched = db.Column(db.Integer)  # 0=unwatched, 1=inprogress, 2=watched
    files = db.relationship('videofile', backref='moviedata')

    def __init__(self, imdb_key):
        """Constructor Method and Populate Fields."""
        self.imdb_key = imdb_key
        self.watched = 0

        title = omdb.imdbid(imdb_key)

        self.movie_title = title.title
        self.cover_pic = title.poster
        self.release_date = int(title.year)
        self.film_description = title.plot
        self.star_rating = float(title.imdb_rating)
        self.runtime = int(title.runtime.split(" ")[0])

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<moviedata:{}>'.format(self.movie_title)


'''
class IMDBSeriesData(db.Model):
    """Store IMDB Data for TV Shows."""

    imdb_key = db.Column(db.String(30), primary_key=True)
    SeriesTitle = db.Column(db.String(90))
    cover_pic = db.Column(db.String(180))
    SeriesDescription = db.Column(db.Text)
    star_rating = db.Column(db.Float)
    NumberOfSeasons = db.Column(db.Integer)
    Seasons = db.relationship('IMDBSeasonData',
                              backref='Series',)
    NumberOfEpisodes = db.Column(db.Integer)
    watched = db.Column(db.Integer)
'''
