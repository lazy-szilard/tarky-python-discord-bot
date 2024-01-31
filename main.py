import discord
import os
from typing import Final
from discord import app_commands as apc
from discord.ext import commands
from grp import analysecommands
from dotenv import load_dotenv
from discord import Intents, Message
import logging

# Set up the logging configuration
logging.basicConfig(level=logging.NOTSET,
                    format='%(asctime)s %(levelname)-8s %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents = intents)

@bot.event
async def on_ready():
    """Prints a message when the bot is ready."""
    logging.info(f'{bot.user} is online!')
    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logging.error(f"An error occurred while syncing: {e}")

bot.tree.add_command(analysecommands.Analyse(bot))


def main() -> None:
    """Starts the bot."""
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()