from repository.user import UserRepo
from schemas.user import User, UserConfirmed
from services.email import send_email

from random import randint

from fastapi import HTTPException



class UserService():
    def __init__(self, db) -> None:
        self.repository = UserRepo(db=db)

    def create_new(self, user: User) -> User:
        user.confirmed = False
        user.otp = str(randint(100000, 999999))
        send_email("Welcome", f"your code is {user.otp}", user.username)
        new_user_from_db = self.repository.create(user)
        new_user = User.from_orm(new_user_from_db)
        return new_user

    def confirmed_user(self, data: UserConfirmed) -> User:
        user = self.get_by_username(data.email)
        if data.otp == user.otp:
            user.confirmed = True
            user = self.repository.update(user)
        return user


    def get_user_for_auth(self, username: str, password: str) -> User:
        user = self.repository.get_user_and_check_pass(username, password)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)


    def get_by_username(self, username: str) -> User:
        user = self.repository.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=403)
        return User.from_orm(user)

    def set_image(self, user: User, url: str) -> User:
        user.image = url
        user_from_db = self.repository.update(user)
        return User.from_orm(user_from_db)


