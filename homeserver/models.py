"""Define models."""
from homeserver import db
from imdbpie import Imdb


class Movie(db.Model):
    """Store Movie Data."""

    id = db.Column(db.Integer, primary_key=True)
    IMDB_Key = db.Column(db.String(30))
    FileName = db.Column(db.String(180), unique=True)

    def __init__(self, IMDB_Key, FileName):
        """Constructor Method."""
        self.IMDB_Key = IMDB_Key
        self.FileName = FileName


class IMDBData(db.Model):
    """Store IMDB Data."""

    IMDB_Key = db.Column(db.Integer, primary_key=True)
    MovieTitle = db.Column(db.String(90))
    CoverPic = db.Column(db.String(180))
    ReleaseDate = db.Column(db.Integer)
    FilmDescription = db.Column(db.Text)
    StarRating = db.Column(db.Float)    # Out of 10
    RunTime = db.Column(db.Integer)  # In Minutes

    def __init__(self, IMDB_Key):
        """Constructor Method and Populate Fields."""
        self.IMDB_Key = IMDB_Key

        title = Imdb().get_title_by_id(IMDB_Key)

        self.MovieTitle = title.title
        self.CoverPic = title.poster_url
        self.ReleaseDate = int(title.year)
        self.Description = title.plot_outline
        self.StarRating = title.rating
        self.RunTime = (int(title.runtime) / 60)
