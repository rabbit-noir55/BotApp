

# Telegram bot tokeningizni shu yerga qo'ying
TOKEN = "8072140256:AAGJP8_1wlMwUKQpJkXMm8PoSGzNOQnRSSo"

import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from yt_dlp import YoutubeDL

# Telegram bot tokenini shu yerga kiriting
TOKN = "SIZNING_BOT_TOKENINGIZ"

# Bot va Dispatcher obyektlari
bot = Bot(token=TOKEN)
dp = Dispatcher()

# YouTube videoni yuklash funksiyasi
def download_video(url):
    options = {
        'format': 'bestvideo+bestaudio/best',  # Eng yaxshi sifatni yuklaydi
        'outtmpl': '%(title)s.%(ext)s',        # Fayl nomini avtomatik yaratadi
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)  # Video yuklanadi
        return ydl.prepare_filename(info)           # Yuklangan fayl nomi qaytariladi

# Playlistni yuklash funksiyasi
def download_playlist(url):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': False,  # Playlistdagi barcha videolarni yuklash
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return [ydl.prepare_filename(entry) for entry in info['entries']]

# /start buyrug'i uchun handler
@dp.message(F.text == "/start")
async def start_command(message: types.Message):
    await message.reply("Salom! Men YouTube videolarini yoki playlistlarini yuklab beradigan botman. Menga havola yuboring.")

# YouTube havolalarni qabul qilish va yuklab berish
@dp.message()
async def handle_url(message: types.Message):
    url = message.text
    chat_id = message.chat.id

    # Playlist yoki oddiy video aniqlash
    if "playlist" in url.lower():
        await bot.send_message(chat_id, "Playlist yuklanmoqda. Iltimos kuting...")
        try:
            filenames = download_playlist(url)
            for filename in filenames:
                with open(filename, 'rb') as video:
                    await bot.send_video(chat_id, video=video)
                os.remove(filename)  # Yuklangan faylni o'chirish
        except Exception as e:
            await bot.send_message(chat_id, f"Xatolik: {str(e)}")
    else:
        await bot.send_message(chat_id, "Video yuklanmoqda. Iltimos kuting...")
        try:
            filename = download_video(url)
            with open(filename, 'rb') as video:
                await bot.send_video(chat_id, video=video)
            os.remove(filename)  # Yuklangan faylni o'chirish
        except Exception as e:
            await bot.send_message(chat_id, f"Xatolik: {str(e)}")

# Botni ishga tushirish
async def main():
    dp.include_router(dp.router)  # Routerni biriktirish
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
