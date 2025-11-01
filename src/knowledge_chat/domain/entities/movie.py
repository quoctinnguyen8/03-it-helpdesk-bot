"""Movie data model module.

This module defines the Movie class, representing a single movie record
that can be loaded from a CSV or other data source.
"""

from pydantic import BaseModel


class Movie(BaseModel):
    """Represents a movie record.

    Attributes:
        title (str): The title of the movie.
        genre (str): The genre or category of the movie.
        year (int): The year the movie was released.
        description (str): A brief description or synopsis of the movie.
    """

    title: str
    genre: str
    year: int
    description: str
