from behave import *

from application import db
from application.tips.models import Tip, Book, Video, Audiobook
from tests.util import make_soup, reset_database


@given("että ollaan lähtötilanteessa")
def step_impl(context):
    reset_database()

@when("käyttäjä avaa sivun kirjan lisäämiselle")
def open_add_book(context):
    context.response = context.client.get("/tips/add-book")

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
        "comment": "gives and error"
    }

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
    assert len(allTipsAfterDelete) == 2

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
    audiobooks = Audiobook.query.filter_by(title=context.form_data['title']).all()

    assert len(audiobooks) == 1
    new_audiobook = audiobooks[0]
    assert new_audiobook.title == context.form_data['title']
    assert new_audiobook.author == context.form_data['author']
    assert new_audiobook.narrator == context.form_data['narrator']
    assert new_audiobook.title == context.form_data['title']
    assert new_audiobook.publication_year == context.form_data['publication_year']
    assert new_audiobook.lengthInSeconds == context.form_data['lengthInSeconds']
    assert new_audiobook.comment == context.form_data['comment']

@then("äänikirjaa ei lisätä vinkkeihin")
def audiobook_is_not_added_to_list(context):
    audiobooks = Audiobook.query.filter_by(title=context.form_data['title']).all()

    assert len(audiobooks) == 0

@when("käyttäjä avaa vinkkisivun")
def step_impl(context):
    context.response = context.client.get("/")


@when('hakee ehdon "{filter}" arvolla "{value}"')
def step_impl(context, filter, value):
    context.response = context.client.get(f"/?{filter}={value}")


@then('ainoastaan vinkki "{text}" näkyy')
def step_impl(context, text):
    page = make_soup(context.response.data)
    cards = page.findAll(class_="card-body")
    assert len(cards) == 1
    assert text in cards[0].text


@then("kaikki vinkit näkyvät")
def step_impl(context):
    page = make_soup(context.response.data)
    assert len(page.find_all(class_="card-body")) == 3
