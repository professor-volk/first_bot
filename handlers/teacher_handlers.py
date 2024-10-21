from aiogram import F, Router, Bot
from states.states import FSM_add_less, FSM_add_student
from aiogram.types import Message, CallbackQuery
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
        await message.answer(text=LEXICON_RU['err_add_student'])
    await state.clear()

# Генерация сообщения "состояния" урока
def fill_lesson_list(d: dict) -> str:
    l = ['student', 'subject', 'name_less', 'data_less', 
         'time_start', 'time_end', 'price', 'memo_less', 'memo_pay']
    res_d = dict()
    for i in l:
        if i in d:
            res_d[i] = d[i]
        else:
            res_d[i] = ''
    res_d[l[0]] = ','.join(res_d[l[0]].split(',')[1:])
    res = 'Ученик: ' + str(res_d[l[0]]) + '\n' + \
        'Предмет: ' + res_d[l[1]] + '\n' + \
        'Название урока: ' + res_d[l[2]] + '\n' + \
        'Дата ближайшего занятия: ' + res_d[l[3]] + '\n' + \
        'Время: ' + res_d[l[4]] + ' - ' + res_d[l[5]] + '\n' + \
        'Цена: ' + res_d[l[6]] + '\n' + \
        'Количество напоминаний об уроке: ' + res_d[l[7]] + '\n'
    if res_d[l[8]]:
        res += 'Напоминание об оплате: да'
    else:
        res += 'Напоминание об оплате: нет'
    return res

#Выбрана команда добавления урока
@router_teacher.message(Command(commands='add_lesson'), lambda message: MyFilter(message.from_user.id))
async def add_lesson(message: Message, state: FSMContext):
    d = await state.get_data()
    msg = await message.answer(text=LEXICON_RU['add_less'] + fill_lesson_list(d)) #отправляем "состояние" урока
    await state.update_data(msg_id = msg.message_id) #Запоминаем айди сообщения для редактирования
    # выбор ученика из списка
    # получаем список учеников у учителя
    student_list = db.students_list_get(message.from_user.id).split(',')
    # Формируем клавиатуру учеников в формате: Имя, юзер нэйм
    await message.answer(
        text=LEXICON_RU['add_less_add_student'],
        reply_markup=keyboard_utils.create_students_keyboard(student_list)
    )
    await state.set_state(FSM_add_less.Student) #Переходим в состояние выбора ученика

#Выбор предмета с проверкой, правильно ли (кнопкой) выбран ученик
@router_teacher.callback_query(StateFilter(FSM_add_less.Student), keyboard_utils.StudentCallback.filter())
async def less_choose_student(callback: CallbackQuery, state: FSMContext, 
                              bot: Bot, callback_data: keyboard_utils.StudentCallback):
    student = callback_data.pack().split(':')[1] # получаем данные из нажатой кнопки: id студента
    st = db.student_check(int(student))
    await state.update_data(student=student+','+st.name + ', ' + st.user_name) # запоминаем, какой ученик выбран
    await callback.message.delete() # удаляем сообщение с кнопками
    subject_list = db.student_check(int(student)).subject.split(',') # получаем список предметов
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = callback.message.chat.id, message_id = d['msg_id'])
    # отправляем клавиатуру со списком предметов
    await callback.message.answer(
        text = LEXICON_RU['add_less_add_subject'],
        reply_markup = keyboard_utils.create_subjects_keyboard(subject_list)
    )
    await state.set_state(FSM_add_less.Subject) # Переходим к состоянию выбора предмета
        
# Если не была нажата кнопка с учеником
@router_teacher.message(StateFilter(FSM_add_less.Student))
async def err_less_choose_student(message: Message, bot: Bot):
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id) # Удаляем неправильное сообщение 
    student_list = db.students_list_get(message.from_user.id).split(',')
    await bot.edit_message_text(
        text = LEXICON_RU['add_less_add_student_err'] + ' ' + LEXICON_RU['add_less_add_student'], 
        reply_markup=keyboard_utils.create_students_keyboard(student_list),
        chat_id = message.chat.id, 
        message_id = message.message_id-1
    )

# получаем выбранный предмет и переходим к вводу названия занятия
@router_teacher.callback_query(StateFilter(FSM_add_less.Subject), keyboard_utils.SubjectCallback.filter())
async def less_choose_subject(callback: CallbackQuery, state: FSMContext, bot: Bot,
                              callback_data: keyboard_utils.SubjectCallback):
    await state.update_data(subject=callback_data.pack().split(':')[1]) # запоминаем, какой предмет выбран
    await callback.message.delete() # удаляем сообщение с кнопками
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = callback.message.chat.id, message_id = d['msg_id'])
    await callback.message.answer(text = LEXICON_RU['add_less_add_name_less'])
    await state.set_state(FSM_add_less.Name_less)
    #выбор предмета из списка

# если не была нажата кнопка с предметом
@router_teacher.message(StateFilter(FSM_add_less.Subject))
async def err_less_choose_student(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id) # Удаляем неправильное сообщение 
    student = await state.get_data()
    student = student['student'].split(',')[0]
    subject_list = db.student_check(int(student)).subject.split(',') # получаем список предметов
    await bot.edit_message_text(
        text = LEXICON_RU['add_less_add_subject_err'] + ' ' + LEXICON_RU['add_less_add_subject'], 
        reply_markup=keyboard_utils.create_subjects_keyboard(subject_list),
        chat_id = message.chat.id, 
        message_id = message.message_id-1
    )

# получаем название занятия и переходим к вводу даты
@router_teacher.message(StateFilter(FSM_add_less.Name_less))
async def less_choose_subject(message:Message, state: FSMContext, bot: Bot):
    await state.update_data(name_less=message.text)
    await message.delete()
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id-1) # Удаляем предыдущее сообщение 
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = message.chat.id, message_id = d['msg_id'])
    await message.answer(
        text=LEXICON_RU['add_less_add_data'],
        reply_markup=await SimpleCalendar(locale='ru_RU.utf8').start_calendar()
    )
    await state.set_state(FSM_add_less.Data)

# проверяем, выбрана ли дата, и переходим к выбору времени
@router_teacher.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, 
                                  state: FSMContext, bot: Bot):
    calendar = SimpleCalendar(
        locale='ru_RU.utf8', show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        callback_query.message.delete()
        #await bot.delete_message(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id-1)
        s = date.strftime("%d/%m/%Y")
        await state.update_data(data_less = s),
        # Редактируем информацию о занятии
        d = await state.get_data()
        s = fill_lesson_list(d)
        await bot.edit_message_text(text = s, chat_id = callback_query.message.chat.id, message_id = d['msg_id'])
        await callback_query.message.answer(text = LEXICON_RU['add_less_add_time_start'])
        await state.set_state(FSM_add_less.Time_start)

# проверяем, написано ли время, и переходим опять к записи времени (конца)
@router_teacher.message(StateFilter(FSM_add_less.Time_start), F.text.split(':')[0].isdigit() & F.text.split(':')[1].isdigit())
async def less_choose_subject(message:Message, state: FSMContext, bot: Bot):
    await state.update_data(time_start = message.text)
    await message.delete()
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id-1)
    await message.answer(text=LEXICON_RU['add_less_add_time_end'])
    await state.set_state(FSM_add_less.Time_end)

# проверяем, выбрано ли время и переходим к вводу цены
@router_teacher.message(StateFilter(FSM_add_less.Time_end), F.text.split(':')[0].isdigit() & F.text.split(':')[1].isdigit())
async def less_choose_subject(message:Message, state: FSMContext, bot: Bot):
    await state.update_data(time_end = message.text)
    await message.delete()
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id-1)
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = message.chat.id, message_id = d['msg_id'])
    await message.answer(text = LEXICON_RU['add_less_add_price'])
    await state.set_state(FSM_add_less.Price)
    
# проверяем, введена ли цена и переходим к выбору количества напоминаний
@router_teacher.message(StateFilter(FSM_add_less.Price), F.text.isdigit())
async def less_choose_subject(message:Message, state: FSMContext, bot: Bot):
    await state.update_data(price = message.text)
    await message.delete()
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id-1)
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = message.chat.id, message_id = d['msg_id'])
    await message.answer(
        text = LEXICON_RU['add_less_add_memo_less'],
        reply_markup = keyboard_utils.markup_memo_less
    )
    await state.set_state(FSM_add_less.Memo_less)
    
# проверяем, нажата ли кнопка и переходим к добавлению напоминания
@router_teacher.callback_query(StateFilter(FSM_add_less.Memo_less), F.data.in_(['1','2','3','4']))
async def less_choose_subject(callback:CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await state.update_data(memo_less = callback.data)
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = callback.message.chat.id, message_id = d['msg_id'])
    await callback.message.answer(text='Выбор предмета')
    await state.set_state(FSM_add_less.Memo_1_t)
    

# проверяем, нажата ли кнопка 0 и переходим к напоминанию об оплате
@router_teacher.callback_query(StateFilter(FSM_add_less.Memo_less), F.data.in_(['0']))
async def less_choose_subject(callback:CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await state.update_data(memo_less = callback.data)
    # Редактируем информацию о занятии
    d = await state.get_data()
    s = fill_lesson_list(d)
    await bot.edit_message_text(text = s, chat_id = callback.message.chat.id, message_id = d['msg_id'])
    await callback.message.answer(
        text=LEXICON_RU['add_less_add_memo_pay'],
        reply_markup = keyboard_utils.markup_memo_pay
        )
    await state.set_state(FSM_add_less.Memo_pay)

# если нажата кнопка "да" 
@router_teacher.callback_query(StateFilter(FSM_add_less.Memo_pay), F.data.in_(['yes']))
async def less_choose_subject(callback:CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await state.update_data(memo_pay = True)
    # Редактируем информацию о занятии
    d = await state.get_data()
    #Вносим информацию в БД
    db.add_lesson(int(d['student'].split(',')[0]), d['subject'], d['name_less'], 
                  d['data_less'], d['time_start'] +' - ' + d['time_end'], 
                  int(d['price']), int(d['memo_less']), d['memo_pay'], 
                  callback.from_user.id)
    s = fill_lesson_list(d)+'\n'+LEXICON_RU['add_less_end']
    await bot.edit_message_text(text = s, chat_id = callback.message.chat.id, message_id = d['msg_id'])
    await state.clear()

# если нажата кнопка "нет" 
@router_teacher.callback_query(StateFilter(FSM_add_less.Memo_pay), F.data.in_(['no']))
async def less_choose_subject(callback:CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await state.update_data(memo_pay = False)
    # Редактируем информацию о занятии
    d = await state.get_data()
    #Вносим информацию в БД
    db.add_lesson(int(d['student'].split(',')[0]), d['subject'], d['name_less'], 
                  d['data_less'], d['time_start'] +' - ' + d['time_end'], 
                  int(d['price']), int(d['memo_less']), d['memo_pay'], 
                  callback.from_user.id)
    s = fill_lesson_list(d)+'\n'+LEXICON_RU['add_less_end']
    await bot.edit_message_text(text = s, chat_id = callback.message.chat.id, message_id = d['msg_id'])
    await state.clear()

# если не нажата кнопка
@router_teacher.callback_query(StateFilter(FSM_add_less.Memo_pay))
async def less_choose_subject(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=LEXICON_RU['err_add_less_add_memo_pay'])
    




'''@router_teacher.message(is_teacher)
async def test(message: Message):
    await message.answer(text=LEXICON_RU['you_teacher'])'''
    