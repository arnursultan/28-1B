from database.db_schema import create_tables
from database.db_users import add_user, get_all_users
from database.db_products import add_product, get_all_products

create_tables()

add_user("Johnny", "jonsmith@icloud.com", 25)
add_user("Kurut", "kg@icloud.com", 30)

add_product("PC Game", 4999.99)
add_product("Laptop", 1999.00)

print(" Пользователи:")
for user in get_all_users():
    print(user)

print("\n Продукты:")
for product in get_all_products():
    print(product)