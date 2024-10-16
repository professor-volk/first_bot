from aiogram import F, Router
from states.states import FSM_my_class, FSM_add_less, FSM_add_student
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from lexicon.lexicon_ru import LEXICON_RU
from filters.filters import MyFilter
from database import database as db
from keyboards import keyboard_utils
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from datetime import datetime
from aiogram.filters.callback_data import CallbackData

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
@router_teacher.message(Command(commands='add_lesson'), lambda message: MyFilter(message.from_user.id))
async def add_lesson(message: Message, state: FSMContext):
    await state.set_state(FSM_add_less.Student)
    # выбор ученика из списка
    # получаем список учеников у учителя
    student_list = db.students_list_get(message.from_user.id).split(',')
    # Формируем клавиатуру учеников в формате: Имя, юзер нэйм
    await message.answer(
        text='Выберите ученика из списка: ',
        reply_markup=keyboard_utils.create_students_keyboard(student_list, message.from_user.id)
    )

#Выбор предмета с проверкой, правильно ли (кнопкой) выбран ученик
@router_teacher.callback_query(StateFilter(FSM_add_less.Student))
async def less_choose_student(callback: CallbackQuery, state: FSMContext):
    button_press = callback.data.split(',') # получаем данные из нажатой кнопки: id учителя, студента
    if button_press[0] == str(callback.from_user.id): # проверяем, была ли нажата кнопка (костыль)
        await state.update_data(student=int(button_press[1])) # запоминаем, какой ученик выбран
        await callback.message.delete() # удаляем сообщение с кнопками
        subject_list = db.student_check(int(button_press[1])).subject.split(',') # получаем список предметов
        await callback.message.answer(
            text = 'Выберите предмет из списка: ',
            reply_markup = keyboard_utils.create_subjects_keyboard(subject_list)
        )
        await state.set_state(FSM_add_less.Subject)
    else:
        await callback.message.answer(text='Для выбора ученика, пожалуйста, пользуйтесь кнопками')

# получаем выбранный предмет и переходим к вводу названия занятия
@router_teacher.callback_query(StateFilter(FSM_add_less.Subject))
async def less_choose_subject(callback: CallbackQuery, state: FSMContext):
    # Добавить проверку, нажата кнопка или нет!!!
    await state.update_data(subject=callback.data) # запоминаем, какой предмет выбран
    await callback.message.delete() # удаляем сообщение с кнопками
    await callback.message.answer(text = 'Введите, как будет называться ваш урок (именно так он будет'
                                  'отражаться в рассписании. Это может быть что-то вроде "Маша ЕГЭ"'
                                  'или "Ярослав 7 класс", чтобы вам сразу было понятно, что это за'
                                  'занятие. Постарайтесь не использовать много букав)')
    await state.set_state(FSM_add_less.Name_less)
    #выбор предмета из списка

# получаем название занятия и переходим к вводу даты
@router_teacher.message(StateFilter(FSM_add_less.Name_less))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.update_data(name_less=message.text)
    await message.answer(
        text='Выберите дату ближайшего занятия: ',
        reply_markup=await SimpleCalendar(locale='ru_RU.utf8').start_calendar()
    )
    await state.set_state(FSM_add_less.Data)

# проверяем, выбрана ли дата, и переходим к выбору времени
@router_teacher.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale='ru_RU.utf8', show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        callback_query.message.delete()
        s = date.strftime("%d/%m/%Y")
        await state.update_data(data_less = s),
        await callback_query.message.answer(text='Во сколько занятие начинается?'
                                            'Введите время в формате чч:мм, например 7:23 или 19:30')
        await state.set_state(FSM_add_less.Time_start)

# проверяем, написано ли время, и переходим опять к записи времени (конца)
@router_teacher.message(StateFilter(FSM_add_less.Time_start), F.text.split(':')[0].isdigit() & F.text.split(':')[1].isdigit())
async def less_choose_subject(message:Message, state: FSMContext):
    await state.update_data(time_start = message.text)
    await message.answer(text='Во сколько занятие заканчивается?'
                                            'Введите время в формате чч:мм, например 7:23 или 19:30')
    await state.set_state(FSM_add_less.Time_end)

# проверяем, выбрано ли время и переходим к вводу цены
@router_teacher.message(StateFilter(FSM_add_less.Time_end), F.text.split(':')[0].isdigit() & F.text.split(':')[1].isdigit())
async def less_choose_subject(message:Message, state: FSMContext):
    await state.update_data(time_end = message.text)
    await message.answer(text='Введите стоимость занятия в рублях. Вводите только число.')
    await state.set_state(FSM_add_less.Price)
    

@router_teacher.message(StateFilter(FSM_add_less.Price), F.text.isdigit())
async def less_choose_subject(message:Message, state: FSMContext):
    await state.update_data(price = message.text)
    await message.answer(
        text='Выберите, сколько раз нужно напоминать о занятии:',
        reply_markup=keyboard_utils.markup_memo_less
    )
    await state.set_state(FSM_add_less.Memo_less)
    #выбор предмета из списка
    

@router_teacher.callback_query(StateFilter(FSM_add_less.Memo_less), F.data.in_(['0','1','2','3','4']))
async def less_choose_subject(callback:CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(memo_less = callback.data)
    await callback.message.answer(text='Выбор предмета')
    await state.set_state(FSM_add_less.Memo_1_t)
    

@router_teacher.message(StateFilter(FSM_add_less.Memo_1_t))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_1_h)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_1_h))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_2_t)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_2_t))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_2_h)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_2_h))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_3_t)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_3_t))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_3_h)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_3_h))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_4_t)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_4_t))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_4_h)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')

@router_teacher.message(StateFilter(FSM_add_less.Memo_4_h))
async def less_choose_subject(message:Message, state: FSMContext):
    await state.set_state(FSM_add_less.Memo_pay)
    #выбор предмета из списка
    await message.answer(text='Выбор предмета')


'''@router_teacher.message(is_teacher)
async def test(message: Message):
    await message.answer(text=LEXICON_RU['you_teacher'])'''
    