from aiogram import Router
from states.states import FSM_my_class
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from lexicon.lexicon_ru import LEXICON_RU

router_student = Router()
#вешаем на роутер проверку ученика
#user_dict = services.user_db_get()
#router_student.message.filter(lambda message: user_dict[message.from_user.id]['status'] == 'student')

@router_student.message(StateFilter(FSM_my_class.Proof_student))
async def test(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['you_student'])