from sqlalchemy import Column, Integer, String, DateTime

from depenedencies.database import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

