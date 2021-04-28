import discord
from discord.ext import commands, tasks
from functools import partial

from config import BOT_TOKEN, COMMAND_PREFIX
from database import add_missing_mp3_urls, add_untracked_episodes

client = discord.Client()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.command(name="refresh")
async def refresh_database(context):
    report_progress = partial(send_message, context)
    await add_untracked_episodes(progress_callback=report_progress)
    await add_missing_mp3_urls(progress_callback=report_progress)


async def send_message(context, message):
    await context.send(message)


print("Running bot...")
bot.run(BOT_TOKEN)
