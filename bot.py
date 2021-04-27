import discord
from discord.ext import commands, tasks

from config import BOT_TOKEN, COMMAND_PREFIX

client = discord.Client()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.command(name="radio")
async def radio(ctx):
    await ctx.send(f"hello {ctx.message.author.name}!")
    return


print("Running bot...")
bot.run(BOT_TOKEN)
