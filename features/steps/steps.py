from behave import *

from application import db
from application.tips.models import Tip, Book, Video
from tests.util import make_soup


@when("käyttäjä avaa etusivun")
def step_impl(context):
    context.response = context.client.get("/")

@when("käyttäjä avaa sivun kirjan lisäämiselle")
def open_add_book(context):
    context.response = context.client.get("/tips/add-book")

@when("käyttäjä avaa vinkkilista sivun")
def open_tips(context):
    context.response = context.client.get("/tips")

@then("käyttäjä näkee vinkkilistan")
def user_sees_list(context):
     soup = make_soup(context.response.data)
     
     assert "Clean Code: A Handbook of Agile Software Craftsmanship" in soup.text
     assert "Merge sort algorithm" in soup.text
     assert 2 == len(soup.findAll(class_="card mb-3"))


@then("käyttäjä näkee staattisen vinkkilistan")
def step_impl(context):
    page = make_soup(context.response.data).text
    assert "Otsikko: Clean Code: A Handbook of Agile Software Craftsmanship" in page
    assert "Otsikko: Merge sort algorithm" in page
    assert "Otsikko: Consistency models" in page

@then("käyttäjä näkee oikeanlaisen formin")
def form_is_right(context):
    page = make_soup(context.response.data)

    assert 5 == len(page.find_all('input'))
    assert 1 == len(page.find_all('textarea'))
    assert "Otsikko" in page.text
    assert "Kirjailija" in page.text
    assert "Julkaisuvuosi" in page.text
    assert "ISBN" in page.text
    assert "Sivuja" in page.text
    assert "Oma kommentti" in page.text