import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from yt_dlp import YoutubeDL

# Telegram bot tokeningizni shu yerga qo'ying
TOKEN = "8072140256:AAGJP8_1wlMwUKQpJkXMm8PoSGzNOQnRSSo"

# Bot va dispatcher obyektlarini yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# YouTube videoni yuklash funksiyasi
def download_video(url):
    options = {
        'format': 'bestvideo+bestaudio/best',  # Eng sifatli versiyani yuklaydi
        'outtmpl': '%(title)s.%(ext)s',        # Fayl nomini avtomatik belgilaydi
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)  # Video yuklanadi
        return ydl.prepare_filename(info)           # Yuklangan fayl nomi qaytariladi

# Playlistni yuklash funksiyasi
def download_playlist(url):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': False,  # Playlistning barcha videolarini yuklash
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return [ydl.prepare_filename(entry) for entry in info['entries']]

# /start buyrug'i uchun handler
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salom! Menga YouTube havolasini yuboring va men uni yuklab beraman.")

# YouTube havolalarni qabul qilish
@dp.message_handler(content_types=ContentType.TEXT)
async def handle_url(message: types.Message):
    url = message.text
    chat_id = message.chat.id

    # Playlist yoki video aniqlash
    if "playlist" in url.lower():
        await bot.send_message(chat_id, "Playlist yuklanmoqda. Iltimos kuting...")
        try:
            filenames = download_playlist(url)
            for filename in filenames:
                await bot.send_video(chat_id, video=open(filename, 'rb'))
                os.remove(filename)  # Faylni xotiradan o'chirish
        except Exception as e:
            await bot.send_message(chat_id, f"Xatolik: {str(e)}")
    else:
        await bot.send_message(chat_id, "Video yuklanmoqda. Iltimos kuting...")
        try:
            filename = download_video(url)
            await bot.send_video(chat_id, video=open(filename, 'rb'))
            os.remove(filename)  # Faylni xotiradan o'chirish
        except Exception as e:
            await bot.send_message(chat_id, f"Xatolik: {str(e)}")

# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
