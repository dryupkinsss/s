from itertools import product

import pymysql


class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.con = pymysql.connect(
            host='localhost',
            user='root',
            password='59723833',
            database='demo_12'
        )
        self.cursor = self.con.cursor()

    def load_all_products(self):
        query = """
        select p.id, p.name_products, tp.name_type_products, p.article, p.min_price, name_material, name_shop, time_ready
        from products p
        join type_products tp ON p.id_type_products = tp.id
        join materials m ON p.id_materials = m.id
        join shop s ON p.id_shop = s.id
        GROUP BY id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def load_all_shop(self):
        query = "SELECT * FROM shop;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_product_id(self, product_id):
        query = "DELETE from products WHERE id = %s"
        self.cursor.execute(query, (product_id,))
        self.con.commit()

    def load_data_from_table(self, table_name, column_name):
        query = f"SELECT id, {column_name} FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_products_table(self, name_products, id_type_products, article, min_price, id_materials, id_shop, time_ready):
        query = """
        INSERT INTO products (name_products, id_type_products, article, min_price, id_materials, id_shop, time_ready)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (name_products, id_type_products, article, min_price, id_materials, id_shop, time_ready))
        self.con.commit()
