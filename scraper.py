import requests
from bs4 import BeautifulSoup

from config import FEED_URL
from schema import Episode


def scrape_items():
    """
    Get XML of all radio episodes from the RSS feed. Each episode is stored
    inside an <item> element.
    """
    page = requests.get(FEED_URL)  # NOTE: this takes a while...
    soup = BeautifulSoup(page.content, "xml")
    return soup.find_all("item")


def get_episode(item):
    """
    Extract the child elements we need and store them as a MongoDB collection
    entry.
    """
    return Episode(
        title=textify(item.title.string),
        description=textify(item.description.string),
        date=item.broadcastDate.string,
        page_url=item.link.string,
    )


def textify(string):
    """
    Some episode titles have HTML-encoded special characters (e.g. "&amp;"), and
    some descriptions are wrapped in <p> elements. The easiest way to get rid of
    both is to run the string through the HTML parser a second time.
    """
    return BeautifulSoup(string, "html.parser").get_text()


def scrape_mp3_url(episode):
    """
    Scrape the stored page URL for the given episode and return it.
    """
    page = requests.get(episode.page_url)  # NOTE: this takes a while...
    soup = BeautifulSoup(page.content, "html.parser")
    url = soup.audio.get("src")
    # The mp3 URL usually has "?stream" appended to the end which we don't want:
    return url.split("?")[0]


def scrape_episodes():
    """
    Putting it all together... returns a list of all episodes.
    """
    return [get_episode(item) for item in scrape_items()]
