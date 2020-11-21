from tests.util import make_soup


def test_listing_item_count(client):
    """Test that static listing has correct number of items."""
    resp = client.get("/")
    soup = make_soup(resp.data)
    assert len(soup.find_all("p")) == 3
