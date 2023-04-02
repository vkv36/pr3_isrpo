from dataclasses import dataclass


@dataclass
class Product:
    product_id: int = 0
    name_Ingredient: str = ""
    cost_Ingredient: float = 0
    count_Ingredient: int = 0
    type_ID: int = 0

    def __str__(self):
        return f"{self.name_Ingredient}" \
               f" стоимость: {self.cost_Ingredient}" \
               f" на складе: {self.count_Ingredient}"

    def buy(self):
        count = int(input("Введите колчество товара"))
        self.count_Ingredient += count
        return self

    def change_cost(self):
        cost = float(input("Введите стоимость товара"))
        self.cost_Ingredient = cost
        return self
