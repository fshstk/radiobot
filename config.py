import os
from dotenv import load_dotenv

# Load env variables from .env file if present:
# (Existing env variables will not be overwritten.)
load_dotenv()

# This is the URL to the specific radio show's RSS feed that we want to scrape.
# It will have a format similar to: "https://cba.fro.at/series/RADIOSHOW/feed".
# Note that this is only tested on a single show and will probably only work for
# shows from the Cultural Broadcasting Archive (CBA):
FEED_URL = os.getenv("FEED_URL")

# URL to the database used to store radio show data. Must be MongoDB-compatible:
DATABASE_URL = os.getenv("DATABASE_URL")
