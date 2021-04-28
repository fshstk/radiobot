import discord
from discord.ext import commands
from functools import partial
from datetime import datetime
from asyncio import sleep

from config import BOT_TOKEN, COMMAND_PREFIX, VOICE_CHANNEL_ID
from database import refresh_database, drop_episodes

client = discord.Client()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.command(name="refresh")
async def refresh(context):
    """
    Update the episode database by scraping the CBA newsfeed. This may take a
    long time, especially when called for the first time on an empty database,
    but progress is reported periodically via the `progress_callback` function.
    """
    reply = await context.send("Refreshing database...")
    report_progress = partial(amend_embed, reply)
    await refresh_database(report_progress)
    await amend_embed(reply, "Done!")


# TODO: this command should only be available to admins/bot owner
@bot.command(name="nuke")
async def reset_database(context):
    """
    This will ERASE THE ENTIRE DATABASE. Use with caution. (You can always
    rebuild it with `refresh`.)
    """
    reply = await context.send("Nuking database...")
    report_progress = partial(amend_embed, reply)
    await drop_episodes(progress_callback=report_progress)


@bot.command(name="play")
async def play(context, url):
    """
    Play the given URL in the channel hardcoded in `config.VOICE_CHANNEL_ID`.
    If the bot is already playing, it will stop and restart.
    """
    await stop(context)  # if the bot is already playing, stop first
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    print(f"{timestamp()} Playing {url} in {voice_channel.name}")

    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(url))
    while voice_client.is_playing():
        await sleep(1)
    print(f"{timestamp()} Finished playing.")
    await voice_client.disconnect()


@bot.command(name="stop")
async def stop(context):
    """
    Disconnect the bot from all voice clients (should only be one anyway)...
    """
    if not bot.voice_clients:
        return  # nothing to do here...
    await context.send("Stopping...")
    for vc in bot.voice_clients:
        return await vc.disconnect()


def timestamp():
    return datetime.now().strftime("[%H:%M:%S]")


async def amend_embed(message, content_to_add, max_lines=10):
    """
    Amend the passed `message` by adding `content_to_add` as a new line to the
    message embed's description. If no embed exists a new one will be added.
    (`message` must have type `discord.Message`) Only the last `max_lines` of
    the message will be shown. If the message exceeds this number of lines it
    will be truncated down, keeping the most recent messages. (Discord has a
    limit of 2048 chars on embed descriptions, so you should keep the value of
    `max_lines` low.)
    """
    new_content = f"{timestamp()} {content_to_add}"
    print(new_content)  # Log the message to console...

    old_content = message.embeds[0].description if message.embeds else ""
    # Truncate down to the last (max_lines-1) lines:
    old_content = "\n".join(old_content.splitlines()[-(max_lines - 1) :])

    new_embed = discord.Embed(description=f"{old_content}\n`{new_content}`")
    await message.edit(embed=new_embed)


@bot.event
async def on_ready():
    print(f"{timestamp()} Bot is ready and online!")


@bot.event
async def on_command_error(_, error):
    """
    In case there's an error, just log it to console instead of crashing.
    """
    print(error)


bot.run(BOT_TOKEN)
