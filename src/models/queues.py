from typing import List

from pydantic import BaseModel
from src.models.users import BaseUser


class BaseQueue(BaseModel):
    owner_queue: List[BaseUser] = None
    visitor_queue: List[BaseUser] = None


class GlobalQueue(BaseQueue):
    pass
