from behave import *

from application import db
from application.tips.models import Tip, Book, Video
from tests.util import make_soup, reset_database


@given("että ollaan lähtötilanteessa")
def step_impl(context):
    reset_database()

@when("käyttäjä avaa etusivun")
def step_impl(context):
    context.response = context.client.get("/")

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

@when("käyttäjä lähettää lomakkeen")
def user_sends_form(context):
    context.response = context.client.post(context.path, data=context.form_data)


@when("käyttäjä avaa vinkkilista sivun")
def open_tips(context):
    context.response = context.client.get("/tips")

@when("käyttäjä poistaa vinkin")
def tips_remove(context):
    allTips = Tip.query.all()
    context.response = context.client.delete("/tips_remove/allTips[0]['id']")

@then("käyttäjä näkee vinkkilistan, josta on poistettu yksi vinkki")
def user_sees_list(context):
    page = make_soup(context.response.data)
    assert len(page.find_all(class_="card-body")) == 2

@then("käyttäjä näkee vinkkilistan")
def user_sees_list(context):
     soup = make_soup(context.response.data)
     
     assert "Clean Code: A Handbook of Agile Software Craftsmanship" in soup.text
     assert "Merge sort algorithm" in soup.text
     #assert 2 == len(soup.findAll(class_="card mb-3"))


@then("käyttäjä näkee staattisen vinkkilistan")
def step_impl(context):
    page = make_soup(context.response.data).text
    assert "Otsikko: Clean Code: A Handbook of Agile Software Craftsmanship" in page
    assert "Otsikko: Merge sort algorithm" in page
    assert "Otsikko: Consistency models" in page

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


@when("käyttäjä avaa vinkkisivun")
def step_impl(context):
    context.response = context.client.get("/tips")


@when('hakee ehdon "{filter}" arvolla "{value}"')
def step_impl(context, filter, value):
    context.response = context.client.get(f"/tips?{filter}={value}")


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
