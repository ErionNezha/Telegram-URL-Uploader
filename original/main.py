import asyncio
import logging
import os
import re
from sql import db
import uuid
from keyboard import result_buttons
from test import download_file, get_length
from decouple import config
from telethon import TelegramClient, events, functions
from telethon.utils import is_video
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeVideo
from aslmedia.get_size import get_size
from aslmedia.scraper import get_movie_info
# initializing logger
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("TelethonSnippets")

# fetching variables from env
try:
    API_ID = config("API_ID", cast=int)
    API_HASH = config("API_HASH")
    SESSION = config("SESSION")
    AUTHS = config("AUTHS")
    USER_AUTHS = config("USER_AUTHS")
except BaseException as ex:
    log.info(ex)


AUTH_USERS = [int(x) for x in USER_AUTHS.split(" ")]

log.info("Connecting bot.")
try:
    bot = TelegramClient(StringSession(SESSION), api_id=API_ID, api_hash=API_HASH).start(bot_token=AUTHS)
except BaseException as e:
    log.warning(e)
    exit(1)
try:
    db.create_user()
except:pass


@bot.on(events.NewMessage(from_users=AUTH_USERS, pattern='/start', incoming=True, func=lambda e: e.is_private))
async def start_handler(event):
    args = event.raw_text.split()[1:]  # "args"ni olish
    chat_id = event.message.peer_id
    if args:
        res = db.select_user(user_id=args[0])
        result = await get_size(res[1])
        if result['ok'] == True:
            send = await bot.send_message(chat_id, 'Yuklanmoqda kuting...')
            down = await download_file(res[1], f"{uuid.uuid4().hex}.mp4")
            if down == False:
                await bot(functions.messages.EditMessageRequest(chat_id, send.id,
                                                                message="Ma'lumot topilmadi. keyinroq qayta uring ko'ring!"))
                os.remove(down)
            else:
                await bot.send_file(chat_id, f'{down}', caption=f"{res[2]}", thumb='cover.jpg', attributes=(
                DocumentAttributeVideo(get_length(down), 1280, 720, supports_streaming=True),))
                await bot(functions.messages.DeleteMessagesRequest(id=[send.id], revoke=True))
                os.remove(down)
        else:
            await bot.send_message(chat_id, "Kino hajmi 2000 MB dan katta!")
    else:
        await bot.send_message(chat_id,"<b>Assalomu alaykum botga xush kelibsiz men sizga aslmedia.org dan kino yuklab berishga yordam beraman!\n\nBuning uchun menga aslmedia.org dan biron kino sahifani yuboring.</b>",parse_mode="HTML")

@bot.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, func=lambda e: e.is_private and is_video(e.media)))
async def on_message_media(event):
    chat_id = event.message.peer_id
    reply_prog = await event.reply("Iltimos, kuting, media yuklab olinmoqda...")
    photo = event.video
    file_path = await bot.download_media(photo, file=f'{uuid.uuid4().hex}.mp4')
    try:
        await reply_prog.delete()
        await bot.send_file(chat_id, file_path, caption=event.message.text, thumb='cover.jpg', attributes=(
            DocumentAttributeVideo(get_length(file_path), 1280, 720, supports_streaming=True),))
        os.remove(file_path)
    except:
        os.remove(file_path)

@bot.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, func=lambda e: e.is_private and e.text and not e.file))
async def on_message_text(event):
    chat_id = event.message.peer_id
    text = event.message.text
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, text)
    if urls != []:
        send = await bot.send_message(chat_id, "Tekshirilmoqda kutiing...")

        results = await get_movie_info(urls[0])
        if results:
            await bot(functions.messages.DeleteMessagesRequest(id=[send.id],revoke=True))
            for result in results:
                await bot.send_message(chat_id, f"<b>FILM HAQIDA QISQACHA:</b>\n\n{result['description']}", parse_mode="HTML")
                await bot.send_file(chat_id, file=f"{result['thumbnail']}", caption=f"<b>{result['name']}</b>", parse_mode="HTML", buttons=result_buttons(result['results']))
        else:
            await bot(functions.messages.EditMessageRequest(chat_id, send.id, message="Ma'lumot topilmadi. keyinroq qayta uring ko'ring yoki to'gri link yuboring!"))



# Run the event loop to start receiving messages


bot.run_until_disconnected()
