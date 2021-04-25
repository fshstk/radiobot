# %%

import dateutil.parser
import requests
from bs4 import BeautifulSoup

url = "https://cba.fro.at/series/toningenieursforum/feed"
page = requests.get(url)  # NOTE: this takes a while...
soup = BeautifulSoup(page.content, "xml")
items = soup.find_all("item")

# %%


def get_episode_from_item(item):
    """
    Each episode is stored inside an <item> element. Here, we extract the child
    elements we need and store them in a more accessible format.
    """
    # TODO: No error checking is being done, so a single malformed item can crash
    # the entire script.
    date = item.broadcastDate.string
    if date is not None:
        date = dateutil.parser.parse(date)

    return {
        "title": item.title.string,
        "date": date,
        "url": item.link.string,
        "description": item.description.string,
    }


def get_mp3_from_episode(episode):
    page = requests.get(episode["url"])  # NOTE: this takes a while...

    # We are using "lxml" here as opposed to "xml" above. This is not a typo,
    # they really are two different parsers:
    soup = BeautifulSoup(page.content, "lxml")
    url = soup.audio.get("src")

    # The mp3 URL usually has "?stream" appended to the end, and we want to get
    # rid of it:
    url = url.split("?")[0]
    return url


# %%

episodes = [get_episode_from_item(item) for item in items]

# %%
