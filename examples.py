from typing import Final
import os
import requests
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
#from responses import get_response

import logging
import datetime

API_URL = 'http://127.0.0.1:5000/analyse'

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')


# loading token fom a safe place
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# bot setup
intents: Intents = Intents.default()
intents.message_content = True
#client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix='>', intents=intents)


# handing Bot Startup
        
@bot.event
async def on_ready() -> None:
    """Prints a message when the bot is ready."""
    logging.info(f'{bot.user} is online!')

# handling incoming messages
    
@bot.event
async def on_message(message: Message) -> None:
    """Responds to messages that mention the bot."""
    if message.author == bot.user or message.author.bot:  # Ignore messages from itself and other bots
        return
    if message.content.startswith('%'):
        try:
            await bot.process_commands(message)
        except Exception as e:
            logging.error(f"An error occurred while processing the command: {e}")
    
    logging.info(f"{str(message.author)} said {str(message.content)} in {str(message.channel)}")



# commands setup

@bot.command(name='analysecolour')
async def analysecolour(ctx, image_url):
    """Analyses the colors of an image and sends the result to Discord."""
    try:
        # Send an HTTP POST request to the Flask API
        response = requests.post(API_URL, json={'image_url': image_url})

        # Check the response from the API
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                # Extract color information from the API response
                result = data['results']

                # Format the color information for display
                formatted_message = (
                    f"Dominant Color: {result['dominant']}\n"
                    f"Support Color: {result['support']}\n"
                    f"Accent Colors: {', '.join(result['accent'])}"
                )

                # Delete the bot's previous message
                await ctx.message.delete()

                # Send the formatted color information
                await ctx.send(formatted_message)
            else:
                await ctx.send(f"API Error: {data['error']}")
        else:
            await ctx.send(f"API Error: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred while processing the command: {e}")

@bot.command(name='test')
async def test_command(ctx):
    await ctx.send('This is a test command!')

# main entry point
    
def main() -> None:
    """Starts the bot."""
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()