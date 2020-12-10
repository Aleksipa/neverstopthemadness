from behave import *

from application import db
from application.tips.models import Tip, Book, Video, Audiobook, Movie
from tests.util import make_soup, reset_database


@given("että ollaan lähtötilanteessa")
def step_impl(context):
    reset_database()

# Kirjaan liittyvät tapaukset

@when("käyttäjä avaa sivun kirjan lisäämiselle")
def open_add_book(context):
    context.response = context.client.get("/tips/add-book")

@when("käyttäjä täyttää kirjan muokkauslomakkeen oikein")
def user_fills_book_form_correctly(context):
    books = Book.query.all()
    context.path = "/tips/edit_book_tip" + str(books[0].id) + "/"
    context.form_data = {
        "title": "some book",
        "author": "some author",
        "comment": "some comment"
    }

@when("käyttäjä täyttää kirjan muokkauslomakkeen väärin")
def user_fills_book_form_incorrectly(context):
    book = Book.query.all()
    context.path = "/tips/edit_book_tip" + str(book[0].id) + "/"
    context.form_data = {
        "title": "",
        "author": "",
        "comment": ""
    }

# Videoon liittyvät tapaukset

@when("käyttäjä avaa sivun videon lisäämiselle")
def open_add_book(context):
    path = "/tips/add-video"
    context.response = context.client.get(path)

@when("käyttäjä täyttää video lomakkeen oikein")
def user_fills_video_form_correctly(context):
    context.path = "/tips/add-video"
    context.form_data = {
        "title": "new video",
        "source": "www.test.com",
        "upload_date": '2020-12-01',
        "comment": "test comment"
    }

@when("käyttäjä täyttää video lomakkeen väärin")
def user_fills_video_form_wrong(context):
    context.path = "/tips/add-video"
    context.form_data = {
        "title": "test shouldnt exist",
        "upload_date": '2020-12-01',
        "comment": "test comment"
    }

@when("käyttäjä avaa sivun videon muokkaamiselle")
def open_edit_video(context):
    videos = Video.query.all()
    context.path = "/tips/edit/" + str(videos[0].id) + "/"
    context.response = context.client.get(context.path)

@when("käyttäjä täyttää videon muokkauslomakkeen oikein")
def user_fills_video_edit_form_correctly(context):
    videos = Video.query.all()
    context.path = "/tips/edit/video/" + str(videos[0].id) + "/"
    context.form_data = {
        "title": "modified video",
        "source": "www.modified.com",
        "upload_date": '2020-12-01',
        "comment": "test comment"
    }

# Äänikirjaan liittyvät tapaukset

@when("käyttäjä avaa sivun äänikirjan lisäämiselle")
def open_add_audiobook(context):
    context.response = context.client.get("/tips/add-audiobook")

@when("käyttäjä täyttää äänikirjan lomakkeen oikein")
def user_fills_audiobook_form_correctly(context):
    context.path = "/tips/add-audiobook"
    context.form_data = {
        "title": "new audiobook",
        "author": "some author",
        "narrator": "some narrator",
        "publication_year": 2019,
        "lengthInSeconds": 8024,
        "comment": "test comment"
    }

@when("käyttäjä täyttää äänikirjan lomakkeen väärin")
def user_fills_audiobook_form_wrong(context):
    context.path = "/tips/add-audiobook"
    context.form_data = {
        "title": "valid title",
        "narrator": "but missing author",
        "comment": "gives an error"
    }

@when("käyttäjä avaa sivun äänikirjan muokkaamiselle")
def open_edit_audiobook(context):
    audiobooks = Audiobook.query.all()
    context.path = "/tips/edit/" + str(audiobooks[0].id) + "/"
    context.response = context.client.get(context.path)

@when("käyttäjä täyttää äänikirjan muokkauslomakkeen oikein")
def user_fills_audiobook_edits_correctly(context):
    audiobooks = Audiobook.query.all()
    context.path = "/tips/edit/audiobook/" + str(audiobooks[0].id) + "/"
    context.form_data = {
        "title": "new audiobook",
        "author": "some author",
        "narrator": "some narrator",
        "publication_year": 2019,
        "lengthInSeconds": 8024,
        "comment": "test comment"
    }

@when("käyttäjä täyttää äänikirjan muokkauslomakkeen väärin")
def user_fills_audiobook_edits_wrong(context):
    audiobooks = Audiobook.query.all()
    context.path = "/tips/edit/audiobook/" + str(audiobooks[0].id) + "/"
    context.form_data = {
        "title": "valid title",
        "narrator": "but missing author",
        "comment": "gives an error"
    }

# Elokuvaan liittyvät tapaukset
    
@when("käyttäjä avaa sivun elokuvan lisäämiselle")
def open_add_movie(context):
    context.response = context.client.get("/tips/add-movie")

@when("käyttäjä täyttää elokuvan lomakkeen oikein")
def user_fills_movie_form_correctly(context):
    context.path = "/tips/add-movie"
    context.form_data = {
        "title": "some movie",
        "director": "test director",
        "publication_year": 2019,
        "lengthInSeconds": 8024,
        "comment": "test comment"
    }

@when("käyttäjä täyttää elokuvan lomakkeen väärin")
def user_fills_movie_form_wrong(context):
    context.path = "/tips/add-movie"
    context.form_data = {
        "title": "title exists but missing director",
        "comment": "gives and error"
    }

# Luettu statukseen, poistoon ja vinkkien esitykseen liittyvät tapaukset

@when("käyttäjä lähettää lomakkeen")
def user_sends_form(context):
    context.response = context.client.post(context.path, data=context.form_data)

@when("käyttäjä vaihtaa vinkin luettu statusta")
def user_(context):
    tips = Tip.query.all()
    firstId = str(tips[0].id)
    path = '/tips/change_read/' + firstId
    context.response = context.client.post(path)
    context.id = firstId

@when("käyttäjä avaa vinkkilista sivun")
def open_tips(context):
    context.response = context.client.get("/")

@when("käyttäjä poistaa vinkin")
def tips_remove(context):
    allTips = Tip.query.all()
    path = "/tips_remove/" + str(allTips[0].id)
    context.response = context.client.delete(path)

@then("käyttäjä näkee vinkkilistan, josta on poistettu yksi vinkki")
def user_sees_list(context):
    allTipsAfterDelete = Tip.query.all()
    assert len(allTipsAfterDelete) == 3

@then("käyttäjä näkee vinkkilistan")
def user_sees_list(context):
     soup = make_soup(context.response.data)
     
     assert "Clean Code: A Handbook of Agile Software Craftsmanship" in soup.text
     assert "Merge sort algorithm" in soup.text

@then("käyttäjä näkee vinkkilistan, jossa vinkki on merkitty luetuksi")
def user_sees_that_tip_is_read(context):
     
     resp = context.client.get("/")
     soup = make_soup(resp.data)
     tip = soup.find(id=context.id)
     assert "Kyllä" in soup.text

@then("käyttäjä näkee vinkkilistan, jossa vinkki on merkitty lukemattomaksi")
def user_sees_that_tip_is_read(context):
     
     resp = context.client.get("/")
     soup = make_soup(resp.data)
     tip = soup.find(id=context.id)
     assert "Ei" in soup.text

# Kirjaan liittyvät tapaukset

@then("käyttäjä näkee oikeanlaisen kirja formin")
def form_is_right(context):
    page = make_soup(context.response.data)

    assert 6 == len(page.find_all('input'))
    assert 1 == len(page.find_all('textarea'))
    assert "Otsikko" in page.text
    assert "Kirjailija" in page.text
    assert "Julkaisuvuosi" in page.text
    assert "ISBN" in page.text
    assert "Sivuja" in page.text
    assert "Oma kommentti" in page.text

@then("muokattu kirja löytyy vinkeistä")
def valid_modified_audiobook_is_found(context):
    books = Book.query.all()
    modified_book = books[0]
    assert modified_book.title == context.form_data['some book']
    assert modified_book.author == context.form_data['some author']
    assert modified_book.comment == context.form_data['some comment']

@then("muokattua kirjaa ei löydy vinkeistä")
def incorrectly_modified_book_is_not_found(context):
    books = Book.query.all()
    unmodified_book = books[0]
    assert unmodified_book.title == "Clean Code: A Handbook of Agile Software Craftsmanship"

# Videoon liittyvät tapaukset

@then("käyttäjä näkee oikeanlaisen video formin")
def form_is_right(context):
    page = make_soup(context.response.data)

    assert 5 == len(page.find_all('input'))
    assert 1 == len(page.find_all('textarea'))
    assert "Otsikko" in page.text
    assert "Ladattu" in page.text
    assert "URL" in page.text
    assert "Liittyvät kurssit" in page.text
    assert "Tunnisteet" in page.text
    assert "Oma kommentti" in page.text

@then("video lisätään vinkkeihin")
def tip_is_added_to_list(context):
    videos = Video.query.filter_by(title=context.form_data['title']).all()

    assert len(videos) == 1
    new_video = videos[0]
    assert new_video.title == context.form_data['title']
    assert new_video.source == context.form_data['source']
    assert new_video.comment == context.form_data['comment']

@then("videota ei lisätä vinkkeihin")
def tip_is_not_added_to_list(context):
    videos = Video.query.filter_by(title=context.form_data['title']).all()

    assert len(videos) == 0

@then("muokattu video löytyy vinkeistä")
def video_is_updated(context):
    videos = Video.query.all()
    assert len(videos) == 1
    modified_video = videos[0]
    assert modified_video.title == context.form_data['title']
    assert modified_video.comment == context.form_data['comment']


@then("video ei muokkaannu")
def incorrectly_modified_book_is_not_found(context):
    videos = Video.query.all()
    unmodified_video = videos[0]
    assert unmodified_video.title == "Merge sort algorithm"

# Äänikirjaan liittyvät tapaukset

@then("käyttäjä näkee oikeanlaisen äänikirjan formin")
def audiobook_form_is_right(context):
    page = make_soup(context.response.data)

    assert 8 == len(page.find_all('input'))
    assert 1 == len(page.find_all('textarea'))
    assert "Otsikko" in page.text
    assert "Kirjailija" in page.text
    assert "Lukija" in page.text
    assert "Julkaisuvuosi" in page.text
    assert "ISBN" in page.text
    assert "Pituus" in page.text
    assert "Liittyvät kurssit" in page.text
    assert "Tunnisteet" in page.text
    assert "Oma kommentti" in page.text

@then("äänikirja lisätään vinkkeihin")
def audiobook_is_added_to_list(context):
    audiobooks = Audiobook.query.all()
    assert len(audiobooks) == 2
    new_audiobook = audiobooks[1]
    assert new_audiobook.title == context.form_data['title']
    assert new_audiobook.author == context.form_data['author']
    assert new_audiobook.narrator == context.form_data['narrator']
    assert new_audiobook.title == context.form_data['title']
    assert new_audiobook.publication_year == context.form_data['publication_year']
    assert new_audiobook.lengthInSeconds == context.form_data['lengthInSeconds']
    assert new_audiobook.comment == context.form_data['comment']

@then("äänikirjaa ei lisätä vinkkeihin")
def audiobook_is_not_added_to_list(context):
    audiobooks = Audiobook.query.all()
    assert len(audiobooks) == 1

@then("muokattu äänikirja löytyy vinkeistä")
def valid_modified_audiobook_is_found(context):
    audiobooks = Audiobook.query.all()
    assert len(audiobooks) == 1
    modified_audiobook = audiobooks[0]
    assert modified_audiobook.title == context.form_data['title']
    assert modified_audiobook.author == context.form_data['author']
    assert modified_audiobook.narrator == context.form_data['narrator']
    assert modified_audiobook.title == context.form_data['title']
    assert modified_audiobook.publication_year == context.form_data['publication_year']
    assert modified_audiobook.lengthInSeconds == context.form_data['lengthInSeconds']
    assert modified_audiobook.comment == context.form_data['comment']

@then("muokattua äänikirjaa ei löydy vinkeistä")
def invalid_modified_audiobook_is_not_found(context):
    audiobooks = Audiobook.query.all()
    assert len(audiobooks) == 1
    unmodified_audiobook = audiobooks[0]
    assert unmodified_audiobook.title == "Python Programming: The Ultimate Beginner's Guide to Master Python Programming Step by Step with Practical Exercices"

# Elokuvaan liittyvät tapaukset

@then("käyttäjä näkee oikeanlaisen elokuvan formin")
def movie_form_is_right(context):
    page = make_soup(context.response.data)

    assert 6 == len(page.find_all('input'))
    assert 1 == len(page.find_all('textarea'))
    assert "Otsikko" in page.text
    assert "Ohjaaja" in page.text
    assert "Julkaisuvuosi" in page.text
    assert "Pituus" in page.text
    assert "Liittyvät kurssit" in page.text
    assert "Tunnisteet" in page.text
    assert "Oma kommentti" in page.text

@then("elokuva lisätään vinkkeihin")
def movie_is_added_to_list(context):
    movies = Movie.query.filter_by(title=context.form_data['title']).all()

    assert len(movies) == 1
    new_movie = movies[0]
    assert new_movie.title == context.form_data['title']
    assert new_movie.director == context.form_data['director']
    assert new_movie.publication_year == context.form_data['publication_year']
    assert new_movie.lengthInSeconds == context.form_data['lengthInSeconds']
    assert new_movie.comment == context.form_data['comment']

@then("elokuvaa ei lisätä vinkkeihin")
def movie_is_not_added_to_list(context):
    movies = Movie.query.filter_by(title=context.form_data['title']).all()

    assert len(movies) == 0

# Hakuun liittyvät tapaukset

@when("käyttäjä avaa vinkkisivun")
def step_impl(context):
    context.response = context.client.get("/")

@when('hakee ehdon "{filter}" arvolla "{value}"')
def step_impl(context, filter, value):
    context.response = context.client.get(f"/?{filter}={value}")


@when('hakee ehtojen "{filter1}" ja "{filter2}" arvoilla "{value1}" ja "{value2}"')
def step_impl(context, filter1, filter2, value1, value2):
    context.response = context.client.get(
        f"/?{filter1}={value1}&{filter2}={value2}")

@then('ainoastaan vinkki "{text}" näkyy')
def step_impl(context, text):
    page = make_soup(context.response.data)
    cards = page.findAll(class_="card-body")
    assert len(cards) == 1
    assert text in cards[0].text


@then("kaikki vinkit näkyvät")
def step_impl(context):
    page = make_soup(context.response.data)
    assert len(page.find_all(class_="card-body")) == 4

