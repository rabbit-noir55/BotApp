

# Telegram bot tokeningizni shu yerga qo'ying
TOKEN = "8072140256:AAGJP8_1wlMwUKQpJkXMm8PoSGzNOQnRSSo"

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from yt_dlp import YoutubeDL

# Bot tokeningizni shu yerga kiriting
OKEN = "SIZNING_BOT_TOKENINGIZ"

# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# YouTube videoni yuklash funksiyasi
def download_video(url):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# Playlistni yuklash funksiyasi
def download_playlist(url):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': False,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return [ydl.prepare_filename(entry) for entry in info['entries']]

# /start buyrug'i uchun handler
@dp.message(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salom! Menga YouTube havolasini yuboring va men uni yuklab beraman.")

# YouTube havolalarni qabul qilish
@dp.message()
async def handle_url(message: types.Message):
    url = message.text
    chat_id = message.chat.id

    if "playlist" in url.lower():
        await bot.send_message(chat_id, "Playlist yuklanmoqda. Iltimos kuting...")
        try:
            filenames = download_playlist(url)
            for filename in filenames:
                await bot.send_video(chat_id, video=open(filename, 'rb'))
                os.remove(filename)
        except Exception as e:
            await bot.send_message(chat_id, f"Xatolik: {str(e)}")
    else:
        await bot.send_message(chat_id, "Video yuklanmoqda. Iltimos kuting...")
        try:
            filename = download_video(url)
            await bot.send_video(chat_id, video=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            await bot.send_message(chat_id, f"Xatolik: {str(e)}")

# Botni ishga tushirish
async def main():
    dp.include_router(dp.router)  # Routerni biriktirish
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
