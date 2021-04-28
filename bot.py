import discord
from discord.ext import commands, tasks
from functools import partial
from datetime import datetime

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
    report_progress = partial(amend_embed, reply)
    await add_untracked_episodes(progress_callback=report_progress)
    await add_missing_mp3_urls(progress_callback=report_progress)


async def amend_embed(message, content_to_add):
    """
    Amend the passed `message` by adding `content_to_add` as a new line to the
    message embed's description. If no embed exists a new one will be added.
    (`message` must have type `discord.Message`)
    """
    old_content = message.embeds[0].description if message.embeds else ""
    new_content = old_content + "\n" + content_to_add
    new_embed = discord.Embed.from_dict({"description": new_content})
    await message.edit(embed=new_embed)


print("Running bot...")
bot.run(BOT_TOKEN)
