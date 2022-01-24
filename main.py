<<<<<<< HEAD
##### Bot discord de Giroll #####

=======
#### Bot Discord de Giroll
>>>>>>> 863ad47434d41f14e5bfe1b3d4f0cc35ebb315f4

# Import des librairies

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import hashlib
import sqlite3

# Prefixe
bot = commands.Bot(command_prefix='!')

#check if database is made and load it
db = sqlite3.connect('/home/yishan/girobot/quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user TEXT, message TEXT, date_added TEXT)')
print("Loaded database")
db.commit()

@bot.event
async def on_ready():
    print ("Connected to discord")

## COMMANDES ##

# Ping

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("pong")
    print ("ping envoyé")

# Menu HELP

@bot.command()
async def quotehelp(ctx):
    embed = discord.Embed(name="help")
    embed.set_author(name="Commandes disponibles:")
    embed.add_field(name="Pour quoter:", value="!quote @[user] [message]", inline=False)
    embed.add_field(name="Pour choisir un utilisateur particulier:", value="!getquote @[user]", inline=False)
    embed.add_field(name="Obtenir une quote aléatoire:", value="!random", inline=False)
    await ctx.send(embed=embed)

# Afficher une quote aléatoirement
@bot.command()
async def random(ctx):

<<<<<<< HEAD
    cursor.execute("SELECT user,message,date_added FROM quotes ORDER BY RANDOM() LIMIT 1")
    query = cursor.fetchone()
=======
load_dotenv()
>>>>>>> 863ad47434d41f14e5bfe1b3d4f0cc35ebb315f4

    #log
    print(query[0]+": \""+query[1]+"\" printed to the screen "+str(query[2]))

    #embeds the output
    style = discord.Embed(name="responding quote", description="- "+str(query[0])+" "+str(query[2]))
    style.set_author(name=str(query[1]))
    await ctx.send(embed=style)


<<<<<<< HEAD
@bot.command()
async def quote(ctx,*, message: str):

    #split the message into words
    string = str(message)
    temp = string.split()

    #take the username out
    user = temp[0]
    del temp[0]

    #join the message back together
    text = " ".join(temp)
    
    if user[1]!='@':
        await ctx.send("Utilise ```@[user] [message]``` pour quoter une personne")
        return
=======
class BotClient(discord.Client):

    async def on_ready(self):
        game = discord.Game("SuperTux")
        await self.change_presence(status=discord.Status.online, activity=game)
>>>>>>> 863ad47434d41f14e5bfe1b3d4f0cc35ebb315f4

    uniqueID = hash(user+message)

<<<<<<< HEAD
    #date and time of the message
    time = datetime.datetime.now()
    formatted_time = str(time.strftime("%d-%m-%Y %H:%M"))
=======
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
>>>>>>> 863ad47434d41f14e5bfe1b3d4f0cc35ebb315f4

    #find if message is in the db already
    cursor.execute("SELECT count(*) FROM quotes WHERE hash = ?",(uniqueID,))
    find = cursor.fetchone()[0]

    if find>0:
        return

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?,?,?)",(uniqueID,user,text,formatted_time))
    await ctx.send("Quote ajoutée avec succès.")

    db.commit()

    #number of words in the database
    rows = cursor.execute("SELECT * from quotes")

    #log to terminal
    print(str(len(rows.fetchall()))+". added - "+str(user)+": \""+str(text)+"\" to database at "+formatted_time)


@bot.command()
async def getquote(ctx,message: str):
    
    #sanitise name
    user = (message,)

    try:
        #query random quote from user
        cursor.execute("SELECT message,date_added FROM quotes WHERE user=(?) ORDER BY RANDOM() LIMIT 1",user)
        query = cursor.fetchone()

        #adds quotes to message
        output = "\""+str(query[0])+"\""

        #log
        print(message+": \""+output+"\" printed to the screen "+str(query[1]))

        #embeds the output to make it pretty
        style = discord.Embed(name="responding quote", description="- "+message+" "+str(query[1]))
        style.set_author(name=output)
        await ctx.send(embed=style)

    except Exception:

        await ctx.send("Pas de quotes trouvées pour cet utilisateur")

    db.commit()    


<<<<<<< HEAD
bot.run("NTQzNDQ5Nzk3NDc5MTA0NTEy.XF2dEA.igaO10IPB_IKSMl8fmUcDP3WzAE")
=======
    async def ping(self, channel, _payload):
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

#    async def echo(self, channel, phrase):
#        await channel.send(phrase + " ")

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


girobot = BotClient()
girobot.run(os.getenv("TOKEN"))
>>>>>>> 863ad47434d41f14e5bfe1b3d4f0cc35ebb315f4
