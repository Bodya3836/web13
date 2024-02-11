from datetime import date
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: int
    birthday: date
    is_done: bool
    description: str

    class Config:
        orm_mode = True
        from_attributes=True


class TodoCreate(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: int
    birthday: date
    description: str | None


class TodoUpdate(BaseModel):
    name: str | None
    surname: str | None
    email: str | None
    phone: int | None
    birthday: date | None
    is_done: bool | None
    description: str | None

class TodoDelete(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: int
    birthday: date
    is_done: bool
    description: str


def schemas():
    return None