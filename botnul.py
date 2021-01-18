"""Bot discord de yishan"""
import os
import logging

import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import urbandictionary as ud
from quote import QUOTES  # quotes personnelles

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('discord')
LOGGER.setLevel(logging.DEBUG)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CENSORED_SENTENCES = (
    "ta gueule",
)

CENSORED_WORDS = (
    "tg",
    "menfou",
    "ftg",
    "tg.",
    "tg!",
)



class BotClient(discord.Client):
    """Discord bot client"""

    async def on_ready(self):
        """The Discord client is ready"""
        game = discord.Game("Au nom de la lune, je vais tous vous punir.")
        await self.change_presence(status=discord.Status.online, activity=game)

    async def on_message(self, message):
        """Handle received messages"""
        bot_commands = {
            "!ping": self.ping,
            "!urban": self.urbandef,
            "!echo": self.echo,
            "!help": self.rtfm,
            "!rtfm": self.rtfm,
            "!quote": self.show_random_quote
        }

        words = message.content.split()
        if not words:
            return
        command = words[0]
        if command in bot_commands:
            await bot_commands[command](message.channel, message.content[len(command) + 1:])
        sentence = message.content.strip().lower()
        if sentence in CENSORED_SENTENCES:
            await message.delete()
        elif command in CENSORED_WORDS:
            await message.delete()

    async def ping(self, channel, _payload):
        """Sends pong"""
        await channel.send("pong")

    async def urbandef(self, channel, term):
        """Cherche une def sur Urban"""
        response = ud.define(term)
        if not response:
            await channel.send("Ça existe pas ta merde.")
            return
        response = response[0]
        response.definition = response.definition.replace("[", "**")
        response.definition = response.definition.replace("]", "**")
        response.example = response.example.replace("[", "**")
        response.example = response.example.replace("]", "**")
        embed = discord.Embed(title=term, color=0x0392E1)
        if len(response.definition) > 1000:
            concat = response.definition[:995] + "\n**[...]**"
        else:
            concat = response.definition

        embed.add_field(name="**definition** :\n", value=concat, inline=False)
        embed.add_field(name="**example** :\n", value=response.example)
        embed.set_thumbnail(url="https://share.yishan.io/images/ud.jpg")
        await channel.send(embed=embed)

    async def echo(self, channel, phrase):
        """Repète Jacquot"""
        await channel.send(phrase + " ducon")

    async def show_random_quote(self, channel, _rien):
        """Balance une quote random"""
        quote = random.choice(QUOTES)
        embed = discord.Embed(title="Quote", description=quote, color=0x0392E1)
        embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
        await channel.send(embed=embed)

    async def rtfm(self, channel, _payload):
        """Fuck you"""
        await channel.send("RTFM!")


DISCORD_NUL_BOT = BotClient()
DISCORD_NUL_BOT.run(TOKEN)
