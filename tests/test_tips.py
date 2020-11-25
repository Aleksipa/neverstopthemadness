import re

from application import db
from application.tips.models import Tip, Book
from tests.util import make_soup


def test_initial_data(client):
    soup = make_soup(client.get("/tips").data)
    assert "Clean Code: A Handbook of Agile Software Craftsmanship" in soup.text


def test_empty_db(client):
    db.session().query(Tip).delete()
    soup = make_soup(client.get("/tips").data)
    assert len(soup.find(class_="container").find_all("p")) == 0


def test_missing_field(client):
    db.session().add(Book(
        title="test title",
        author="test author",
    ))
    soup = make_soup(client.get("/tips").data)
    test_book = soup.find(string=re.compile("test title")).parent
    assert "ISBN" not in test_book.text
