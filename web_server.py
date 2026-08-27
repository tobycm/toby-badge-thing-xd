import os
from io import BytesIO

from aiohttp import ClientSession
from discord.ext.ipc import Client
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import Response

from image import make_image
from objects import Data

load_dotenv()

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("No token provided")

IPC_PORT = int(os.getenv("IPC_PORT", "8765"))
MULTICAST_PORT = int(os.getenv("MULTICAST_PORT", "8766"))

ipc = Client(secret_key=TOKEN, standard_port=IPC_PORT, multicast_port=MULTICAST_PORT)


class CApp(FastAPI):
    session: ClientSession


app = CApp()

cached_images = {}


@app.on_event("startup")
async def startup_event():
    """
    Run at start up
    """

    app.session = ClientSession()


@app.get(
    "/badge_hehe",
    responses={
        200: {"content": {"image/png": {}}},
        500: {"content": {"text/plain": {}}},
    },
    response_class=Response,
)
async def badge_hehe():
    """
    Generate a Discord badge
    """

    data = await ipc.request("get_user_data", user_id=487597510559531009)
    if data is None:
        return Response(status_code=500)
    data = Data(data.response)

    if data.status in cached_images:
        image: BytesIO = cached_images[data.status]
    else:
        image = await make_image(app.session, data)

        cached_images[data.status] = image

    response = Response(content=image.read(), media_type="image/png")
    image.seek(0)
    return response
