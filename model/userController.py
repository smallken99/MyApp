import sqlite3
from model.userVO import User

class UserCtrl:
    def __init__(self, Session):
        self.session = Session()

    def add_user(self, name, email):
        user = User(name, email)
        self.session.add(user)
        self.session.commit()
        return "資料新增成功!"        

    def get_users(self):
        users = self.session.query(User).all()
        return users