from pydantic import BaseModel, EmailStr
import enum

class Email(BaseModel):
    email: EmailStr

class RolesEnum(str, enum.Enum):
    USER = "User"
    MANAGER = "Manager"
    ADMIN = "ADMIN"


class User(BaseModel):
    username: EmailStr
    password: str
    role: RolesEnum
    confirmed: bool | None
    otp: str | None
    image: str

    class Config:
        orm_mode = True
        from_attributes=True



class UserConfirmed(BaseModel):
    email: EmailStr
    otp: str

