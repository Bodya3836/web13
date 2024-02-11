from sqlalchemy import Column, String, Boolean

from .base import Base, BaseModel

class UserDB(BaseModel):
    __tablename__ = "users"
    username = Column(String)
    password = Column(String)
    salt = Column(String)
    role = Column(String)
    confirmed = Column(Boolean, default=False)
    otp = Column(String)
    image = Column(String)