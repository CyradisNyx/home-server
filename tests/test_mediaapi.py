"""Test IMDB-Pie responses."""

import pytest
import omdb
from homeserver import models


class TestMovie:
    """Test IMDB Movie Calls."""

    file_path = "/Users/sarah/Desktop/Coding/Caddy/Ferris.Bueller's.Day.Off.1986.1080p.BluRay.DTS.x264-FoRM.mkv"
    title = omdb.imdbid('tt0133093')

    def test_movietitle(self):
        """Test Movie Title."""
        assert self.title.title == "The Matrix"

    def test_coverpic(self):
        """Test Cover Pic Url."""
        assert self.title.poster == "https://images-na.ssl-images-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg"

    def test_releasedate(self):
        """Test Release Date."""
        assert int(self.title.year) == 1999

    def test_description(self):
        """Test Description."""
        assert self.title.plot == "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."

    def test_starrating(self):
        """Test Star Rating. Subject to Change based on IMDB voting."""
        assert float(self.title.imdb_rating) == 8.7

    def test_runtime(self):
        """Test Run Time."""
        assert int(self.title.runtime.split(" ")[0]) == 136

    def test_filename(self):
        """Separate FileName from Path."""
        FileName = self.file_path.rsplit("/", 1)[-1]
        assert FileName == "Ferris.Bueller's.Day.Off.1986.1080p.BluRay.DTS.x264-FoRM.mkv"

    def test_findkey(self):
        """Find imdb_key based on FileName."""
        assert models.videofile.FindID(self, self.file_path) == 'tt0091042'

    def test_checktype(self):
        """Check Type of videofile."""
        assert models.videofile.CheckType(self, self.title.imdb_id) == 'movie'


class TestTV:
    """Test IMDB TV Show calls."""

    tv_title = omdb.imdbid('tt4730012')
    file_path = 'friends.s02e01.720p.bluray-sujaidr.mkv'

    def test_findkey(self):
        """Find imdb_key based on FileName."""
        assert models.videofile.FindID(self, self.file_path) == 'tt0583562'

    def test_checktype(self):
        """Check Type of videofile."""
        assert models.videofile.CheckType(self, self.tv_title.imdb_id) == 'episode'
