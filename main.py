import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from aiogram.fsm.storage.redis import RedisStorage, Redis

# Импортируем миддлвари
# Импортируем вспомогательные функции для создания нужных объектов
#from database import database
# Импортируем хэндлеры (в них же роутеры)
from handlers import admin_handlers, student_handlers, teacher_handlers, other_handlers

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()
    
    # Инициализируем Redis
    redis = Redis(host='localhost')
    
    # Инициализируем объект хранилища
    storage = RedisStorage(redis=redis)

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=storage)

    # Инициализируем другие объекты (пул соединений с БД, кеш и т.п.)
    #database.db_start()
    # Помещаем нужные объекты в workflow_data диспетчера
    #dp.workflow_data.update(...)

    # Настраиваем главное меню бота
    #await set_main_menu(bot)

    # Регистриуем роутеры
    logger.info('Подключаем роутеры')
    dp.include_router(admin_handlers.router_admin)    
    dp.include_router(other_handlers.router_other)
    dp.include_router(teacher_handlers.router_teacher)
    dp.include_router(student_handlers.router_student)
        
    # Регистрируем миддлвари
    logger.info('Подключаем миддлвари')
    #dp.message.outer_middleware(MessageLogMiddleware())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
