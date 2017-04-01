"""Test IMDB-Pie responses."""

import pytest
from imdbpie import Imdb


class TestMovie:
    """Test IMDB Movie Calls."""

    imdb = Imdb(anonymize=True)
    title = imdb.get_title_by_id("tt0133093")

    def test_movietitle(self):
        """Test Movie Title."""
        assert self.title.title == "The Matrix"

    def test_coverpic(self):
        """Test Cover Pic Url."""
        assert self.title.poster_url == "https://images-na.ssl-images-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"

    def test_releasedate(self):
        """Test Release Date."""
        assert int(self.title.year) == 1999

    def test_description(self):
        """Test Description."""
        assert self.title.plot_outline == "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."

    def test_starrating(self):
        """Test Star Rating. Subject to Change based on IMDB voting."""
        assert self.title.rating == 8.7

    def test_runtime(self):
        """Test Run Time."""
        print(self.title.runtime)
        assert (int(self.title.runtime) / 60) == 136
