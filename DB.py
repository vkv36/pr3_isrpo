from typing import List

import pyodbc

from models.Cheque import Cheque
from models.Dish import Dish
from models.Product import Product
from models.User import User

db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                    "Server=(localdb)\MSSQLLocalDB;"
                    "Database=Restaurant;"
                    "Trusted_Connection=yes;")
cursor = db.cursor()


def login(phone: str, password: str) -> int:
    return cursor.execute(
        f"""
           select [User].ID
           from [User]
           where Number_Phone = '{phone}' and Password = '{password}'
           """
    ).fetchone().ID


def get_role_by_User_Id(user_id: int) -> str:
    return cursor.execute(
        f"""
        select Name_Role
        from [User]
        inner join Role R2 on R2.ID = [User].Role_ID
        where [User].ID = {user_id}
        """
    ).fetchone().Name_Role


def update_user(user: User) -> User:
    cursor.execute(
        f"""
        update [User] 
        set 
            First_Name = '{user.name}',
            Second_Name = '{user.second_name}',
            Middle_Name = '{user.middle_name}',
            Balance = {user.balance},
            Number_Phone = '{user.phone}',
            Password = '{user.password}',
            Card_ID = {user.card_id},
            Role_ID = {user.role_id}
        where ID = {user.user_id}
        """
    ).commit()
    return user


def getProducts() -> List[Product]:
    products: List[Product] = []

    for i in cursor.execute(
            f"""
        select ID, Name_Ingredient, Cost_Ingredient, Count_Ingredient, Type_ID
        from Ingredient
        """
    ).fetchall():
        products.append(
            Product(
                product_id=i.ID,
                name_Ingredient=i.Name_Ingredient,
                cost_Ingredient=i.Cost_Ingredient,
                count_Ingredient=i.Count_Ingredient,
                type_ID=i.Type_ID
            )
        )
    return products


def get_user_by_id(user_id: int) -> User:
    user = cursor.execute(
        f"""
        select ID, First_Name, Second_Name, Middle_Name, Number_Phone, Password, Balance, Card_ID, Role_ID
        from [User]
        where ID = {user_id}
        """
    ).fetchone()
    return User(
        user_id=user.ID,
        name=user.First_Name,
        second_name=user.Second_Name,
        middle_name=user.Middle_Name,
        phone=user.Number_Phone,
        password=user.Password,
        balance=user.Balance,
        card_id=user.Card_ID,
        role_id=user.Role_ID
    )


def find_user_by_phone(phone: str) -> int:
    try:
        return cursor.execute(
            f"""
                             select [User].ID
                             from [User]
                             where Number_Phone like('{phone}') 
                             """
        ).fetchone().ID
    except:
        return 0


def buy_product(product: Product):
    cursor.execute(
        f"""
        update Ingredient
        set Count_Ingredient = {product.count_Ingredient}
        where ID = {product.product_id}
        """
    ).commit()


def change_product_cost(product: Product):
    cursor.execute(
        f"""
        update Ingredient
        set Cost_Ingredient = {product.cost_Ingredient}
        where ID = {product.product_id}
        """
    ).commit()


def get_dish_by_id(dish_id: int) -> Dish:
    dish = cursor.execute(
        f"""
        select ID, Name, Is_Default
        from Dish
        where ID = {dish_id}
        """
    ).fetchone()

    return Dish(
        ID=dish.ID,
        name=dish.Name,
        is_default=dish.Is_Default
    )


def get_products_by_dish_id(dish_id: int) -> list[Product]:
    products: list[Product] = []

    for i in cursor.execute(
            f"""
        select I.ID, Name_Ingredient, Cost_Ingredient, Count_Ingredient, Type_ID
        from Dish_Ingredient
        inner join Dish D on D.ID = Dish_Ingredient.Dish_ID
        inner join Ingredient I on I.ID = Dish_Ingredient.Ingredient_ID
        where D.ID = {dish_id}
        """
    ).fetchall():
        products.append(
            Product(
                product_id=i.ID,
                name_Ingredient=i.Name_Ingredient,
                cost_Ingredient=i.Cost_Ingredient,
                count_Ingredient=i.Count_Ingredient,
                type_ID=i.Type_ID
            )
        )
    return products


def get_product_by_id(product_id: int) -> Product:
    try:
        product = cursor.execute(f"""
        select ID, Name_Ingredient, Cost_Ingredient, Count_Ingredient, Type_ID
        from Ingredient
        """).fetchone()

        return Product(
            product_id=product.ID,
            name_Ingredient=product.Name_Ingredient,
            cost_Ingredient=product.Cost_Ingredient,
            count_Ingredient=product.Count_Ingredient,
            type_ID=product.Type_ID
        )
    except:
        return Product()


def get_all_cheques() -> list[Cheque]:
    cheques: list[Cheque] = []
    for i in cursor.execute(
            f"""
        select ID, Date, Cost_Cheque, Dish_ID, User_ID
        from Cheque
        """
    ).fetchall():
        ch = Cheque(
            ID=i.ID,
            Date=i.Date,
            Cost_Cheque=i.Cost_Cheque,
            Dish_ID=i.Dish_ID,
            User_ID=i.User_ID,
            dish=get_dish_by_id(i.Dish_ID),
        )
        ch.user = get_user_by_id(ch.User_ID)
        ch.dish.products = get_products_by_dish_id(ch.Dish_ID)
        cheques.append(ch)
    return cheques


def get_cheques_by_usrer_id(user_id: int) -> list[Cheque]:
    cheques: list[Cheque] = []
    for i in cursor.execute(
            f"""
        select ID, Date, Cost_Cheque, Dish_ID, User_ID
        from Cheque
        where User_ID = {user_id}
        """
    ).fetchall():
        ch = Cheque(
            ID=i.ID,
            Date=i.Date,
            Cost_Cheque=i.Cost_Cheque,
            Dish_ID=i.Dish_ID,
            User_ID=i.User_ID,
            dish=get_dish_by_id(i.Dish_ID),
        )
        ch.user = get_user_by_id(ch.User_ID)
        ch.dish.products = get_products_by_dish_id(ch.Dish_ID)
        cheques.append(ch)
    return cheques


def get_all_dishes():
    dishes: list[Dish] = []
    for i in cursor.execute(
            f"""
            select ID, Name, Is_Default
            from Dish
            where Is_Default = 1
            """
    ).fetchall():
        dish = Dish(
            ID=i.ID,
            name=i.Name,
            is_default=i.Is_Default
        )
        dish.products = get_products_by_dish_id(dish.ID)
        dishes.append(dish)
    return dishes


def add_dish(dish: Dish) -> Dish:
    cursor.execute(
        f"""
        insert into Dish 
        values 
            (N'{dish.name}', 0)
        """
    ).commit()
    products = dish.products
    dish = cursor.execute(
        f"""
        select top 1 ID, Name, Is_Default
        from Dish
        order by Id desc 
        """
    ).fetchone()
    dish = Dish(
        ID=dish.ID,
        name=dish.Name,
        is_default=dish.Is_Default
    )

    for i in products:
        cursor.execute(
            f"""
            insert into Dish_Ingredient
            values 
                ({dish.ID}, {i.product_id})
            """
        ).commit()
    dish.products = products
    return dish


def buy(user: User, dish: Dish) -> Cheque | None:
    if dish.ID == 0:
        dish = add_dish(dish)
    cost = cursor.execute(
        f"""
        select dbo.get_DishCost({dish.ID})
        """
    ).fetchone()[0]

    if user.balance < cost:
        return

    for i in dish.products:
        count = cursor.execute(
            f"""
            select Count_Ingredient
            from Ingredient
            """
        ).fetchone().Count_Ingredient
        if count <= 0:
            return
        cursor.execute(
            f"""
            update Ingredient
            set Count_Ingredient = {count - 1}
            where ID = {i.product_id}
            """
        )

    cursor.execute(
        f"""
        insert
        into Cheque (Cost_Cheque, Dish_ID, User_ID)
        values ({cost}, {dish.ID}, {user.user_id})
        """
    ).commit()

    user.balance -= cost

    update_user(user)

    cheque = cursor.execute(
        f"""
        select top 1 ID, Date, Cost_Cheque, Dish_ID, User_ID
        from Cheque
        where User_ID = {user.user_id}
        order by ID desc 
        """
    ).fetchone()

    return Cheque(
        ID=cheque.ID,
        Date=cheque.Date,
        Cost_Cheque=cheque.Cost_Cheque,
        Dish_ID=cheque.Dish_ID,
        User_ID=cheque.User_ID,
        dish=dish,
        user=get_user_by_id(cheque.User_ID)
    )
