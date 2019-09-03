from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.setting import SQLITE_DATABASE

engine = create_engine(f'sqlite:///{SQLITE_DATABASE}.db?check_same_thread=False')

Base = declarative_base()
session = sessionmaker(bind=engine)()


import app.model.user
