# database
from sqlalchemy import create_engine, select, MetaData, Table, and_
import sys
from config import *
import os

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)

metadata = MetaData(bind=None)
chat_t = Table(
    'chat_t', 
    metadata, 
    autoload=True, 
    autoload_with=engine
)

# stmt = "SELECT msg_count FROM chat_t WHERE identity = 'main'"

conn = engine.connect()

# stmt = select(chat_t.c.msg_count)
stmt = select(chat_t.c['id']).where(chat_t.c.identity=='mains')
results = conn.execute(stmt).fetchall()
print(results)
sys.exit(0)
msg_count = results[0][0]

stmt = chat_t.update().where(chat_t.c.identity=='main').values(msg_count=msg_count+1)
results = conn.execute(stmt)

stmt = select(chat_t.c['msg_count']).where(chat_t.c.identity=='main')
results = conn.execute(stmt).fetchall()
msg_count = results[0][0]
print(msg_count)
# print(a)


# results = conn.execute(stmt).fetchall()

# print(results)