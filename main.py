import pyodbc
import os
import DB

import Administrator
import buyer


# def user():
#     for row in cursor.execute(f"select * from [User] where Number_Phone = '{Phone}'"):
#         balance = row.Balanse
#     os.system('cls')
#     print("Добро пожаловать")
#     print(f"Ваш баланс {balance} рублей")
#     number = int(input("1 - Купить ролл "))
#     match number:
#         case "1":
#             Purchase_of_goods.Purchase_of_goods()


def Authorization(phone, password) -> int:
    user_id = DB.login(phone, password)
    if user_id is not None:
        match DB.get_role_by_User_Id(user_id):
            case "Администратор":
                Administrator.Administrator(user_id)
            case "Пользователь":
                buyer.buyer(user_id=user_id)
        return user_id
    else:
        print("Введены не вeрные данные")
        return 0


if __name__ == '__main__':
    Phone = input("Введите номер телефона ")
    Password = input("Введите пароль ")

    Authorization(Phone, Password)
