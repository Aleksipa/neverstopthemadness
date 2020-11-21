from bs4 import BeautifulSoup


def make_soup(markup: str) -> BeautifulSoup:
    return BeautifulSoup(markup, "html.parser")
