from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from database import database as db
from aiogram.filters.callback_data import CallbackData

#Клавиатура выбора роли
def markup_choose_status():
    teacher_button = InlineKeyboardButton(
        text='Учитель',
        callback_data='teacher'
    )
    student_button = InlineKeyboardButton(
        text='Ученик',
        callback_data='student'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[teacher_button, student_button]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Клавиатура подтверждения учителя
def markup_proof_teacher():
    yes_button_teacher = InlineKeyboardButton(
        text='Точно!',
        callback_data='yes'
    )
    no_button_teacher = InlineKeyboardButton(
        text='Блин, нет(',
        callback_data='no'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button_teacher, no_button_teacher]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Клавиатура подтверждения ученика
def markup_proof_student():
    yes_button_student = InlineKeyboardButton(
        text='Мамой клянусь!',
        callback_data='yes'
    )
    no_button_student = InlineKeyboardButton(
        text='Ладно, расуксил',
        callback_data='no'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button_student, no_button_student]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Клавиатура для напоминаний об оплате
def markup_memo_pay():
    yes_button = InlineKeyboardButton(
        text='Да',
        callback_data='yes'
    )
    no_button = InlineKeyboardButton(
        text='Нет',
        callback_data='no'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

class StudentCallback(CallbackData, prefix='students'):
    student_id: int

class SubjectCallback(CallbackData, prefix='subjects'):
    sub_name: str

class LessonCallback(CallbackData, prefix='lessons', sep='&'):
    lesson_name: str
    lesson_time: str

# формирование клавиатуры из списка учеников
def create_students_keyboard(student_list: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру списком учеников
    for i in student_list:
        st = db.student_check(int(i))
        res = st.name + ', ' + st.user_name
        kb_builder.row(InlineKeyboardButton(
            text=res,
            callback_data = StudentCallback(student_id=i).pack()
        ))
    return kb_builder.as_markup()

# формирование клавиатуры из списка предметов
def create_subjects_keyboard(subject_list: str) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру списком предметов
    for i in subject_list:
        kb_builder.row(InlineKeyboardButton(
            text=i,
            callback_data = SubjectCallback(sub_name=i).pack()
        ))
    return kb_builder.as_markup()

#Клавиатура выбора количества напоминаний
def markup_memo_less():
    zero_button = InlineKeyboardButton(
        text='0',
        callback_data='0'
    )
    one_button = InlineKeyboardButton(
        text='1',
        callback_data='1'
    )
    two_button = InlineKeyboardButton(
        text='2',
        callback_data='2'
    )
    three_button = InlineKeyboardButton(
        text='3',
        callback_data='3'
    )
    four_button = InlineKeyboardButton(
        text='4',
        callback_data='4'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[zero_button, one_button, two_button, three_button, four_button]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Формирование клавиатуры расписания
def create_schedule(teacher_id: int, edit: bool) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру списком уроков
    teacher = db.teacher_check(teacher_id)
    lesson_list = teacher.lessons.split(',')
    for i in lesson_list:
        lesson = db.lesson_check(int(i))
        if edit:
            kb_builder.row(InlineKeyboardButton(
                text=lesson.lesson_name + '\n' + lesson.time_less,
                callback_data = LessonCallback(
                    lesson_name=lesson.lesson_name, 
                    lesson_time=lesson.time_less).pack()
            ))
        else:
            kb_builder.row(InlineKeyboardButton(
                text=lesson.lesson_name + '\n' + lesson.time_less,
                callback_data = 'ignor'))
    return kb_builder.as_markup()