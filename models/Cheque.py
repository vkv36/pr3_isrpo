from dataclasses import dataclass
from datetime import datetime

from models.Dish import Dish
from models.User import User


@dataclass
class Cheque:
    ID: int = 0
    Date: datetime = datetime.now()
    Cost_Cheque: int = 0
    Dish_ID: int = 0
    User_ID: int = 0

    dish: Dish = None
    user: User = None

    def __str__(self):
        return f"{self.ID}- {self.Date} {self.Cost_Cheque} {self.dish.name} {self.user.FIO}"

