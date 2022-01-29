"""Bot discord de Giroll"""

# Import des librairies
from distutils.log import error
from email import message
from lib2to3.pgen2.token import ASYNC
import os
import discord
from discord.ext import commands
import datetime
import hashlib
import sqlite3
from pyparsing import Word
from dotenv import load_dotenv

# Mise en place du Prefixe
bot = commands.Bot(command_prefix='!')

load_dotenv(dotenv_path="config")


# Initialisation du Bot
@bot.event
async def on_ready():
    game = discord.Game("with the API")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Connected to discord")


# Ping
@bot.command()
async def ping(ctx):
    await ctx.send("pong")
    print("ping envoyé")


"""<QUOTES>"""
# Verifier que la base de données est créée et lancée
db = sqlite3.connect('c:/home/yishan/girobot/quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user TEXT, message TEXT, date_added TEXT)')
print("Loaded database")
db.commit()


# Menu Help
@bot.command()
async def quotehelp(ctx):
    embed = discord.Embed(name="help")
    embed.set_author(name="Commandes disponibles:")
    embed.add_field(name="Pour quoter:", value="!quote @[user] [message]", inline=False)
    embed.add_field(name="Pour choisir un utilisateur particulier:", value="!getquote @[user]", inline=False)
    embed.add_field(name="Obtenir une quote aléatoire:", value="!random", inline=False)
    await ctx.send(embed=embed)


# Effectuer une quote
@bot.command()
async def quote(ctx, *, message: str):
    # split the message into words
    string = str(message)
    temp = string.split()

    # take the username out
    user = temp[0]
    del temp[0]

    # join the message back together
    text = " ".join(temp)

    if user[1] != '@':
        await ctx.send("Utilise ```@[user] [message]``` pour quoter un utilisateur")
        return

    unique_id = hash(user + message)

    # date et heure de la quote :
    time = datetime.datetime.now()
    formatted_time = str(time.strftime("%d-%m-%Y %H:%M"))

    # Cherche si la quote est déjà dans la BDD 
    cursor.execute("SELECT count(*) FROM quotes WHERE hash = ?", (unique_id,))
    find = cursor.fetchone()[0]

    if find > 0:
        return

    # Sinon on l'ajoute
    cursor.execute("INSERT INTO quotes VALUES(?,?,?,?)", (unique_id, user, text, formatted_time))
    await ctx.send("Quote ajoutée avec succès")

    db.commit()

    # Nombre de quotes dans la BDD
    rows = cursor.execute("SELECT * from quotes")

    # log
    print(str(len(rows.fetchall())) + ". added - " + str(user) + ": \"" + str(
        text) + "\" to database at " + formatted_time)


# Afficher une quote aléatoirement
@bot.command()
async def random(ctx):
    cursor.execute("SELECT user,message,date_added FROM quotes ORDER BY RANDOM() LIMIT 1")
    query = cursor.fetchone()

    # log
    print(query[0] + ": \"" + query[1] + "\" printed to the screen " + str(query[2]))

    # Sortie en embed
    style = discord.Embed(name="responding quote", description="- " + str(query[0]) + " " + str(query[2]))
    style.set_author(name=str(query[1]))
    await ctx.send(embed=style)


# Afficher une quote d'un utilisateur précis aléatoirement
@bot.command()
async def getquote(ctx, message: str):
    # sanitise name
    user = (message,)

    try:
        # query random quote from user
        cursor.execute("SELECT message,date_added FROM quotes WHERE user=(?) ORDER BY RANDOM() LIMIT 1", user)
        query = cursor.fetchone()

        # adds quotes to message
        output = "\"" + str(query[0]) + "\""

        # log
        print(message + ": \"" + output + "\" printed to the screen " + str(query[1]))

        # Embed
        style = discord.Embed(name="responding quote", description="- " + message + " " + str(query[1]))
        style.set_author(name=output)
        await ctx.send(embed=style)

    except Exception:

        await ctx.send("Il n'y a pas de quotes pour cet utilisateur")

    db.commit()


'''</QUOTES>'''

'''<NOSTALGIE BOT IRC>'''


# Barman


@bot.command()
async def cafe(ctx, member: discord.Member):
    user = member.mention
    await ctx.send(f"{ctx.author.display_name} offre un café à {user}")


@cafe.error
async def cafe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Girobot offre un café à {ctx.author.mention}")


@bot.command()
async def the(ctx, member: discord.Member):
    user = member.mention
    await ctx.send(f"{ctx.author.display_name} offre un thé à {user}")


@the.error
async def the_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Girobot offre un thé à {ctx.author.mention}")


@bot.command()
async def biere(ctx, member: discord.Member):
    user = member.mention
    await ctx.send(f"{ctx.author.display_name} offre une bière à {user}")


@biere.error
async def biere_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Girobot offre une bière à {ctx.author.mention}")


@bot.command()
async def coca(ctx, member: discord.Member):
    user = member.mention
    await ctx.send(f"{ctx.author.display_name} offre un coca à {user}")


@coca.error
async def coca_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Girobot offre un coca à {ctx.author.mention}")

# Les mots interdits


@bot.event
async def on_message(message):
    await bot.process_commands(message)  # https://stackoverflow.com/questions/62076257/discord-py-bot-event
    if message.author == bot.user:
        return
    msg_content = message.content.lower()
    words_forbidden = ['lol', 'mdr', 'ptdr', 'windows']
    if any(word in msg_content for word in words_forbidden):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, attention à ton langage !")


'''</NOSTALGIE BOT IRC>'''

'''<GESTION DU SERVEUR>'''


@bot.command()
async def rules(ctx):
    await ctx.send("Keep Cool And Use Linux")


@bot.command()
@commands.has_permissions(administrator=True)
async def warning(ctx, membre: discord.Member):
    pseudo = membre.mention
    id = membre.id
    await ctx.send(f"le membre {pseudo} a reçu un avertissement, attention à bien respecter les règles du serveur !")


@warning.error
async def warning_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande est : !warning @pseudo")


'''</GESTION DU SERVEUR>'''

'''TOKEN'''
bot.run(os.getenv("TOKEN"))
