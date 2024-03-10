import re
import subprocess
import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
from LoggerGenerator import LoggerGenerator
from pytube import YouTube

# set up logging
LOG = LoggerGenerator.create_logger("coda", log_level=logging.INFO)

# grab env vars
load_dotenv()
DISCORD_KEY = os.getenv("DISCORD_KEY")

# set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, log_level=logging.INFO)


@bot.event
async def on_ready():
    LOG.info("bot logged in as %s", bot.user)
    await bot.tree.sync()


@bot.tree.command(
    name="rip_all",
    description="Grab audio from a youtube link.  Please do not rip copyrighted material.",
)
async def rip(interaction: discord.Interaction, url: str):
    LOG.info("Ripping audio from %s", url)
    await interaction.response.defer(thinking=True)

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(filename_prefix="coda_")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".mp3"

        # Use ffmpeg to convert the file to mp3
        cmd = f'ffmpeg -i "{output_file}" -vn -ab 128k -ar 44100 -y "{new_file}"'
        subprocess.run(cmd, shell=True)

        # Check the size of the file
        if os.path.getsize(new_file) > 8e6:  # Adjusted to 8MB for Discord limit
            LOG.info("%s too large", new_file)
            response = "File too large to send, sorry!"
            await interaction.followup.send(content=response)
            return

        file = discord.File(new_file)
        response = f"Here's your audio! ({yt.title}, {os.path.getsize(new_file) / 1e+6:.2f} MB)"
        await interaction.followup.send(content=response, file=file)

        os.remove(new_file)
        os.remove(output_file)
    except Exception:
        await interaction.followup.send(content=f"I wasn't able to rip that!")


@bot.tree.command(
    name="rip_from_timestamp",
    description=(
        "Rip five seconds of audio from a yt link with timestamp"
        "  Please do not rip copyrighted material."
    ),
)
async def rip_from_timestamp(interaction: discord.Interaction, url: str):
    LOG.info("Ripping audio from %s", url)
    await interaction.response.defer(thinking=True)

    try:
        timestamp_match = re.search(r"t=(\d+)s?", url)
        start_seconds = timestamp_match.group(1) if timestamp_match else "0"

        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(filename_prefix="coda_")
        base, ext = os.path.splitext(output_file)
        new_file = base + ".mp3"

        cmd = f'ffmpeg -ss {start_seconds} -i "{output_file}" -t 4.8 -vn -ab 128k -ar 44100 -y "{new_file}"'
        subprocess.run(cmd, shell=True)

        # Check the size of the file
        if os.path.getsize(new_file) > 8e6:  # Adjusted to 8MB for Discord limit
            LOG.info("%s too large", new_file)
            response = "File too large to send, sorry!"
            await interaction.followup.send(content=response)
            return

        file = discord.File(new_file)
        response = f"Here's your audio! ({yt.title}, {os.path.getsize(new_file) / 1e+6:.2f} MB)"
        await interaction.followup.send(content=response, file=file)

        os.remove(new_file)  # Clean up after sending
        os.remove(output_file)
    except Exception as e:
        LOG.error(f"Error ripping audio: {e}")
        await interaction.followup.send(content=f"I wasn't able to rip that!")


bot.run(DISCORD_KEY)
