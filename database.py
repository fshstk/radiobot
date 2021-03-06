import aiohttp
import mongoengine
from mongoengine.errors import NotUniqueError

from config import DATABASE_URL
from schema import Episode
from scraper import scrape_episodes, scrape_mp3_url

mongoengine.connect(host=DATABASE_URL)


async def add_untracked_episodes(session, progress_callback=None):
    """
    Scrapes the RSS feed for all available episodes, then tries to add them to
    the database. Existing episodes will be rejected by the database backend as
    each episode must have a unique page url. The function must be passed an
    `aiohttp.ClientSession` object.
    """
    episodes = await scrape_episodes(session)
    if progress_callback is not None:
        await progress_callback(f"Scraper found {len(episodes)} episodes in feed.")

    update_counter = 0
    duplicate_counter = 0

    for ep in episodes:
        try:
            ep.save()
            update_counter += 1
        except NotUniqueError:
            duplicate_counter += 1

    if progress_callback is not None:
        await progress_callback(
            f"Added {update_counter} entries. {duplicate_counter} were duplicates."
        )


async def add_missing_mp3_urls(session, progress_callback=None):
    """
    Checks which episodes do not have a url to the episode audio and tries to
    update them. This involves a separate page scrape for EACH episode we are
    trying to add and can potentially take a long time (more than a minute).
    The function must be passed an `aiohttp.ClientSession` object.
    """
    episodes_to_process = Episode.missing_audio
    num_episodes = len(episodes_to_process)
    if progress_callback is not None:
        await progress_callback(f"{num_episodes or 'No'} episodes to process")
    for number, ep in enumerate(episodes_to_process):
        if progress_callback is not None:
            await progress_callback(
                f"Processing episode {number+1} of {num_episodes}..."
            )
        ep.update(mp3_url=await scrape_mp3_url(session, ep))


async def refresh_database(progress_callback=None):
    """
    Wraps `add_untracked_episodes` and `add_missing_mp3_urls` in one operation,
    opening up only a single aiohttp client session.
    """
    async with aiohttp.ClientSession() as session:
        await add_untracked_episodes(session, progress_callback)
        await add_missing_mp3_urls(session, progress_callback)


async def drop_episodes(progress_callback=None):
    """
    WARNING: this will ERASE all episodes from the database!
    """
    if progress_callback is not None:
        await progress_callback("Dropping all episodes...")
    Episode.drop_collection()
    if progress_callback is not None:
        await progress_callback("Done")
