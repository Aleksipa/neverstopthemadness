from bs4 import BeautifulSoup

from application import db
from application.tips.models import Audiobook, Tip, Book, Video, Movie

def make_soup(markup: str) -> BeautifulSoup:
    return BeautifulSoup(markup, "html.parser")


def reset_database():
    """Restore the database to its default state."""
    db.session().query(Tip).delete()
    db.session().query(Book).delete()
    db.session().query(Video).delete()
    db.session().query(Audiobook).delete()
    db.session().query(Movie).delete()
    db.session().commit()
    Tip.insert_initial_values()
