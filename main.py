import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_tables(connection):
    create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        code TEXT PRIMARY KEY,
        title TEXT NOT NULL
    );
    """

    create_products_table = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        category_code TEXT NOT NULL,
        unit_price REAL,
        stock_quantity INTEGER,
        store_id INTEGER,
        FOREIGN KEY (category_code) REFERENCES categories (code),
        FOREIGN KEY (store_id) REFERENCES store (id)
    );
    """

    create_store_table = """
    CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL
    );
    """

    cursor = connection.cursor()
    cursor.execute(create_categories_table)
    cursor.execute(create_products_table)
    cursor.execute(create_store_table)
    connection.commit()
    cursor.close()

def insert_sample_data(connection):
    insert_categories = """
    INSERT INTO categories (code, title) VALUES
    ('FD', 'Food products'),
    ('CL', 'Clothes');
    """

    insert_store = """
    INSERT INTO store (id, title) VALUES
    (1, 'Asia'),
    (2, 'Globus'),
    (3, 'Spar');
    """

    insert_products = """
    INSERT INTO products (title, category_code, unit_price, stock_quantity, store_id) VALUES
    ('Chocolate', 'FD', 10.5, 129, 1),
    ('T-Shirt', 'CL', 200.0, 15, 1),
    ('Milk', 'FD', 1.5, 50, 2),
    ('Jeans', 'CL', 40.0, 20, 2),
    ('Bread', 'FD', 2.0, 100, 3);
    """

    cursor = connection.cursor()
    try:
        cursor.execute(insert_categories)
        cursor.execute(insert_store)
        cursor.execute(insert_products)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred while inserting data")
    cursor.close()

def get_stores(connection):
    query = "SELECT id, title FROM store"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_store_products(connection, store_id):
    query = """
    SELECT p.title, c.title as category, p.unit_price, p.stock_quantity 
    FROM products p
    JOIN categories c ON p.category_code = c.code
    WHERE p.store_id = ?
    """
    cursor = connection.cursor()
    cursor.execute(query, (store_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

def main():
    # Path to your SQLite database file
    db_file = "database.db"

    connection = create_connection(db_file)

    if not connection:
        print("Failed to create connection to the database.")
        return

    # Create tables and insert sample data
    create_tables(connection)
    insert_sample_data(connection)

    while True:
        print("Вы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже, для выхода из программы введите цифру 0:")
        stores = get_stores(connection)

        for store in stores:
            print(f"{store[0]}. {store[1]}")

        user_input = input("Введите id магазина или 0 для выхода: ")

        if user_input == '0':
            print("Выход из программы.")
            break

        try:
            store_id = int(user_input)
        except ValueError:
            print("Некорректный ввод, пожалуйста, введите числовое значение.")
            continue

        products = get_store_products(connection, store_id)

        if not products:
            print("Нет продуктов для данного магазина.")
        else:
            for product in products:
                print(f"Название продукта: {product[0]}")
                print(f"Категория: {product[1]}")
                print(f"Цена: {product[2]}")
                print(f"Количество на складе: {product[3]}")
                print("-----------------------------")

if __name__ == "__main__":
    main()
