from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from states.states import FSM_my_class
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from keyboards.keyboard_utils import (markup_choose_status, markup_proof_teacher,
                                      markup_proof_student)
from database.database import register_user, select_user

# Инициализируем роутер уровня модуля
router_other = Router()

#config: Config = load_config()

# Этот хэндлер срабатывает на команду /delete
@router_other.message(Command(commands='delete'))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/delete'])
    await state.clear()
    '''user_dict = services.user_db_get()
    if message.from_user.id in user_dict:
        del user_dict[message.from_user.id]
        services.user_db_upload(user_dict)'''

# Этот хэндлер срабатывает на команду /start
@router_other.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    if not select_user(message.from_user.id):
        await message.answer(
            text=LEXICON_RU['/start'],
            reply_markup=markup_choose_status
        )
        await state.set_state(FSM_my_class.Choose_status)
    else:
        await message.answer(text=LEXICON_RU['second_reg'])

# Этот хэндлер НЕ будет срабатывать на команду "/cancel"
@router_other.message(Command(commands='cancel'), lambda message: message.from_user.id not in [7812730819])
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['no cancel'])

#выбрана роль "Учитель"
@router_other.callback_query(StateFilter(FSM_my_class.Choose_status),F.data == 'teacher')
async def process_proof_teacher(callback: CallbackQuery, state: FSMContext):
    await state.update_data(status=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text = LEXICON_RU['teacher_proof'],
        reply_markup=markup_proof_teacher
    )
    await state.set_state(FSM_my_class.Wait_proof_teacher)

#выбрана роль "Студент"
@router_other.callback_query(StateFilter(FSM_my_class.Choose_status),F.data == 'student')
async def process_proof_student(callback: CallbackQuery, state: FSMContext):
    await state.update_data(status=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text = LEXICON_RU['student_proof'],
        reply_markup=markup_proof_student
    )
    await state.set_state(FSM_my_class.Wait_proof_student)

# отправлено что-то некорректное при выборе роли
@router_other.message(StateFilter(FSM_my_class.Choose_status))
async def warning_not_status(message: Message):
    await message.answer(
        text=LEXICON_RU['err_status']
    )

#проверка учителя
@router_other.callback_query(StateFilter(FSM_my_class.Wait_proof_teacher), F.data.in_(['yes', 'no']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(proof=callback.data)
    # Удаляем сообщение с кнопками
    await callback.message.delete()
    user_id = callback.from_user.id
    '''user_dict = services.user_db_get()
    user_dict[user_id] = deepcopy(teacher_dict)
    user_dict[user_id]['status'] = 'teacher'
    services.user_db_upload(user_dict)'''
    await callback.message.answer(
        text=LEXICON_RU['save_data']
    )   
    await callback.message.answer(
        text=LEXICON_RU['you_teacher']
    )
    await state.clear()

#проверка ученика
@router_other.callback_query(StateFilter(FSM_my_class.Wait_proof_student), F.data.in_(['yes', 'no']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(proof=callback.data)
    # Удаляем сообщение с кнопками
    await callback.message.delete()
    user_id = callback.from_user.id
    '''user_dict = services.user_db_get()
    user_dict[user_id] = deepcopy(student_dict)
    user_dict[user_id]['status'] = 'student'
    services.user_db_upload(user_dict)'''
    await callback.message.answer(
        text=LEXICON_RU['save_data']
    )   
    await callback.message.answer(
        text=LEXICON_RU['you_student']
    )
    await state.clear()

# Этот хэндлер будет срабатывать, если во время подтверждения
# будет введено/отправлено что-то некорректное
@router_other.message(StateFilter(FSM_my_class.Wait_proof_teacher))
async def warning_not_proof(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['err_proof']
    )

@router_other.message(StateFilter(FSM_my_class.Wait_proof_student))
async def warning_not_proof(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['err_proof']
    )

# Этот хэндлер НЕ срабатывает на команду /start
@router_other.message(CommandStart(), ~StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU['err_reg']
    )

'''# Этот хэндлер будет срабатывать на любые сообщения в состоянии "по умолчанию",
# кроме тех, для которых есть отдельные хэндлеры
@router_other.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['default_err'])'''