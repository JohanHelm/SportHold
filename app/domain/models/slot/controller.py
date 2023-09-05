from collections import deque

class QueueController:

    def __init__(self):
        self.deque = deque()
    def get(self):
        return self.deque

    def add_list(self, id_list):
        for id in id_list:
            self.deque.append(id)
        return self

    def to_str(self):
        deque_as_list = list(self.deque)
        deque_as_str = ','.join(deque_as_list)
        return deque_as_str

    def from_str(self,deque_as_str):
        self.deque.clear()
        self.deque.extend(deque_as_str.split(","))
        return self

    def remove_first(self):
        self.deque.popleft()

    def remove(self, key):
        self.deque.remove(key)