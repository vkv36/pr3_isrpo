from os import system

import DB
from models.Product import Product


def Administrator(UserId):
    user = DB.get_user_by_id(UserId)

    while True:
        system('cls')

        print(
            f"""
            Доброго времени суток, {user.FIO}
            
            Баланс: {user.balance}

            1 - Посмотреть список продуктов
            2 - Купить продукты
            3 - Изменить цену продукта
            4 - Посмотреть все покупки
            5 - Посмотреть покупки у пользователя
            6 - Выход
            """)

        action = input("Введите номер действия\n")

        match action:
            case "1":
                print_product_list()
            case "2":
                buy_product()
            case "3":
                change_cost()
            case "4":
                cheque_list()
            case "5":
                user_cheques()
            case "6":
                break


def print_product_list():
    for i in DB.getProducts():
        print(f"{i.product_id}. {i}")


def buy_product():
    print_product_list()
    product_id = int(input("Введите номер продукта\n"))
    product = Product(product_id=product_id)
    product.buy()

    DB.buy_product(product)


def change_cost():
    print_product_list()
    product_id = int(input("Введите номер продукта\n"))
    product = Product(product_id=product_id)
    product.change_cost()

    DB.change_product_cost(product)


def cheque_list():
    for i in DB.get_all_cheques():
        print(i)


def user_cheques():
    phone = input("Введите номер телефона: ")
    user = DB.find_user_by_phone(phone)
    if user == 0:
        print("Пользователь не найден")
        return
    for i in DB.get_cheques_by_usrer_id(user_id=user):
        print(i)
