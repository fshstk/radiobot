import discord
from discord.ext import commands, tasks
from functools import partial

from config import BOT_TOKEN, COMMAND_PREFIX
from database import add_missing_mp3_urls, add_untracked_episodes

client = discord.Client()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.command(name="refresh")
async def refresh_database(context):
    """
    Update the episode database by scraping the CBA newsfeed. This may take a
    long time, especially when called for the first time on an empty database,
    but progress is reported periodically via the `progress_callback` function.
    """
    reply = await context.send("Refreshing database...")
    report_progress = partial(amend_message, reply)
    await add_untracked_episodes(progress_callback=report_progress)
    await add_missing_mp3_urls(progress_callback=report_progress)


async def amend_message(message, string):
    """
    Amend the passed `message`, replacing its contents with `string`.
    (`message` must have type `discord.Message`)
    """
    await message.edit(content=string)


print("Running bot...")
bot.run(BOT_TOKEN)
