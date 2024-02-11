from models.todo import TodoDB


class TodoRepo():
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self) -> list[TodoDB]:
        return self.db.query(TodoDB).filter()

    def create(self, todo_item):
        new_item = TodoDB(**todo_item.dict())
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def get_by_id(self, id):
        return self.db.query(TodoDB).filter(TodoDB.id == id).first()