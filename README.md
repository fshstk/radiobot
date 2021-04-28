# radiobot
Discord bot &amp; web scraper for playing episodes from the archive of the
Cultural Broadcasting Archive (CBA)

## Deployment

`Procfile` and `.buildpacks` files for Heroku-compatible deployments are
included, so if you want to deploy your own version of this site it shouldn't be
too complicated. The original bot is hosted and deployed using
[Dokku](https://dokku.com/).

You should be able to deploy this app in four easy steps:
1. Install [Heroku](https://heroku.com).
2. Clone this repository.
3. Follow the Discord instructions on how to generate a bot token
4. Follow the Heroku instructions on how to deploy an app.

Additionally, you must make sure the following env variables are set in your app
dashboard:

- `COMMAND_PREFIX` command prefix to use for addressing bot, or empty string if
  none
- `ALLOWED_CHANNEL` the bot will only react to commands in channels whose name
  matches this string
- `VOICE_CHANNEL_ID` fixed ID of the voice channel in which to stream
- `BOT_TOKEN` you need to create a bot via the Discord developer portal to get
  one of these
- `FEED_URL` URL to the RSS feed of the radio show you want to track (usually of
  the form `https://cba.fro.at/series/RADIOSHOW/feed`)
- `MONGO_URL` URL to a MongoDB database including access credentials (Note: you
  can use the [MongoDB plug-in](https://github.com/dokku/dokku-mongo) if you are
  using Dokku and it will set this variable up for you automatically. I'm sure
  there's something equivalent for Heroku as well.)

## License

All code is licensed under GPLv3.
