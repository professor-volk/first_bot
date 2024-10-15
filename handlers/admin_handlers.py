from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import Redis
from config_data.config import Config, load_config
from lexicon.lexicon_ru import LEXICON_RU

config: Config = load_config()
#redis = Redis(host='localhost')
router_admin = Router()
router_admin.message.filter(lambda message: message.from_user.id in [7812730819])
# Этот хэндлер будет срабатывать на команду "/cancel"
@router_admin.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'])
    await state.clear()
    open('file.txt', 'w').close()
    #await redis.flushdb()