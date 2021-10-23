import sqlite3
import numpy as np
import io


# array compression code borrowed from asterio gonzalez response on https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
compressor = 'zlib'


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read().encode(compressor))  # zlib, bz2


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    out = io.BytesIO(out.read().decode(compressor))
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
            image array
        )""")

    def put(self, brand, category, title, price, image):
        self.c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (brand, category, title, price, image))
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
                "image": entry[4],
            })
        return data

    def close(self):
        self.conn.close()
        self.c.close()
