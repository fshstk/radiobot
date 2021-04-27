# %%

import dateutil.parser
import requests
from bs4 import BeautifulSoup


def date_string_to_iso(string):
    try:
        return dateutil.parser.parse(string).isoformat()
    except TypeError:
        return ""
    except dateutil.parser.ParserError:
        return ""


def get_episode_from_item(item):
    """
    Each episode is stored inside an <item> element. Here, we extract the child
    elements we need and store them in a more accessible format.
    """
    # TODO: No error checking is being done, so a single malformed item can crash
    # the entire script.
    return {
        "title": item.title.string,
        "date": date_string_to_iso(item.broadcastDate.string),
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

url = "https://cba.fro.at/series/toningenieursforum/feed"
page = requests.get(url)  # NOTE: this takes a while...
soup = BeautifulSoup(page.content, "xml")
items = soup.find_all("item")
episodes = [get_episode_from_item(item) for item in items]

# %%
