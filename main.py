import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message


TOKEN = "8292377879:AAHq0jvuRTB1ckOBR-W-1W4iCe05pWVZJ3o"

# Обход системного прокси (VPN), из‑за которого падали запросы
NO_PROXY = {"http": None, "https": None}

bot = Bot(token=TOKEN)
dp = Dispatcher()


def clean_city_name(text: str) -> str:
    return text.strip().lstrip("!").strip()


def fetch_weather(city: str) -> str | None:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo = requests.get(
        geo_url,
        params={"name": city, "count": 1, "language": "en"},
        timeout=15,
        proxies=NO_PROXY,
    )
    geo.raise_for_status()
    results = geo.json().get("results")
    if not results:
        return None

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]
    name = results[0].get("name", city)

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather = requests.get(
        weather_url,
        params={"latitude": lat, "longitude": lon, "current_weather": "true"},
        timeout=15,
        proxies=NO_PROXY,
    )
    weather.raise_for_status()
    current = weather.json()["current_weather"]

    return (
        f"🌤 Weather in {name}:\n"
        f"🌡 Temperature: {current['temperature']}°C\n"
        f"💨 Wind: {current['windspeed']} km/h"
    )


@dp.message()
async def get_weather(message: Message):
    if not message.text:
        await message.reply("Напиши название города, например: Moscow")
        return

    city = clean_city_name(message.text)
    if not city:
        await message.reply("Напиши название города, например: Moscow")
        return

    try:
        text = await asyncio.to_thread(fetch_weather, city)
        if text is None:
            await message.reply("❌ Город не найден")
            return
        await message.reply(text)
    except Exception:
        await message.reply("⚠️ Ошибка при получении погоды")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
