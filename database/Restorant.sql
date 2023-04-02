set ansi_nulls on
go
set ansi_padding on
go
set quoted_identifier on
go

-- create database Restaurant
-- go
use Restaurant
go

create table [dbo].[Card]
(
    ID     int          not null identity (1,1),
    [Name] nvarchar(30) not null,
    Sale   int          not null,
    constraint [PK_Card] primary key clustered
        (ID ASC) on [PRIMARY]
)
go
insert into [dbo].[Card] ([Name], Sale)
values (N'Обычная карта', 1),
       (N'Бронзовая карта', 5),
       (N'Серебренная карта', 10),
       (N'Золотая карта', 20)
go

create table [dbo].[Role]
(
    ID        int          not null identity (1,1),
    Name_Role nvarchar(30) not null,
    constraint [PK_Role] primary key clustered
        (ID ASC) on [PRIMARY]
)
go
insert into [dbo].[Role]([Name_Role])
values (N'Администратор'),
       (N'Пользователь')
go

create table [dbo].[User]
(
    ID           int          not null identity (1,1),
    First_Name   nvarchar(30) not null,
    Second_Name  nvarchar(30) not null,
    Middle_Name  nvarchar(30) not null default (''),
    Number_Phone nvarchar(30) not null,
    Password     nvarchar(30) not null,
    Balance      int          not null default (500),
    Card_ID      int          not null,
    Role_ID      int          not null,

    constraint [FK_Card_Employee] foreign key (Card_ID)
        references [dbo].[Card] (ID),
    constraint [FK_Role_Employee] foreign key (Role_ID)
        references [dbo].[Role] (ID),
    constraint [PK_Employee] primary key clustered
        (ID ASC) on [PRIMARY]
)
go

insert into [User](First_Name, Second_Name, Middle_Name, Number_Phone, Password, Card_ID, Role_ID)
values ('Ivan', 'Ivanov', 'Ivanovich', '88005553535', 'qwerty', 1, 1)

insert into [User](First_Name, Second_Name, Middle_Name, Number_Phone, Password, Card_ID, Role_ID)
values ('Ivan', 'Ivanov', 'Ivanovich', '8', '8', 1, 1)

insert into [User](First_Name, Second_Name, Middle_Name, Number_Phone, Password, Card_ID, Role_ID)
values ('Ivan', 'Ivanov', 'Ivanovich', '7', '7', 1, 2)



create table Type
(
    ID        int          not null identity (1,1),
    Name_Type nvarchar(30) not null,
    constraint [PK_Type] primary key clustered
        (ID ASC) on [PRIMARY]
)
go
insert into Type(Name_Type)
values (N'Мясо'),
       (N'Овощи'),
       (N'Сыр'),
       (N'Соус'),
       (N'Лук'),
       (N'Специальный ингредиент')
go

create table Ingredient
(
    ID               int          not null identity (1,1),
    Name_Ingredient  nvarchar(30) not null,
    Cost_Ingredient  int          not null default (0),
    Count_Ingredient int          not null,
    Type_ID          int          not null,
    constraint [FK_Type_Ingredient] foreign key (Type_ID)
        references Type (ID),
    constraint [PK_Ingredient] primary key clustered
        (ID ASC) on [PRIMARY]
)
go
insert into Ingredient([Name_Ingredient], [Cost_Ingredient], [Count_Ingredient], Type_ID)
values (N'Лук репчатый', 10, 10, 2),
       (N'Лук Зеленый', 10, 10, 2),
       (N'Помидор', 10, 10, 2),
       (N'Соус Тартар', 30, 10, 4),
       (N'Соус Сырный', 30, 10, 4),
       (N'Кетчуп', 30, 10, 4),
       (N'Мазик', 30, 10, 4),
       (N'Моцарелла', 25, 10, 3),
       (N'Пармезан', 20, 10, 3),
       (N'Чеддер', 15, 10, 3),
       (N'Помидор оранжевый', 15, 10, 2),
       (N'Помидор жёлтый', 20, 10, 2),
       (N'Курица', 20, 10, 1),
       (N'Свинина', 30, 10, 1),
       (N'Говядина', 40, 10, 1),
        (N'таракан', 0, 100000, 6)
go

create table Dish
(
    ID         int         not null identity (1,1),
    Name       nvarchar(50) not null,
    Is_Default binary      not null default (0),

    constraint PK_Dish primary key clustered (ID ASC) on [PRIMARY],
)
go

insert into Dish (Name, Is_Default)
values (N'Мясо по французски', 1);

create table Dish_Ingredient
(
    ID            int not null identity (1,1),
    Dish_ID       int not null,
    Ingredient_ID int not null,

    constraint PK_Dish_Ingredient primary key clustered (ID ASC) on [PRIMARY],
    constraint [FK_Dish] foreign key (Dish_ID) references Dish (ID),
    constraint [FK_Ingredient] foreign key (Ingredient_ID) references Ingredient (ID)
);

insert into Dish_Ingredient (Dish_ID, Ingredient_ID)
values (1, 14),
       (1, 1),
       (1, 7),
       (1, 3),
       (1, 9)
GO

create table Cheque
(
    ID          int      not null identity (1,1),
    Date        datetime not null default current_timestamp,
    Cost_Cheque int      not null,
    Dish_ID     int      not null,
    User_ID     int      not null,

    constraint [FK_Dish_Cheque] foreign key ([Dish_ID])
        references Dish (ID),
    constraint [FK_Employee_Cheque] foreign key (User_ID)
        references [User] (ID),
    constraint [PK_Cheque] primary key clustered
        (ID ASC) on [PRIMARY]
)
go

create or alter function get_DishCost(@ID int)
    returns int
    with execute as caller
as
begin
    return (select sum(Cost_Ingredient)
            from Ingredient
                     inner join Dish_Ingredient DI on Ingredient.ID = DI.Ingredient_ID
                     inner join Dish D on D.ID = DI.Dish_ID
            where Dish_ID = @ID)
end
go


insert into Cheque (Cost_Cheque, Dish_ID, User_ID)
values (dbo.get_DishCost(1), 1, 1);
go

create or alter function get_All_Expenses_By_User_ID(@ID int)
    returns int
    with execute as caller
as
begin
    return
        (select sum(Cost_Ingredient)
         from Ingredient
                  inner join Dish_Ingredient DI on Ingredient.ID = DI.Ingredient_ID
                  inner join Dish D on D.ID = DI.Dish_ID
                  inner join Cheque C on D.ID = C.Dish_ID
         where User_ID = @ID)
end
go

select *
from [User]
         inner join dbo.Role R on R.ID = [User].Role_ID;

/*create or alter trigger Cheque_trigger
    on Cheque after delete, update, insert
    as
    begin

    end
    go*/

