import asyncio, discord, aiohttp, re, html, random
from   discord.ext import commands
from   Cogs import Utils, Message, DisplayName, PickList, DL
from   urllib.parse import quote

def setup(bot):
    settings = bot.get_cog("Settings")
    bot.add_cog(E926(bot, settings))

class E926(commands.Cog):

    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.ua = "github_eggtoaster_corpbot.pr redtux/1.0" # "redtux" part is my e926 username, so the site maintainer can contact me if there's a problem
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    async def _getPost(self, query : str):
        headers = {"User-agent" : self.ua}
        post = None
        try:
            arg = ""
            if query is not None:
                arg = "&tags={}".format(quote(query))
            response = await DL.async_json("https://e926.net/posts.json?limit=10{}".format(arg), headers=headers)
            post = response["posts"][random.randint(0,9)]
        except Exception as e:
            print(e)
            return False
        return post

    @commands.command(aliases=["e9"])
    async def e926(self, ctx, *, query : str = None):
        """Grabs a post from e926. (SFW only)"""

        message = await ctx.send("Surfing the internet...")
        post = await self._getPost(query)
        if post:
            desc = "No description provided."
            if post["description"] != "":
                desc = post["description"]
            elif query is not None:
                desc = "Search query: {}".format(query)
            await Message.Embed(
                title = "A post from e926",
                color = ctx.author,
                description = desc,
                url = "https://e926.net/posts/{}".format(post["id"]),
                image = post["file"]["url"],
                thumbnail = post["preview"]["url"],
                footer = {"text": "powered by e926", "icon_url": "https://e926.net/favicon.ico"}
            ).send(ctx, message)
        elif post == False:
            await message.edit(content="Error retrieving post data")
        else:
            await message.edit(content="No results found for that query.")
