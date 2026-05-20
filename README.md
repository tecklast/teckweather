
# Weather Bot

Telegram-бот, который по названию города показывает текущую погоду (температура и ветер).

Данные берутся из [Open-Meteo](https://open-meteo.com/) (геокодинг и прогноз), без API-ключей.

## Как пользоваться

1. Запустите бота.
2. Напишите боту в Telegram название города, например: `Moscow` или `Berlin`.

## Требования

- Python 3.10+
- [aiogram](https://docs.aiogram.dev/)
- [requests](https://requests.readthedocs.io/)

## Установка

```bash
pip install aiogram requests
```

Создайте бота в [@BotFather](https://t.me/BotFather) и получите токен.

## Запуск

Укажите токен в `main.py` (переменная `TOKEN`) или вынесите его в переменную окружения и подставляйте в коде.

```bash
python main.py
```

## Структура

- `main.py` — логика бота и запросы к Open-Meteo
