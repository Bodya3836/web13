from sqlalchemy import Column, String, Boolean, Date, Integer

from .base import BaseModel, Base

class TodoDB(BaseModel):
    __tablename__ = "todos"
    # id = Column(Integer)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(Integer)
    birthday = Column(Date)
    is_done = Column(Boolean, default=False)
    description = Column(String)