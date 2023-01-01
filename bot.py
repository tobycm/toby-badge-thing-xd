#!/usr/bin/env python3

"""
Discord Bot for retrieving info
"""

from discord import Intents, Member
from discord.ext.commands import Bot
from discord.ext.ipc import Server, ClientPayload

bot = Bot(
    command_prefix = "asdadfasda",
    intents = Intents.all()
)

ipc = Server(bot, secret_key="idk xd")

async def startup_tasks():
    """
    Run on bot start up
    """

    await ipc.start()

@Server.route()
async def get_user_data(self, data: ClientPayload) -> dict:
    """
    Return user data (avatar, name and discriminator, status)
    """

    user: Member = self.get_guild(999104580396789832).get_member(487597510559531009)
    return {
        "avatar_url": user.avatar.url,
        "name": f"{user.name}#{user.discriminator}",
        "status": user.raw_status
    }

bot.setup_hook = startup_tasks

bot.run(token = "MTAyMTU3Njg4MzczMDY2MTQyNg.Gf-knx.OIQsONoKAkgnd1urM8LntEAt7m_5TL-7zDw-xw")
