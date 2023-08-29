from typing import List

from pydantic import BaseModel
from src.models.users import BaseUser


class BaseQueue(BaseModel):
    clients_queue: List[BaseUser] = None


class GlobalQueue(BaseQueue):
    pass
