#!/usr/bin/env python3

"""
Send user a Discord Badge (very cool ik)
"""

import os
from multiprocessing import Process

import uvicorn
from dotenv import load_dotenv

from bot import bot
from web_server import app

load_dotenv()

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("No token provided")

os.makedirs("./run", exist_ok=True)

if __name__ == "__main__":
    Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={"uds": "./run/toby-badge-thing-xd.sock"},
    ).start()
    Process(target=bot.run, args=(TOKEN,)).start()
