from src.controllers.memorydb import InMemoryDB
from src.models.users import BaseUser

db = InMemoryDB

class UserController():
    @staticmethod
    def create_user(user: BaseUser):
        result = db.save_user(user)
        return result
