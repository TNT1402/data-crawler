import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()
HOST_NAME = os.getenv("HOST_NAME")
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST_NAME,
            user=USER_NAME,
            password=USER_PASSWORD,
            database=DB_NAME
        )
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred while connecting to MySQL")
        return None

def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title TEXT,
        img_src TEXT,
        link_href TEXT,
        price TEXT,
        category TEXT
    )
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def save_to_db(connection, data):
    insert_query = """
    INSERT INTO products (title, img_src, link_href, price, category) VALUES (%s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        for category, items in data.items():
            for item in items:
                title = item.get('title')
                img_src = item.get('img_src')
                link_href = item.get('link_href')
                price = item.get('price')
                cursor.execute(insert_query, (title, img_src, link_href, price, category))
        connection.commit()
        print("Data saved to database successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def get_products(connection):
    select_products_query = "SELECT * FROM products WHERE img_src LIKE '%https%' ORDER BY title ASC"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(select_products_query)
        products = cursor.fetchall()
        return products
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

def get_products_by_title(connection, title):
    cursor = connection.cursor(dictionary=True)
    try:
        if title:
            sql = "SELECT * FROM products WHERE title LIKE %s and img_src LIKE '%https%'"
            cursor.execute(sql, ('%' + title + '%',))
        else:
            sql = "SELECT * FROM products WHERE img_src LIKE '%https%'"
            cursor.execute(sql)
        products = cursor.fetchall()
        return products
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

def get_products_categories(connection):
    query = "SELECT DISTINCT category FROM products WHERE img_src LIKE '%https%' "
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        categories = cursor.fetchall()
        return categories
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

def get_products_by_category(connection, category):
    cursor = connection.cursor(dictionary=True)
    try:
        if category:
            sql = "SELECT * FROM products WHERE category = %s AND img_src LIKE '%https%'"
            cursor.execute(sql, (category,))
        else:
            sql = "SELECT * FROM products WHERE img_src LIKE '%https%'"
            cursor.execute(sql)
        products = cursor.fetchall()
        return products
    except Error as e:
        print(f"The error '{e}' occurred")
        return []