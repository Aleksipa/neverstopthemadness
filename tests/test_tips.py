from inspect import cleandoc
import re

from bs4.element import ResultSet

from application import db
from application.tips.models import Tip, Book, Video, Audiobook, Movie
from tests.util import make_soup, reset_database


def test_initial_data(client):
    reset_database()
    soup = make_soup(client.get("/").data)
    assert "Clean Code: A Handbook of Agile Software Craftsmanship" in soup.text


def test_tips_render_video(client):
    db.session().add(Video(
        title="test video",
        source="test source",
        comment="test comment",
        tags="Ohjelmointi, algoritmit"
    ))
    soup = make_soup(client.get("/").data)
    assert "test video" in soup.text
    assert "test source" in soup.text
    assert "test comment" in soup.text
    assert "Ohjelmointi, algoritmit" in soup.text
    
def test_empty_db(client):
    db.session().query(Tip).delete()
    soup = make_soup(client.get("/").data)
    
    assert soup.find(class_="card mb-3") == None


def test_missing_field(client):
    db.session().add(Book(
        title="test title",
        author="test author",
    ))
    soup = make_soup(client.get("/").data)
    test_book = soup.find(string=re.compile("test title")).parent
    assert "ISBN" not in test_book.text


def test_missing_mandatory_field_book(client):
    resp = client.post("/tips/add-book", data={
        "title": "new book",
        "publication_year": 2020,
    })
    soup = make_soup(resp.data)
    author = soup.find(attrs={"id": "author"}).parent
    assert "This field is required" in author.text
    assert Book.query.filter_by(title="new book").count() == 0


def test_successful_post_book(client):
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


def test_missing_mandatory_field_video(client):
    resp = client.post("/tips/add-video", data={
        "title": "test title",
    })
    soup = make_soup(resp.data)
    source = soup.find(attrs={"id": "source"}).parent
    assert "This field is required" in source.text
    assert Video.query.filter_by(title="test title").count() == 0

def test_successful_post_video(client):
    resp = client.post("/tips/add-video", data={
        "title": "new video",
        "source": "www.test.com",
        "upload_date": '2020-12-01',
        "comment": "test comment"
    })
    assert resp.status_code == 302
    new_video = Video.query.filter_by(title="new video", source="www.test.com", upload_date='2020-12-01').all()
    assert len(new_video) == 1
    assert new_video[0].comment == 'test comment'
    assert new_video[0].related_courses == ''

def test_missing_mandatory_field_audiobook(client):
    resp = client.post("/tips/add-audiobook", data={
        "title": "test title"
    })
    soup = make_soup(resp.data)
    author = soup.find(attrs={"id": "author"}).parent
    assert "This field is required" in author.text
    assert Audiobook.query.filter_by(title="test title").count() == 0

def test_successful_post_audiobook(client):
    resp = client.post("/tips/add-audiobook", data={
        "title": "new audiobook",
        "author": "test author",
        "narrator": "test narrator",
        "publication_year": 2018,
        "isbn": "",
        "lengthInSeconds": 12180
    })
    assert resp.status_code == 302
    new_audiobook = Audiobook.query.filter_by(title="new audiobook", author="test author").all()
    assert new_audiobook[0].title == "new audiobook"
    assert new_audiobook[0].author == "test author"
    assert new_audiobook[0].narrator == "test narrator"
    assert new_audiobook[0].publication_year == 2018
    assert new_audiobook[0].isbn == ""
    assert new_audiobook[0].lengthInSeconds == 12180
    
def test_missing_mandatory_field_movie(client):
    resp = client.post("/tips/add-movie", data={
        "director": "test director"
    })
    soup = make_soup(resp.data)
    title = soup.find(attrs={"id": "title"}).parent
    assert "This field is required" in title.text
    assert Movie.query.filter_by(title="test title").count() == 0

def test_successful_post_movie(client):
    resp = client.post("/tips/add-movie", data={
        "title": "new movie",
        "director": "test director",
        "publication_year": 2018,
        "lengthInSeconds": 12180
    })
    assert resp.status_code == 302
    new_movie = Movie.query.filter_by(title="new movie", director="test director").all()
    assert new_movie[0].title == "new movie"
    assert new_movie[0].director == "test director"
    assert new_movie[0].publication_year == 2018
    assert new_movie[0].lengthInSeconds == 12180

def test_successful_edit_audiobook(client):
    old_audiobook = Audiobook.query.filter_by(isbn="978-7834915091").all()
    resp = client.post("/tips/edit/audiobook/" + str(old_audiobook[0].id) + "/", data={
        "title": "Python Programming: The Ultimate Beginner's Guide",
        "author": "test author"
    })
    assert resp.status_code == 302

    new_audiobook = Audiobook.query.filter_by(isbn="978-7834915091").all()
    assert new_audiobook[0].title == "Python Programming: The Ultimate Beginner's Guide"
    assert new_audiobook[0].author == "test author"

def test_empty_search(client):
    reset_database()
    soup = make_soup(client.get("/").data)
    assert len(soup.find_all(class_="card-body")) == 4
    assert soup.find(string=re.compile("Poista rajaukset")) is None


def test_search_single_field(client):
    reset_database()
    soup = make_soup(client.get("/?title=sort").data)
    card = soup.find(class_="card-body")
    assert card is not None
    assert "Merge sort algorithm" in card.text
    assert soup.find(string=re.compile("Poista rajaukset")) is not None


def test_search_invalid_field(client):
    reset_database()
    soup = make_soup(client.get("/?asdasd=asd").data)
    assert soup.find(class_="card-body") is None

def test_successful_edit_book(client):
    allTips = Tip.query.all()
    resp = client.post("/tips/edit/" + str(allTips[0].id) + "/",  data={
        "title": "edited book",
        "author": "some other author",
        "publication_year": 1986,
    })
    assert resp.status_code == 302
    edited_book = Book.query.filter_by(title="edited book").all()
    assert len(edited_book) == 1
    assert edited_book[0].title == "edited book"
    assert edited_book[0].author == "some other author"
    assert edited_book[0].publication_year == 1986


def test_successful_edit_video(client):
    allTips = Tip.query.all()
    resp = client.post("/tips/edit/video/" + str(allTips[1].id) + "/",  data={
        "title": "edited video",
        "source": "www.other.com",
        "comment": "test comment"
    })
    assert resp.status_code == 302
    edited_video = Video.query.filter_by(title="edited video").all()
    assert len(edited_video) == 1
    assert edited_video[0].title == "edited video"
    assert edited_video[0].comment == "test comment"
