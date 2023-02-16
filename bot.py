#!/usr/bin/env python3

"""
Discord Bot for retrieving info
"""

import os

from discord import Intents
from discord.ext.commands import Bot
from discord.ext.ipc import ClientPayload, Server
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
IPC_PORT = os.getenv("IPC_PORT", 8765)
MULTICAST_PORT = os.getenv("MULTICAST_PORT", 8766)

if TOKEN is None:
    raise ValueError("No token provided")

bot = Bot(command_prefix="!", intents=Intents().all())

ipc = Server(
    bot, secret_key=TOKEN, standard_port=IPC_PORT, multicast_port=MULTICAST_PORT
)


async def startup_tasks():
    """
    Run on bot start up
    """

    await ipc.start()


bot.setup_hook = startup_tasks


@Server.route()
async def get_user_data(self: Bot, data: ClientPayload) -> dict:
    """
    Return user data (avatar, name and discriminator, status)
    """

    user = self.get_guild(999104580396789832).get_member(487597510559531009)
    return {
        "avatar_url": user.avatar.url,
        "name": f"{user.name}#{user.discriminator}",
        "status": user.raw_status,
    }


if __name__ == "__main__":
    bot.run(TOKEN)
