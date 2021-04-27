import mongoengine
from mongoengine.errors import NotUniqueError

from config import DATABASE_URL
from schema import Episode
from scraper import scrape_episodes, scrape_mp3_url

mongoengine.connect(host=DATABASE_URL)


def add_untracked_episodes():
    episodes = scrape_episodes()
    print(f"Scraper found {len(episodes)} episodes in feed.")

    update_counter = 0
    duplicate_counter = 0

    for ep in episodes:
        try:
            ep.save()
            update_counter += 1
        except NotUniqueError:
            duplicate_counter += 1

    print(f"Added {update_counter} entries. {duplicate_counter} were duplicates.")


def add_missing_mp3_urls():
    episodes_to_process = Episode.missing_audio

    if len(episodes_to_process) == 0:
        print("No episodes to process")
        return
    for number, ep in enumerate(episodes_to_process):
        print(f"Processing episode {number+1} of {len(episodes_to_process)}...")
        ep.update(mp3_url=scrape_mp3_url(ep))
    print("Done")
