#!/usr/bin/env python3

"""
Send user a Discord Badge (very cool ik)
"""

from io import BytesIO
from aiohttp import ClientSession
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response

from discord.ext.ipc import Client

from image import make_image

ipc = Client(secret_key="idk xd")

app = FastAPI()

cached_images = {}

@app.on_event("startup")
async def startup_event():
    """
    Run at start up
    """

    app.session = ClientSession()

@app.get(
    "/badge_hehe",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class = Response
)
async def badge_hehe():
    """
    Generate a Discord badge
    """

    data = await ipc.request("get_user_data", user_id=487597510559531009)

    if data["status"] in cached_images:
        image: BytesIO = cached_images[data["status"]]
    else:
        image = await make_image(
            app.session,
            data["avatar_url"],
            data["status"],
            data["name"]
        )

        cached_images[data["status"]] = image

    response = Response(content = image.read(), media_type = "image/png")
    image.seek(0)
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port=3213, reload = True)
