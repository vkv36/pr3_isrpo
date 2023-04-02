from dataclasses import dataclass

from models.Product import Product


@dataclass
class Dish:
    ID: int = 0
    name: str = ""
    is_default: bool = False

    products: list[Product] = list[Product]

    def __str__(self):
        return f"{self.ID} {self.name}"

    def show_composition(self):
        for i in self.products:
            print(i)
