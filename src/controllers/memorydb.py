
from src.models.users import BaseUser

class InMemoryDB():
    DATABASE = {
        "users": {},
        "objects": {},
        "schedules": {},
        "slots": {},
        "queues": {}
    }

    @staticmethod
    def get_user():
        pass

    @classmethod
    def save_user(cls, user: BaseUser):
        db_users = cls.DATABASE["users"]
        db_users[user.tg_id] = user
        print(cls.DATABASE)
        return cls.DATABASE["users"][user.tg_id]

    @staticmethod
    def remove_user():
        pass

    @staticmethod
    def get_object():
        pass

    @staticmethod
    def save_object():
        pass

    @staticmethod
    def remove_object():
        pass

    @staticmethod
    def get_shedule():
        pass

    @staticmethod
    def save_shedule():
        pass

    @staticmethod
    def remove_shedule():
        pass


    @staticmethod
    def get_slots():
        pass

    @staticmethod
    def save_slots():
        pass

    @staticmethod
    def remove_slots():
        pass

    @staticmethod
    def get_queue():
        pass

    @staticmethod
    def save_queue():
        pass

    @staticmethod
    def remove_queue():
        pass