"""Define models."""
from homeserver import db
import omdb
import PTN


class VideoFile(db.Model):
    """Store Movie Data."""

    __tablename__ = 'videofile'
    id = db.Column(db.Integer, primary_key=True)
    IMDBData = db.Column(db.String(30), db.ForeignKey('moviedata.IMDB_Key'))
    FilePath = db.Column(db.String(180), unique=True)
    FileType = db.Column(db.String(10))
    FileResolution = db.Column(db.String(10))
    AudioCodec = db.Column(db.String(10))
    VideoCodec = db.Column(db.String(10))

    def __init__(self, FilePath, IMDB_Key=None):
        """Constructor Method."""
        if IMDB_Key is None:
            IMDB_Key = self.FindID(FilePath)

        if IMDBMovieData.query.get(IMDB_Key) is None:
            db.session.add(IMDBMovieData(IMDB_Key=IMDB_Key))
            db.session.commit()

        self.IMDBData = IMDBMovieData.query.get(IMDB_Key)
        self.FilePath = FilePath

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<VideoFile:{}, ID:{}>'.format(self.FilePath, self.id)

    def FindID(self, Path):
        """Parse File Name and Output IMDB_Key."""
        data = PTN.parse(self.FilePath.rsplit("/", 1)[-1])

        self.FileType = data['container']
        if 'resolution' in data:
            self.FileResolution = data['resolution']
        if 'audio' in data:
            self.AudioCodec = data['audio']
        if 'codec' in data:
            self.VideoCodec = data['codec']

        if 'season' in data:
            episode = omdb.get(episode=data['episode'], season=data['season'], title=data['title'])
            return episode.imdb_id
        else:
            if 'year' in data:
                moardata = omdb.get(title=data['title'], year=data['year'])
            else:
                moardata = omdb.get(title=data['title'])

            return moardata.imdb_id

    def CheckType(self, IMDB_Key):
        """Check if Movie or Episode."""
        title = omdb.imdbid(IMDB_Key)
        return title.type


class IMDBMovieData(db.Model):
    """Store IMDB Data for Movies."""

    __tablename__ = 'moviedata'
    IMDB_Key = db.Column(db.String(30), primary_key=True)
    MovieTitle = db.Column(db.String(90))
    CoverPic = db.Column(db.String(255))
    ReleaseDate = db.Column(db.Integer)
    FilmDescription = db.Column(db.String(255))
    StarRating = db.Column(db.Float)    # Out of 10
    RunTime = db.Column(db.Integer)  # In Minutes
    Watched = db.Column(db.Integer)  # 0=unwatched, 1=inprogress, 2=watched
    Files = db.relationship('VideoFile', backref='MovieData')

    def __init__(self, IMDB_Key):
        """Constructor Method and Populate Fields."""
        self.IMDB_Key = IMDB_Key
        self.Watched = 0

        title = omdb.imdbid(IMDB_Key)

        self.MovieTitle = title.title
        self.CoverPic = title.poster
        self.ReleaseDate = int(title.year)
        self.FilmDescription = title.plot
        self.StarRating = float(title.imdb_rating)
        self.RunTime = int(self.title.runtime.split(" ")[0])

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<IMDBFileData:{}>'.format(self.MovieTitle)


'''
class IMDBSeriesData(db.Model):
    """Store IMDB Data for TV Shows."""

    IMDB_Key = db.Column(db.String(30), primary_key=True)
    SeriesTitle = db.Column(db.String(90))
    CoverPic = db.Column(db.String(180))
    SeriesDescription = db.Column(db.Text)
    StarRating = db.Column(db.Float)
    NumberOfSeasons = db.Column(db.Integer)
    Seasons = db.relationship('IMDBSeasonData',
                              backref='Series',)
    NumberOfEpisodes = db.Column(db.Integer)
    Watched = db.Column(db.Integer)
'''
