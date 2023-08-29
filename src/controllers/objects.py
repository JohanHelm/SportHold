from src.models.objects import BaseObject

class ObjectController():
    def __init__(self, db):
        self.db = db
    def save_object(self, object: BaseObject):
        result = self.db.save_object(object)
        return result

    def get_object_by_name(self, object_name):
        current_object: BaseObject = self.db.get_object(object_name)
        return current_object
