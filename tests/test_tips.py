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
    
    assert soup.find(class_="card") == None


def test_missing_field(client):
    db.session().add(Book(
        title="test title",
        author="test author",
    ))
    soup = make_soup(client.get("/tips").data)
    test_book = soup.find(string=re.compile("test title")).parent
    assert "ISBN" not in test_book.text


def test_missing_mandatory_field(client):
    resp = client.post("/tips/add-book", data={
        "title": "new book",
        "publication_year": 2020,
    })
    soup = make_soup(resp.data)
    author = soup.find(attrs={"id": "author"}).parent
    assert "This field is required" in author.text
    assert Book.query.filter_by(title="new book").count() == 0


def test_successful_post(client):
    resp = client.post("/tips/add-book", data={
        "title": "new book",
        "author": "some author",
        "publication_year": 2020,
    })
    assert resp.status_code == 302
    new_book = Book.query.filter_by(title="new book").all()
    assert len(new_book) == 1
    assert new_book[0].title == "new book"
    assert new_book[0].author == "some author"
    assert new_book[0].publication_year == 2020
    assert new_book[0].pages == None
    assert new_book[0].isbn == ""
    assert new_book[0].comment == ""
    assert new_book[0].related_courses == ""
    assert new_book[0].tags == ""
