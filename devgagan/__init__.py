# ---------------------------------------------------
# Fixed Version (Telethon removed + Stable bot)
# ---------------------------------------------------

import asyncio
import logging
import time
from pyrogram import Client
from pyrogram.enums import ParseMode 
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION
from motor.motor_asyncio import AsyncIOMotorClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# Main Bot
app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    parse_mode=ParseMode.MARKDOWN
)

# Optional Userbot (STRING)
if STRING:
    pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)
else:
    pro = None

# Optional Default Session
if DEFAULT_SESSION:
    userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION)
else:
    userrbot = None

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

async def create_ttl_index():
    try:
        await token.create_index("expires_at", expireAfterSeconds=0)
        print("MongoDB TTL index created.")
    except Exception as e:
        print(f"MongoDB Error: {e}")

async def setup_database():
    if MONGO_DB:
        await create_ttl_index()

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME

    await setup_database()

    await app.start()
    getme = await app.get_me()

    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name

    print(f"✅ Bot Started: @{BOT_USERNAME}")

    if pro:
        await pro.start()
    if userrbot:
        await userrbot.start()

    # Keep bot alive
    await asyncio.Event().wait()

loop.run_until_complete(restrict_bot())
