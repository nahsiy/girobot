#### Bot Discord de Fsociety

# Import des librairies

import os
import re
import logging
import random
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
import urbandictionary as ud


# Mise en place de la log du bot en mode Verbose

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('discord')
LOGGER.setLevel(logging.DEBUG)

# Sécurisation du tocken

load_dotenv(dotenv_path="config")



# Initialisation du Bot

class BotClient(discord.Client):
    """Discord bot client"""

    async def on_ready(self):
        """The Discord client is ready"""
        game = discord.Game("We are fsociety. We are free. We are awake")
        await self.change_presence(status=discord.Status.online, activity=game)

# Définition des commandes

    async def on_message(self, message):
       
        bot_commands = {
            "!ping": self.ping,
            "!urban": self.urbandef,
            "!echo": self.echo,
            "!help": self.help,
            "!rtfm": self.rtfm,
            "!quote": self.show_quote,
            "!addquote": self.add_quote
        }

        command = message.content.split()[0]
        if command in bot_commands:
            await bot_commands[command](message.channel, message.content[len(command) + 1:])


# Ping

    async def ping(self, channel, _payload):
        """Sends pong"""
        await channel.send("pong")

# Rechercher une définition sur Urban

    async def urbandef(self, channel, term):
        response = ud.define(term)
        if not response:
            await channel.send("N'existe pas dans la BDD d'Urban")
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

# Echo

    async def echo(self, channel, phrase):
        """Repète Jacquot"""
        await channel.send(phrase + " ducon")

# RTFM

    async def rtfm(self, channel, _payload):
        await channel.send("Lis le putain de manuel !")

# HELP

    async def help(self, channel, _payload):
        embed = discord.Embed(title="Help", description="**Commandes Disponibles**", color=0x0392E1)
        embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
        embed.add_field(name="!ping",value="Vérifie que le bot est opérationnel",inline=True)
        embed.add_field(name="!urban",value="Effectue une recherche d'un terme sur le site urban dictionary",inline=True)
        embed.add_field(name="!rtfm",value="Indique de lire le putain de manuel",inline=False)
        embed.add_field(name="!quote",value="Affiche une citation d'un membre du serveur qui a retenu l'attention",inline=False)
        embed.add_field(name="!addquote",value="Ajoute une citation d'un membre dans la liste des quotes \n Usage : !addquote pseudo - citation",inline=False)
        await channel.send(embed=embed)

# Quote
### Choisit une quote de la list ou mode random
    async def show_quote(self, channel, user_choice):
        
        with open("quote.json") as quote_file:
            list_quotes = json.load(quote_file)
        if user_choice:
            quote = list_quotes[int(user_choice)]
        else:
            quote = random.choice(list_quotes)
        embed = discord.Embed(title="Quote", description=quote, color=0x0392E1)
        embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
        await channel.send(embed=embed)

### Ajouter une quote   

    async def add_quote(self, channel, quote):

        with open("quote.json") as quote_file:
            list_quotes = json.load(quote_file)
        list_quotes.append(quote)
        with open("quote.json","w") as quote_file:
            json.dump(list_quotes, quote_file)
        embed = discord.Embed(title="Quote", description="La quote a été ajoutée", color=0x0392E1)
        embed.set_thumbnail(url="https://share.yishan.io/images/quote.png")
        await channel.send(embed=embed)


fsociety = BotClient()
fsociety.run(os.getenv("TOKEN"))