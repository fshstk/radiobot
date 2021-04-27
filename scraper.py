import requests
from bs4 import BeautifulSoup

from schema import Episode


def scrape_items():
    """
    Get XML of all radio episodes from the RSS feed. Each episode is stored
    inside an <item> element.
    """
    url = "https://cba.fro.at/series/toningenieursforum/feed"
    page = requests.get(url)  # NOTE: this takes a while...
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


def add_mp3_url_single(episode):
    """
    Scrape the stored page URL for the given episode and save the URL to its
    audio file.
    """
    page = requests.get(episode.page_url)  # NOTE: this takes a while...
    soup = BeautifulSoup(page.content, "html.parser")
    url = soup.audio.get("src")
    # The mp3 URL usually has "?stream" appended to the end which we don't want:
    episode.mp3_url = url.split("?")[0]


def add_mp3_url(episodes):
    """
    Run `add_mp3_url_single()` on multiple episodes. Be careful, this can take a very
    long time to run.
    """
    episodes_to_process = [ep for ep in episodes if "mp3_url" not in ep]
    if len(episodes_to_process) == 0:
        print("No episodes to process")
        return
    for number, ep in enumerate(episodes_to_process):
        print(f"Processing episode {number+1} of {len(episodes_to_process)}...")
        add_mp3_url(ep)
    print("Done")


def scrape_episodes():
    """
    Putting it all together... returns a list of all episodes.
    """
    return [get_episode(item) for item in scrape_items()]
