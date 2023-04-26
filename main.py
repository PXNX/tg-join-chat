import asyncio
from datetime import datetime
from logging import INFO, basicConfig
from os import makedirs
from os.path import dirname

from pyrogram import Client
from pyrogram.enums import ParseMode

from config import API_HASH, PHONE, API_ID
from functions import run_functions

LOG_FILENAME = rf"./logs/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H-%M-%S')}.log"
makedirs(dirname(LOG_FILENAME), exist_ok=True)
basicConfig(
    format="%(asctime)s %(levelname)-5s %(funcName)-16s [%(filename)s:%(lineno)d]: %(message)s",
    encoding="utf-8",
    filename=LOG_FILENAME,
    level=INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


async def main():
    try:
        async with Client(
                name="join-chat",
                api_id=API_ID,
                api_hash=API_HASH,
                phone_number=PHONE,
                parse_mode=ParseMode.HTML
        ) as app:
            print("Running...")

            await run_functions(app)

            print("Done!")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
