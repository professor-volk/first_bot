from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from database import database as db

#Клавиатура выбора роли
teacher_button = InlineKeyboardButton(
    text='Учитель',
    callback_data='teacher'
)
student_button = InlineKeyboardButton(
    text='Ученик',
    callback_data='student'
)
keyboard: list[list[InlineKeyboardButton]] = [[teacher_button, student_button]]
markup_choose_status = InlineKeyboardMarkup(inline_keyboard=keyboard)

#Клавиатура подтверждения учителя
yes_button_teacher = InlineKeyboardButton(
    text='Точно!',
    callback_data='yes'
)
no_button_teacher = InlineKeyboardButton(
    text='Блин, нет(',
    callback_data='no'
)
keyboard: list[list[InlineKeyboardButton]] = [[yes_button_teacher, no_button_teacher]]
markup_proof_teacher = InlineKeyboardMarkup(inline_keyboard=keyboard)

#Клавиатура подтверждения ученика
yes_button_student = InlineKeyboardButton(
    text='Мамой клянусь!',
    callback_data='yes'
)
no_button_student = InlineKeyboardButton(
    text='Ладно, расуксил',
    callback_data='no'
)
keyboard: list[list[InlineKeyboardButton]] = [[yes_button_student, no_button_student]]
markup_proof_student = InlineKeyboardMarkup(inline_keyboard=keyboard)

# формирование клавиатуры из списка учеников
def create_students_keyboard(student_list: list, teacher_id: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for i in student_list:
        st = db.student_check(int(i))
        res = st.name + ', ' + st.user_name
        kb_builder.row(InlineKeyboardButton(
            text=res,
            callback_data=str(teacher_id)+', ' + i
        ))
    return kb_builder.as_markup()

# формирование клавиатуры из списка предметов
def create_subjects_keyboard(subject_list: str) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for i in subject_list:
        kb_builder.row(InlineKeyboardButton(
            text=i,
            callback_data=i
        ))
    return kb_builder.as_markup()
