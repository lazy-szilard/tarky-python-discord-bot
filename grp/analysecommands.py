import logging
import os
import asyncio
from dotenv import load_dotenv
from webcolors import hex_to_name
import requests
import discord
from discord import app_commands as apc

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

def identify_color(hex_code):
    try:
        color_name = hex_to_name(hex_code)
        print(f"Color Name: {color_name}")

        color_theories = {
            'RED': "A deeper red can raise blood pressure and elicit fear and foreboding. It can also represent lust, love, and hope.",
            'BLUE': "Can range from calming to cold and isolating, to passive and melancholic.",
            'PINK': "Exudes femininity, innocence, and empathy.",
            'YELLOW': "Signifies idyllic, naivete, and obsessiveness. It can also insinuate madness, insecurity, and illness.",
            'PURPLE': "Has a fantastical and ominous presence, but can also represent erotic and metaphysical themes.",
            'GREEN': "Most notably suggestive of nature, but can also denote immaturity, corruption, and danger.",
            'ORANGE': "Warm, friendly, and sociable. It also signifies youth, happiness, and exoticism."
        }

        # Get color theory based on the color name
        theory = color_theories.get(color_name.upper(), "No specific color theory available.")

        print(f"Color Theory: {theory}")

    except ValueError:
        print("Invalid hex code. Please provide a valid hex code.")
    

# Define a simple Button View class
class Confirm(discord.ui.View):
    def __init__(self, dominant_color, support_color, accent_colors):
        super().__init__()
        self.stop_after = 300
        self.dominant_color = dominant_color
        self.support_color = support_color
        self.accent_colors = accent_colors
    
    async def _stop_listening(self, interaction: discord.Interaction):
        await asyncio.sleep(self.stop_after)
        await interaction.response.send_message('Thanks for using Tarky!', ephemeral=True)
        self.stop()

    def start_timer(self):
        asyncio.create_task(self._stop_listening())

    @discord.ui.button(label='Dominant', style=discord.ButtonStyle.grey)
    async def dominant_color_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'Dominant Color: {self.dominant_color}\n{identify_color(self.dominant_color)}', ephemeral=False)

    @discord.ui.button(label='Support', style=discord.ButtonStyle.grey)
    async def support_color_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'Support Color: {self.support_color}\n{identify_color(self.support_color)}', ephemeral=False)

    @discord.ui.button(label='Accent', style=discord.ButtonStyle.grey)
    async def accent_colors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for color in self.accent_colors:
            await interaction.followup.send(f'Accent Color: {color}\n{identify_color(color)}', ephemeral=False)
        

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
                    
                    formatted_result_dict = {'dominant': result[0],
                                            'support': result[1],
                                            'accent': result[2:]}
                    
                    await interaction.followup.send(file=discord.File("plot.png"), view=Confirm(formatted_result_dict['dominant'], formatted_result_dict['support'], formatted_result_dict['accent']))
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