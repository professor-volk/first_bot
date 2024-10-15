from config_data.config import Config, load_config
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
#from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

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

def register_user(user_id, user_status):
    new_data = Users(id = user_id, status = user_status)
    session.add(new_data)
    session.commit()

def select_user(user_id): 
    user = session.query(Users).filter(Users.id == user_id).first() 
    return user
    