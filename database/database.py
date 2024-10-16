from random import randint
from config_data.config import Config, load_config
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
#from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
import array
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from flask_sqlalchemy import SQLAlchemy

config: Config = load_config()

host = config.db.db_host
password = config.db.db_password
database = config.db.database
db_user = config.db.db_user

Base = declarative_base()
metadata = MetaData()
session: scoped_session
engine = create_engine(f"postgresql+psycopg2://{db_user}:{password}@{host}/{database}")
session = scoped_session(sessionmaker(bind=engine))
Base.query = session.query_property()

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    status = Column(String)

class Students(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    name = Column(String)
    subject = Column(String)

class Teacher(Base):
    __tablename__= 'teacher'

    id = Column(Integer, primary_key=True)
    students = Column(String)
    lessons = Column(String)
    pay = Column(String)
    name = Column(String)

def register_user(user_id, user_status):
    new_data = Users(id = user_id, status = user_status)
    session.add(new_data)
    session.commit()
    if user_status == 'teacher':
        new_data = Teacher(id = user_id)
        session.add(new_data)
        session.commit()

def user_check(user_id): 
    user = session.query(Users).filter(Users.id == user_id).first() 
    return user

def student_check(student_id: int): 
    student = session.query(Students).filter(Students.id == student_id).first() 
    return student

def students_list_get(teacher_id: int) -> str:
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first() 
    return teacher.students

def add_student_to_teacher(student_id: int, teacher_id: int):
    #считать список студентов у учителя
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first() 
    #добавить в него id нового студента
    s = teacher.students + ', ' + str(student_id)
    #изменить список студентов у учителя
    teacher.students = s
    session.add(teacher)
    session.commit()

def add_student(student_user_name: str, student_name: str, student_subject: list, teacher_id: int):
    student_id = randint(1,1000000)
    i = 1
    while True:
        new_data = Students(
            id = student_id, 
            user_name = student_user_name, 
            name =student_name, 
            subject = student_subject #добавить преобразование лист в стр
        )
        session.add(new_data)
        try:
            session.commit()
            break
        except IntegrityError:
            session.rollback()  # откатываем session.add(user)
        i += 1
        if i > 1000:
            break
        student_id = randint(1,1000000)
    if i > 1000:
        return False
    else:
        add_student_to_teacher(student_id, teacher_id)
        return True

