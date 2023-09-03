from app.domain.models.user.dto import BaseUser

class UserController():
    def __init__(self, db):
        self.db = db
    def save_user(self, user: BaseUser):
        result = self.db.save_user(user)
        return result

    def get_user_by_tg_id(self, tg_id):
        user: BaseUser = self.db.get_user(tg_id)
        return user
