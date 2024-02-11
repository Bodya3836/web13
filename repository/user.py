from models.users import UserDB
import os
import hashlib
from depenedencies.database import SessionLocal

class UserRepo():
    def __init__(self, db) -> None:
        self.db = db


    def create(self, user):
        password, salt = self.hash_password(user.password)
        new_user = UserDB(**user.dict())
        new_user.password = password
        new_user.salt = salt
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update(self, user):
        self.db.query(UserDB).filter(UserDB.username==user.username).delete()
        return self.create(user)

    def get_by_username(self, username):
        return self.db.query(UserDB).filter(UserDB.username == username).first()


    def get_user_and_check_pass(self, username, password):
        user = self.db.query(UserDB).filter(UserDB.username == username).first()
        password_from_db = user.password
        user_salt = user.salt
        hashed_pass, _ =  self.hash_password(password=password, salt=user_salt)
        if hashed_pass ==password_from_db:
            return user
        else:
            return None


    def generate_salt(self):
        return os.urandom(16)

    def hash_password(self, password, salt=None) -> tuple[str]:
        if salt is None:
            salt = self.generate_salt()
        else:
            salt = bytes.fromhex(salt)
        salted_password = password.encode() + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return str(hashed_password), str(salt.hex())

async def confirmed_email(email: str, db: SessionLocal) -> None:
        user = await get_user_by_email(email, db)
        user.confirmed = True
        await db.commit()