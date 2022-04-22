
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class chat_t(Base):
    __tablename__ = 'chat_t'
    id = Column(Integer, primary_key=True)
    identity = Column(String(50))
    username =  Column(String(50))
    msg_count = Column(Integer)
    last_msg_time = Column(String(50))