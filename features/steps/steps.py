from behave import *

from tests.util import make_soup


@when("käyttäjä avaa etusivun")
def step_impl(context):
    context.response = context.client.get("/")


@then("käyttäjä näkee staattisen vinkkilistan")
def step_impl(context):
    page = make_soup(context.response.data).text
    assert "Otsikko: Clean Code: A Handbook of Agile Software Craftsmanship" in page
    assert "Otsikko: Merge sort algorithm" in page
    assert "Otsikko: Consistency models" in page
