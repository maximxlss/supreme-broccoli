# discord-printer

## Dependencies

- Python 3
- `Discord.py` - `pip install discord.py`
- PIL - `pip install Pillow`
- requests - `pip install requests`
- Discord guilds with color emojis. Emojis can be generated with [a script](./pixels-generator/). Insert their ids into main.py. You need to invite bot into them.

## Description

Discord bot that prints images as emojis.
Example:

`!print 38` with image attached (where 38 is width in emojis)
![example in action](./example.png)

I remember that it had working gif animation system, but I broke it.

Prints slowly because of discord's rate limits. Code is not optimized at all (image gets resized several times instead of one, color select is terrible, etc.)