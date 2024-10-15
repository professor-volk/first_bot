from sqlalchemy import create_engine
#from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean

DATABASE='first_bot'
DB_HOST='127.0.0.1'
DB_USER='professor'
DB_PASSWORD='1996Ujlf'

host = DB_HOST
password = DB_PASSWORD
database = DATABASE
db_user = DB_USER

engine = create_engine(f"postgresql+psycopg2://{db_user}:{password}@{host}/{database}")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

metadata = MetaData()

class MyTable(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    status = Column(String)

new_data = MyTable(id = 1234567, status='teacher')
session.add(new_data)
session.commit()


'''connect = psycopg2.connect(dbname="first_bot", host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=5432)
cursor = connect.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)
'''