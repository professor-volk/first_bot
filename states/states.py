from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

# Класс для регистрации
class FSM_my_class(StatesGroup):
    Choose_status = State() #Выбор роли
    Wait_proof_teacher = State() # Подтверждение учителя
    Wait_proof_student = State() # Подтверждение ученика
    Proof_teacher = State() # Подтвержденный учитель
    Proof_student = State() # Подтвержденный ученик

#Класс для добавления ученика учителем
class FSM_add_student(StatesGroup):
    Name= State() #Имя ученика
    Subject = State() # Название предмета
    Telega = State() # Является ли ученик пользователем телеграм
    Name_user = State() # "Имя пользователя" ученика в телеграм

#Класс для добавления урока
class FSM_add_less(StatesGroup):
    Student = State() # Выбор студента
    Subject = State() # Выбор предмета
    Name_less = State() # Подтверждение ученика
    Data = State() # Дата ближайшего занятия
    Time_start = State() # С какого 
    Time_end = State() # по какое время
    Price = State() # Стоимость занятия
    Memo_less = State() # Сколько раз нужно напоминать об уроке
    Memo_1_t = State() # Для каждого из напоминаний нужно выбрать, за какое время до занятия и кому напоминать
    Memo_1_h = State() # 
    Memo_2_t = State() # 
    Memo_2_h = State() # 
    Memo_3_t = State() # 
    Memo_3_h = State() # 
    Memo_4_t = State() # 
    Memo_4_h = State() # 
    Memo_pay = State() # Нужно ли напоминать об оплате