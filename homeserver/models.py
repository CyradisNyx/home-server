"""Define models."""
from homeserver import db
from imdbpie import Imdb


class VideoFile(db.Model):
    """Store Movie Data."""

    __tablename__ = 'videofile'
    id = db.Column(db.Integer, primary_key=True)
    IMDBData = db.Column(db.String(30), db.ForeignKey('moviedata.IMDB_Key'))
    FileName = db.Column(db.String(180), unique=True)

    def __init__(self, IMDB_Key, FileName):
        """Constructor Method."""
        if IMDBMovieData.query.get(IMDB_Key) is None:
            db.session.add(IMDBMovieData(IMDB_Key=IMDB_Key))
            db.session.commit()

        self.IMDBData = IMDBMovieData.query.get(IMDB_Key)
        self.FileName = FileName

    def __repr__(self):
        """Return Pretty Formatted Summary of Model."""
        return '<VideoFile:{}, ID:{}>'.format(self.FileName, self.id)


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

        title = Imdb().get_title_by_id(IMDB_Key)

        self.MovieTitle = title.title
        self.CoverPic = title.poster_url
        self.ReleaseDate = int(title.year)
        self.FilmDescription = title.plot_outline
        self.StarRating = title.rating
        self.RunTime = (int(title.runtime) / 60)

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
