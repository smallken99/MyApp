import eel
from model.userController import UserCtrl

class UserAPI:
    def __init__(self, session):
        self.UserDAO = UserCtrl(session)

 
    def add_user(self, name, email):
        return self.UserDAO.add_user(name, email)

 
    def get_users(self):
        users = self.UserDAO.get_users()
        result = [user.to_dict() for user in users]
        return result