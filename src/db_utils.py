import sqlite3
import numpy as np
import io


# array compression code borrowed from unutbu response on https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read()) 


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)


# Our class for storing custom data
class DatabaseHandler():
    """
    A class to help putting product data into our database
    """

    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS products (
            brand text,
            category text,
            title text,
            price text,
            url text,
            image array
        )""")

    def put(self, brand, category, title, price, url, image):
        self.c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", (brand, category, title, price, url, image))
        self.conn.commit()

    def find(self, brand):
        self.c.execute("SELECT * FROM products WHERE brand=?", (brand,))
        data = {}
        for entry in self.c.fetchall():
            if entry[1] not in data:
                data[entry[1]] = []
            data[entry[1]].append({
                "title": entry[2],
                "price": entry[3],
                "link": entry[4],
                "image": entry[5]
            })
        return data

    def close(self):
        self.c.close()
        self.conn.close()
