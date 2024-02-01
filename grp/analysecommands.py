import discord
from discord import app_commands as apc
import logging
import requests
import os
from dotenv import load_dotenv
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(rc={'figure.figsize':(11.7,8.27)})

# Set up the logging configuration
logging.basicConfig(level=logging.NOTSET,
                    format='%(asctime)s %(levelname)-8s %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()
API_URL = os.getenv("API_URL")


def hex_to_rgb(hex_value):
  h = hex_value.lstrip('#')
  return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def palette(hex_colors):
    sns.set()
    rgb_colors = list(map(hex_to_rgb, hex_colors))
    sns.palplot(rgb_colors)
    plt.savefig("plot.png")
    plt.clf()


class Analyse(apc.Group):
    """Manage Analyse commands"""
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command()
    async def colour(self, interaction: discord.Interaction,image_url: str):
        """Analyse the color of a frame"""
        await interaction.response.defer()
        try:
            # Send an HTTP POST request to the Flask API
            response = requests.post(API_URL, json={'image_url': image_url})

            # Check the response from the API
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    # Extract color information from the API response
                    result = data['results']
                    palette(result)
                    # Format the color information for display
                    #formatted_message = (
                        #f"Dominant Color: {result['dominant']}\n"
                        #f"Support Color: {result['support']}\n"
                        #f"Accent Colors: {', '.join(result['accent'])}"
                    #)
                    
                    # Send the formatted color information
                    await interaction.followup.send(file=discord.File("plot.png"))
                    os.remove('plot.png')
                else:
                    await interaction.followup.send(f"API Error: {data['error']}")
            else:
                await interaction.followup.send(f"API Error: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while processing the command: {e}")

    @apc.command()
    async def ratio(self, interaction: discord.Interaction, ratio: str):
        """Gives you info on the aspect ratio of a frame"""
        await interaction.response.send_message('command not implemented yet')