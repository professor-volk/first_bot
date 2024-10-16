from copy import deepcopy
from aiogram import F, Router
from states.states import FSM_my_class, FSM_add_less, FSM_add_student
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from lexicon.lexicon_ru import LEXICON_RU
from filters.filters import MyFilter
from database import database as db

router_teacher = Router()

#Выбрана команда добавления ученика
@router_teacher.message(Command(commands='add_student'), lambda message: MyFilter(message.from_user.id))
async def add_student(message: Message, state: FSMContext):
    await state.set_state(FSM_add_student.Name_user)
    await message.answer(text=LEXICON_RU['add_student_name_user'])
    '''if is_teacher(message):
        await state.set_state(FSM_add_student.Name_user)
        await message.answer(text=LEXICON_RU['add_student_name_user'])
    else:
        await message.answer(text=LEXICON_RU['no_teacher'])'''

# Этот хэндлер будет срабатывать, если введено корректное имя пользователя 
# Пока считаем, что имя пользователя есть у всех учеников
@router_teacher.message(StateFilter(FSM_add_student.Name_user), F.text[0] == '@')
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(user_name = message.text)
    await message.answer(text=LEXICON_RU['add_student_name'])
    await state.set_state(FSM_add_student.Name)

# Введено некорректное имя пользователя
@router_teacher.message(StateFilter(FSM_add_student.Name_user))
async def process_name_sent(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['err_add_student_name_user'])

# Этот хэндлер будет срабатывать, если введено корректное имя пользователя
@router_teacher.message(StateFilter(FSM_add_student.Name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer(text=LEXICON_RU['add_student_subject'])
    await state.set_state(FSM_add_student.Subject)

# Введено некорректное имя ученика
@router_teacher.message(StateFilter(FSM_add_student.Name))
async def process_name_sent(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['err_add_student_name'])

# Этот хэндлер будет срабатывать, если введено корректное имя ученика
@router_teacher.message(StateFilter(FSM_add_student.Subject))
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(subject = message.text)
    d = await state.get_data()
    s1 = d['user_name']
    s2 = d['name']
    s3 = d['subject']
    if db.add_student(s1, s2, s3, message.from_user.id):
        await message.answer(text=LEXICON_RU['add_student_finish'])
    else:
        await message.answer(text='Что-то пошло не так...')
    await state.clear()

#Выбрана команда добавления урока
@router_teacher.message(Command(commands='add_lesson'))
async def add_student(message: Message, state: FSMContext):
    #await state.set_state(FSM_add_student.Name_user)
    await message.answer(text='Пока эта функция еще не добавлена(')
    '''if is_teacher(message):
        #await state.set_state(FSM_add_student.Name_user)
        await message.answer(text='Пока эта функция еще не добавлена(')
    else:
        await message.answer(text=LEXICON_RU['no_teacher'])'''

'''@router_teacher.message(is_teacher)
async def test(message: Message):
    await message.answer(text=LEXICON_RU['you_teacher'])'''
    