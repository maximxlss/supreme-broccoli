from discord import *
import json
from mediawiki import MediaWiki
import re

wiki = MediaWiki(lang="ru")
lurk = MediaWiki(url="https://lurkmo.re/api.php")
client = Client()

CHANNEL_ID = 698954006441230356
TOKEN = ""

aliases = (
    'что значит ',
    'что за ',
    'что такое ',
    'what is ',
    "what's ",
    'wtf is ',
    '!wikis ',
    '/wikis ',
    '#wikis ',
    '@wikis ',
    'find on wiki ',
)

lang = "ru"


@client.event
async def on_ready():
    global textch
    textch = client.get_channel(CHANNEL_ID)


@client.event
async def on_voice_state_update(member, before, after):
    global textch
    overwrites = textch.overwrites
    if before.channel != None and after.channel == None:
        try:
            overwrites[member].view_channel = False
        except KeyError:
            overwrites = {**overwrites, member: PermissionOverwrite(view_channel=False)}
        await textch.send("**" + member.display_name + "** вышел из чата")
    elif before.channel == None and after.channel != None:
        try:
            overwrites[member].view_channel = True
        except KeyError:
            overwrites = {**overwrites, member: PermissionOverwrite(view_channel=True)}
        await textch.send("**" + member.display_name + "** присоединился к чату")
    await textch.edit(overwrites=overwrites)


def find(wiki, query):
    try:
        title = wiki.wiki_request(
        {
            "action": "opensearch",
            "search": query,
            "limit": "1",
            "profile": "fuzzy"
        })[1][0].encode().decode('utf-8')
        summ = wiki.wiki_request(
        {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvslots": "*",
            "rvprop": "content"
        })["query"]["pages"][0]["revisions"][ 0]["slots"]["main"]["content"].encode().decode('utf-8')
        summ = re.sub("[\(\[].*?[\)\]]", "", summ)[:100]+"..."
        img = wiki.wiki_request(
        {
            "action": "query",
            "prop": "imageinfo",
            "titles": title,
            "iiprop": "url",
            "iilimit": "1",
            "exsectionformat": "true"
        })["query"]["pages"]
        img = list(img.values())[0]["imageinfo"]["url"].encode().decode('utf-8')
        return (img, summ + "...")
    except KeyError:
        return ("https://image.freepik.com/free-vector/glitch-error-404-page-background_23-2148092637.jpg",
                "Не найдено")


@client.event
async def on_message(message):
    global messagee

    if message.author == client.user:
        return

    if message.content.lower().startswith(aliases):
        for alias in aliases:
            if message.content.lower().startswith(alias):
                query = message.content[len(alias):]

        await message.channel.trigger_typing()
        messagee = []
        embed = Embed(colour=Colour(0x205ce4))

        embed.set_footer(text="Русский язык | Извините, если это лишнее ¯\_(ツ)_/¯")

        (image, summ) = find(lurk, query)
        embed.add_field(name="<:lurklogo:699375011823222875> Lurkmore", value=summ, inline=True)

        (image, summ) = find(wiki, query)
        embed.add_field(name="<:wikilogo:699375877036703835> Wikipedia", value=summ, inline=True)

        embed.set_thumbnail(url=image)
        embed.add_field(name="...",
                        value="[Lurkmore](https://lurkmo.re/?search=" + query.replace(" ","%20") + ") | [Wikipedia](https://" + lang + ".wikipedia.org/?search=" + query.replace(" ","%20") + ")",
                        inline=False)
        embed.add_field(name="...",
                        value="Нажмите на реакцию внизу чтобы сменить язык вики",
                        inline=True)

        messagee = [await message.channel.send(embed=embed), query]
        await messagee[0].add_reaction("🇺🇸")


client.run(TOKEN)
