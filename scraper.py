from bs4 import BeautifulSoup

from config import FEED_URL
from schema import Episode


async def scrape_items(session):
    """
    Get XML of all radio episodes from the RSS feed. Each episode is stored
    inside an <item> element. The function must be passed an
    `aiohttp.ClientSession` object.
    """
    async with session.get(FEED_URL) as page:
        soup = BeautifulSoup(await page.text(), "xml")
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


async def scrape_mp3_url(session, episode):
    """
    Scrape the stored page URL for the given episode and return it. The function
    must be passed an `aiohttp.ClientSession` object.
    """
    async with session.get(episode.page_url) as page:
        soup = BeautifulSoup(await page.text(), "html.parser")
    url = soup.audio.get("src")
    # The URL usually has "?stream" appended to the end which we don't want:
    return url.split("?")[0]


async def scrape_episodes(session):
    """
    Putting it all together... returns a list of all episodes. The function must
    be passed an `aiohttp.ClientSession` object.
    """
    return [get_episode(item) for item in await scrape_items(session)]
