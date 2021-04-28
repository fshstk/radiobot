import mongoengine
from mongoengine.errors import NotUniqueError

from config import DATABASE_URL
from schema import Episode
from scraper import scrape_episodes, scrape_mp3_url

mongoengine.connect(host=DATABASE_URL)


async def add_untracked_episodes(progress_callback=None):
    """
    Scrapes the RSS feed for all available episodes, then tries to add them to
    the database. Existing episodes will be rejected by the database backend as
    each episode must have a unique page url.
    """
    episodes = await scrape_episodes()
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


async def add_missing_mp3_urls(progress_callback=None):
    """
    Checks which episodes do not have a url to the episode audio and tries to
    update them. This involves a separate page scrape for EACH episode we are
    trying to add and can potentially take a long time (more than a minute).
    """
    episodes_to_process = Episode.missing_audio

    if len(episodes_to_process) == 0:
        if progress_callback is not None:
            await progress_callback("No episodes to process")
        return
    for number, ep in enumerate(episodes_to_process):
        if progress_callback is not None:
            await progress_callback(
                f"Processing episode {number+1} of {len(episodes_to_process)}..."
            )
        ep.update(mp3_url=await scrape_mp3_url(ep))


async def drop_episodes(progress_callback=None):
    """
    WARNING: this will ERASE all episodes from the database!
    """
    if progress_callback is not None:
        await progress_callback("Dropping all episodes...")
    Episode.drop_collection()
    if progress_callback is not None:
        await progress_callback("Done")
