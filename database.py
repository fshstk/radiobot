# %%

import mongoengine
from mongoengine.errors import NotUniqueError

from scraper import scrape_episodes, add_mp3_url

database_url = "mongodb://localhost:27017/radiobot"
mongoengine.connect(host=database_url)

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
