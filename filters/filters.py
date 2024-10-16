from aiogram.types import Message
from aiogram.filters import BaseFilter
from database import database as db


class MyFilter(BaseFilter):
    def __init__(self, id: int) -> None:
        # В качестве параметра фильтр принимает список с целыми числами 
        self.user = db.user_check(id)
    async def __call__(self) -> bool:
        return  self.user.status == 'teacher'


