
from src.models.users import BaseUser
from src.models.objects import BaseObject
from src.models.schedules import BaseSchedule

class InMemoryDB():
    DATABASE = {
        "users": {},
        "objects": {},
        "schedules": {},
        "slots": {},
        "queues": {}
    }

    @classmethod
    def get_user(cls, tg_id):
        db_users = cls.DATABASE["users"]
        user = db_users[tg_id]
        return user

    @classmethod
    def save_user(cls, user: BaseUser):
        db_users = cls.DATABASE["users"]
        db_users[user.tg_id] = user
        return cls.DATABASE["users"][user.tg_id]

    @classmethod
    def get_object(cls, object_name):
        db_objects = cls.DATABASE["objects"]
        current_object = db_objects[object_name]
        return current_object

    @classmethod
    def save_object(cls, object: BaseObject):
        db_objects = cls.DATABASE["objects"]
        db_objects[object.name] = object
        return cls.DATABASE["objects"][object.name]


    @classmethod
    def save_schedule(cls, schedule: BaseSchedule):
        db_schedules = cls.DATABASE["schedules"]
        db_schedules[schedule.id] = schedule
        return schedule

    @classmethod
    def get_schedule(cls, uuid):
        db_schedules = cls.DATABASE["schedules"]
        schedule = db_schedules[uuid]
        return schedule
