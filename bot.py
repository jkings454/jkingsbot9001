import random
import logging

import discord
from discord.ext import commands
from util import config
from util.prefixes import get_prefix
from util.prefixes import get_server_prefix, get_user_prefix
from util.prefixes import set_server_prefix, set_user_prefix

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

version = "0.0.2"

description = "a bot that needs more gay"

conf = config.Config()

bot = commands.Bot(get_prefix, pm_help=True, description=description)



game = random.choice(conf.settings["games"])
startup_extensions = ["cogs.rng", "cogs.fun"]

@bot.event
async def on_ready():
    """
    Startup code
    """
    print("\\\\HELLO SEXY\\\\")
    logger.info("janitorbot9001 started... hello world!")

    await bot.change_presence(game=discord.Game(name=game))

@bot.event
async def on_server_join(server):
    """
    Code to be implemented when a server is joined.
    """
    conf.settings["servers"] = {server.id: {}}
    conf.save()

@bot.event
async def on_message(message : discord.Message):
    """
    Code executed whenever a message is sent.
    """
    if "i'm gay" in message.content.lower():
        await bot.add_reaction(message, "🏳️‍🌈")

    await bot.process_commands(message)

@bot.command()
async def about():
    """
    sends a message with the bot's information, including an invite link.
    """
    info = await bot.application_info()
    emb = discord.Embed()
    emb.set_thumbnail(url=info.icon_url)
    emb.title = "About jkingsbot9000"
    emb.description = "jkingsbot9001, a very gay discord bot"
    emb.colour = discord.Color.purple()
    emb.add_field(name="Author", value=info.owner.name)
    emb.add_field(name="version", value=version)
    emb.add_field(name="description", value=info.description, inline=False)
    emb.add_field(name="invite link", value=discord.utils.oauth_url(info.id), inline=False)
    await bot.say(embed=emb)

@bot.group(pass_context=True)
async def prefix(ctx):
    """
    A group of commands dealing with prefixes.
    """
    if ctx.invoked_subcommand is None:
        await bot.say(
            "Usage: j.prefix [user/server] [subcommand] [parameters]."
            + "\nThe following subcommands are available: get, set.")

@prefix.group(pass_context=True)
async def user(ctx):
    """
    User prefix group.
    """
    if ctx.invoked_subcommand is None:
        await user_get(ctx)

@user.command(pass_context=True, name="get")
async def user_get(ctx):
    """
    get's the user's prefix
    """
    user_prefix = get_user_prefix(ctx.message.author)
    if user_prefix is None:
        await bot.say("You don't have a custom prefix!")
    else:
        await bot.say("Your custom prefix is `{}`".format(user_prefix))

@user.command(pass_context=True, name="set")
async def user_set(ctx, prefix : str):
    """
    sets the user's prefix.
    """
    set_user_prefix(ctx.message.author, prefix)
    await bot.say("{0}, now you can invoke me using the prefix: `{1}`".format(
        ctx.message.author.mention, prefix))

@prefix.group(pass_context=True, name="server")
async def server_group(ctx):
    pass

@server_group.command(pass_context=True, name="get")
async def server_get(ctx):
    """ 
    gets the server's prefix.
    """
    server_prefix = get_server_prefix(ctx.message.server)
    if server_prefix is None:
        await bot.say("This server doesn't have a custom prefix!")
    else:
        await bot.say("This server's custom prefix is `{}`".format(server_prefix))

@server_group.command(pass_context=True, name="set")
async def server_set(ctx, prefix : str):
    """
    sets the users prefix. requires the manage_server permission.
    """
    if not(ctx.message.channel.permissions_for(ctx.message.author).manage_server):
        await bot.say("You require the \"manage server\" permissions to invoke this command.")
        return

    set_server_prefix(ctx.message.server, prefix)
    await bot.say("now you can invoke me using the prefix: `{}` on this server.".format(prefix))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as ex:
            exc = "{}: {}".format(type(ex).__name__, ex)
            print("Failed to load extension {}\n{}".format(extension, exc))

    bot.run(conf.settings["token"])
