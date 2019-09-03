import time

from app.model.base import Base, session
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String(32), unique=True)
    brokerid = Column(String(32))
    appid = Column(String(32))
    auth_code = Column(String(32))
    td_address = Column(String(32))
    md_address = Column(String(32))
    login_time = Column(String(32))

    @classmethod
    def add(cls, data, **kwargs):
        model = session.query(cls).filter_by(userid=data.get('userid')).first()
        if not model:
            model = cls()
            for k in data.keys():
                if hasattr(model, k):
                    setattr(model, k, data.get(k))
            session.add(model)
            session.commit()
