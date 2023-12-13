from datetime import datetime


class User(object):
    id: int
    name: str
    email: str
    created_at: datetime

    def __init__(self, id: int, name: str, email: str, created_at: datetime):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, created_at={self.created_at})"
