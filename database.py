# %%

import mongoengine
from mongoengine.errors import NotUniqueError

from scraper import scrape_episodes, add_mp3_url
from config import DATABASE_URL

mongoengine.connect(host=DATABASE_URL)

episodes = scrape_episodes()

# %%

# add_mp3_url(episodes)

# %%

# Add to database:
for ep in episodes:
    try:
        ep.save()
    except NotUniqueError:
        print(f"{ep.title} already exists")

# %%
