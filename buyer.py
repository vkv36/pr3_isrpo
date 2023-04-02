import DB
from models.Dish import Dish
from models.Product import Product
from models.User import User


def buyer(user_id: int):
    user = DB.get_user_by_id(user_id)
    user.add_balance()
    user = DB.update_user(user)

    while True:
        print(
            f"""
                    Доброго времени суток, {user.FIO}
                    
                    Баланс: {user.balance}

                    1 - Посмотреть список товаров
                    2 - Купить товар
                    3 - Посмотреть все покупки
                    4 - Выход
                    """)

        action = input("Введите номер действия\n")

        match action:
            case "1":
                dishes_list()
            case "2":
                buy(user)
            case "3":
                cheque_list(user)
            case "4":
                break



def cheque_list(user: User):
    for i in DB.get_cheques_by_usrer_id(user.user_id):
        print(i)

def dishes_list():
    for i in DB.get_all_dishes():
        print(i)


def buy(user: User):
    dishes_list()
    dish_id = int(input("Выберите блюдо для покупки: "))

    dish = DB.get_dish_by_id(dish_id)
    dish.products = DB.get_products_by_dish_id(dish_id)
    dish = change_composition(dish)

    cheque = DB.buy(user, dish)
    if cheque is None:
        print("Произошла ошибка")
        return
    print("Спасибо за покупку, ваш чек")
    print(cheque)


def change_composition(dish: Dish) -> Dish:
    action = input(f"Выбрано блюдо {dish}\n"
                   f"Изменить состав:?д/н\n")
    match action:
        case "д":
            while True:
                action = input("""
                1 - добавить
                2 - удалить
                3 - сохранить
                """)
                match action:
                    case "1":
                        dish = add_product(dish)
                    case "2":
                        dish = delete_product(dish)
                    case "3":
                        return dish
    return dish


def print_product_list():
    for i in DB.getProducts():
        print(f"{i.product_id}. {i}")


def add_product(dish: Dish) -> Dish:
    print_product_list()
    product_id = int(input("\nвыберите продукт: "))
    product: Product = DB.get_product_by_id(product_id)
    dish.products.append(product)
    print(f"Продукт {product} добавлен")
    dish.ID = 0
    return dish


def delete_product(dish: Dish) -> Dish:
    for i in dish.products:
        print(i)
    product_id = int(input("\nвыберите продукт: "))
    product = DB.get_product_by_id(product_id)
    dish.products.remove(product)
    print(f"Продукт {product} удален")
    dish.ID = 0
    return dish
