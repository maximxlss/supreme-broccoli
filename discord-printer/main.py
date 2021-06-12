from discord import *
from time import time
from asyncio import sleep
from PIL import Image, ImageEnhance
from itertools import zip_longest
import requests
from math import sqrt

client = Client()

emojis = []

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def hex_to_rgb(hex):
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

def closest_color(colors, rgb):
    r, g, b = rgb
    color_diffs = []
    for color in colors:
        cr, cg, cb = color
        mean = (r + cr)/2
        color_diff = (2 + mean/256)*(r - cr)**2 + 4*(g - cg)**2 + (2 + (255-mean)/256)*(b - cb)**2
        color_diffs.append((color_diff, color))
    return min(color_diffs, key=lambda x: x[0])[1]

getcolor = lambda rgb: utils.get(emojis, name=rgb_to_hex(rgb))

def printimg(img, maxwidth, frame):
    img = img.convert(mode="RGB")
    img.seek(frame)
    img.thumbnail((maxwidth, 100), Image.ANTIALIAS)
    #converter = ImageEnhance.Color(img)
    #img = converter.enhance(2)
    msg = ""
    for y in range(img.height):
        for x in range(img.width):
            msg += str(getcolor(closest_color(colors, img.getpixel((x,y)))))
        if len(msg) > 2000 - img.width*28:
            yield msg
            msg = ""
        else:
            msg += "\n"

colors = []

@client.event
async def on_ready():
    global colors
    global emojis
    emojis = client.get_guild(853008775447445564).emojis + client.get_guild(853009024734986250).emojis
    colors = [hex_to_rgb(emoji.name) for emoji in emojis]
    print("redy")
    
@client.event
async def on_message(message):
    global dontprint
    if message.author == client.user:
        return

    if message.attachments != [] and message.content.lower().strip().startswith("!print"):
        try:
            maxwidth = int(message.content.lower().strip()[6:])
        except (IndexError, ValueError):
            maxwidth = 26
        r = requests.get(message.attachments[0].url)
        with open('tempimage', 'wb') as outfile:
            outfile.write(r.content)
        img = Image.open('tempimage')
        imgmsg = []
        frame = 0
        iterr = printimg(img, maxwidth, frame)
        while 1:
            try:
                msg = next(iterr)
            except StopIteration:
                break
            imgmsg.append(await message.channel.send(msg))
            # await sleep(0.7)
        # await imgmsg[-1].add_reaction("🛑")
        # cache_msg = await imgmsg[-1].channel.fetch_message(imgmsg[-1].id)
        # frame += 1
        # reaction_count = cache_msg.reactions[0].count
        # while not reaction_count > 1:
        #     try:
        #         iterr = printimg(img, maxwidth, frame)
        #         for imsg in imgmsg:
        #             cache_msg = await imgmsg[-1].channel.fetch_message(imgmsg[-1].id)
        #             reaction_count = cache_msg.reactions[0].count
        #             if reaction_count > 1:
        #                 break
        #             try:
        #                 msg = next(iterr)
        #             except StopIteration: 
        #                 break
        #             await imsg.edit(content=msg)
        #             #await sleep(0.7)
        #         frame += 1
        #     except EOFError:
        #         if frame == 1:
        #             return
        #         frame = 0
        #     cache_msg = await imgmsg[-1].channel.fetch_message(imgmsg[-1].id)
        #     reaction_count = cache_msg.reactions[0].count

client.run('NzAwMjAzMTMzNTYwOTQ2NzI4.Xpfg_A.Ie67iMTXqaQqt6gS2m0YFmPvavY')
