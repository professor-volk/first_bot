from aiogram.types import Message
from database import services

def is_teacher(message: Message) -> bool:
    user_dict = services.user_db_get()
    return user_dict[message.from_user.id]['status'] == 'teacher'


