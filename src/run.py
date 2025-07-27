import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import TG_TOKEN
from bot.handlers import router

from bot.database.models import async_main


bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN_V2
        # тут ещё много других интересных настроек
    )
)

dp = Dispatcher()


async def main():
    await async_main()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
