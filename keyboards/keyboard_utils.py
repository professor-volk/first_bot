from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

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