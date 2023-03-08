import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()
load_dotenv('.env')
engine = create_engine(url=os.environ['DATABASE_URL'], connect_args={"check_same_thread": False})

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    money = Column(Float)

SessionLocal = sessionmaker(autoflush=False, bind=engine)