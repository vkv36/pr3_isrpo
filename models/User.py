import random
from dataclasses import dataclass


@dataclass
class User:
    name: str = ""
    second_name: str = ""
    middle_name: str = ""
    phone: str = ""
    password: str = ""
    balance: float = 500
    user_id: int = None
    card_id: int = None
    role_id: int = None

    def add_balance(self):
        r = random.randint(20, 40)
        self.balance += (self.balance / 100) * r

    @property
    def FIO(self):
        return f"{self.name} {self.second_name} {self.middle_name}"
