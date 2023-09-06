from collections import deque

class QueueController:

    def __init__(self):
        self.deque = deque()
    def get_deque(self):
        return self.deque

    def get_list(self):
        deque_as_list = list(self.deque)
        return deque_as_list

    def add_list(self, id_list):
        for id in id_list:
            self.deque.append(id)
        return self

    def to_list(self):
        deque_as_list = list(self.deque)
        return deque_as_list

    def from_list(self,deque_as_list):
        self.deque.clear()
        self.deque.extend(deque_as_list)
        return self

    def remove_first(self):
        self.deque.popleft()

    def remove(self, key):
        self.deque.remove(key)