# -*- coding: utf8 -*-

import mysql.connector
import json

MYDB = ""

MYCURSOR = ""


class Data:

    def __init__(self, data):
        self.product_name = data[1]
        self.id = data[2]
        self.nutriscore = data[3]
        self.sugar = data[4]
        self.salt = data[5]
        self.fat = data[6]
        self.energy = data[7]

    def save_product(self, user):
        sql = "INSERT IGNORE INTO products_saved (user, product) " \
              "VALUES (%s, %s)"
        val = (user, self.id)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        input("produit enregistré")

    @classmethod
    def check_database(cls):
        global MYDB, MYCURSOR
        with open("login_bdd.json") as f:
            data = json.load(f)
        try:
            MYDB = mysql.connector.connect(
                host="localhost",
                user=data["user"],
                password=data["password"],
                database="pur_beurre_p5")
            MYCURSOR = MYDB.cursor()
            print("Connection à la database réussie!")
            categories = cls.check_table_categories()
            print("la table categories existe avec",categories ,"catégories." )
            products = cls.check_table_x("products")
            print("la table products existe avec", products, "produits.")
            ingredients = cls.check_table_x("ingredients")
            print("la table ingredients existe avec", ingredients, "ingredients.")
            accounts = cls.check_table_x("accounts")
            print("la table accounts existe avec", accounts, "comptes.")
            products_saved = cls.check_table_x("products_saved")
            print("la table products_saved existe avec", products_saved, "produits.")
            cls.check_table_x("substituts")
            print("la table substituts existe.")
            print(" ")
            if products > 0:
                return "login"
            else:
                return "empty_table"

        except mysql.connector.Error as err:
            if err.errno in (1045, 1044):
                print("Mauvais log SQL.")
                return "create_log"
            elif err.errno == 1049:
                print("database inconue.")
                return "create_database"
            elif err.errno == 1146:
                print("table introuvable.")
                return "create_table"
            else:
                print("Something went wrong: {}".format(err))
                return "quit"

    @classmethod
    def check_table_categories(cls):
        MYCURSOR.execute("SELECT COUNT(DISTINCT category) FROM categories")
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def check_table_x(cls, table):
        MYCURSOR.execute("SELECT COUNT(*) FROM " + table)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def check_database_root(cls, password):
        global MYDB, MYCURSOR
        try:
            MYDB = mysql.connector.connect(
                host="localhost",
                user="root",
                password=password,
                database="pur_beurre_p5")
            MYCURSOR = MYDB.cursor()
            print("Connection à la database réussie!")
            return "access_ok"
        except mysql.connector.Error as err:
            if err.errno == 1045:
                print("Mauvais mot de passe.")
                return "wrong_access"
            elif err.errno == 1049:
                MYDB = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=password)
                MYCURSOR = MYDB.cursor()
                print("Connexion réussie")
                print("database introuvable")
                return "create_database"
            else:
                print("Something went wrong: {}".format(err))
                return "quit"

    @classmethod
    def save_log(cls):
        global MYDB, MYCURSOR
        with open("login_bdd.json") as f:
            data = json.load(f)
        MYDB = mysql.connector.connect(
            host="localhost",
            user=data["user"],
            password=data["password"],
            database="pur_beurre_p5")
        MYCURSOR = MYDB.cursor()

    @classmethod
    def create_database(cls):
        MYCURSOR.execute("CREATE DATABASE pur_beurre_p5")
        MYCURSOR.execute("USE pur_beurre_p5")

    @classmethod
    def tables_exist(cls):
        MYCURSOR.execute("SHOW TABLES")
        myresult = MYCURSOR.fetchall()
        if len(myresult) == 6:
            return True
        else:
            return False

    @classmethod
    def create_tables(cls):
        sql = "DROP TABLE IF EXISTS products, accounts, categories, ingredients, products_saved, substituts"
        MYCURSOR.execute(sql)

        sql = "CREATE TABLE products " \
              "(id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
              "product_name VARCHAR(255), " \
              "_id VARCHAR(30) NOT NULL, " \
              "nutriscore VARCHAR(15), " \
              "sugar VARCHAR(15), " \
              "salt VARCHAR(15), " \
              "fat VARCHAR(31), " \
              "energy VARCHAR(31), " \
              "UNIQUE INDEX idprod (_id), " \
              "FULLTEXT INDEX search (product_name)) " \
              "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        MYCURSOR.execute(sql)
        print("Table products crée")

        sql = "CREATE TABLE accounts " \
              "(id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
              "username VARCHAR(30) NOT NULL, " \
              "password VARCHAR(30), " \
              "UNIQUE INDEX USERNAME (username)) " \
              "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        MYCURSOR.execute(sql)
        print("Table accounts crée")

        sql = "CREATE TABLE categories " \
              "(id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
              "category VARCHAR(255) NOT NULL, " \
              "id_product VARCHAR(30) NOT NULL, " \
              "UNIQUE INDEX IDPROD_CAT (id_product, category)) " \
              "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        MYCURSOR.execute(sql)
        print("Table categories crée")

        sql = "CREATE TABLE ingredients " \
              "(id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
              "ingredient_name VARCHAR(255) NOT NULL, " \
              "rank VARCHAR(15), " \
              "percent DECIMAL(10.0), " \
              "id_product VARCHAR(30) NOT NULL, " \
              "UNIQUE INDEX IDPROD_ING (ingredient_name, id_product)) " \
              "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        MYCURSOR.execute(sql)
        print("Table ingredients crée")

        sql = "CREATE TABLE products_saved " \
              "(id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
              "product VARCHAR(30) NOT NULL, " \
              "user VARCHAR(30) NOT NULL, " \
              "UNIQUE INDEX PRODSAVED (product, user)) " \
              "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        MYCURSOR.execute(sql)
        print("Table products_saved crée")

        sql = "CREATE TABLE substituts " \
              "(id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
              "id_product VARCHAR(30), " \
              "sugar TINYINT(1), " \
              "salt TINYINT(1), " \
              "fat TINYINT(1), " \
              "energy TINYINT(1), " \
              "nutriscore TINYINT(1), " \
              "searchscore INT(3), " \
              "address VARCHAR(255)) " \
              "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        MYCURSOR.execute(sql)
        print("Table substituts crée")

    @classmethod
    def create_log_user(cls, r):
        with open("login_bdd.json") as f:
            data = json.load(f)
        data["user"] = r
        with open("login_bdd.json", "w") as f:
            json.dump(data, f)

    @classmethod
    def create_log_pwd(cls, r):
        with open("login_bdd.json") as f:
            data = json.load(f)
        data["password"] = r
        with open("login_bdd.json", "w") as f:
            json.dump(data, f)
        cls.new_log_sql()

    @classmethod
    def new_log_sql(cls):
        with open("login_bdd.json") as f:
            data = json.load(f)
        print("création du compte")
        user = data["user"]
        pwd = data["password"]
        sql = "CREATE USER %s@'localhost' IDENTIFIED BY %s"
        val = (user, pwd)
        try:
            MYCURSOR.execute(sql, val)
        except mysql.connector.Error as err:
            if err.errno == 1396:
                print("compte déjà existant")
        sql = "GRANT ALL PRIVILEGES ON pur_beurre_p5.* TO %s@'localhost'"
        val = (user,)
        MYCURSOR.execute(sql, val)
        print("Accès accordé.")
        print(" ")

    @classmethod
    def get_saved(cls, user):
        sql = "SELECT products.id, " \
              "products.product_name, " \
              "products_saved.product, " \
              "products.nutriscore, " \
              "products.sugar, " \
              "products.salt, " \
              "products.fat, " \
              "products.energy " \
              "FROM products_saved " \
              "INNER JOIN products " \
              "ON products_saved.product = products._id " \
              "WHERE products_saved.user = %s"
        val = (user,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    @classmethod
    def count_saved(cls, user):
        sql = "SELECT COUNT(*) " \
              "FROM products_saved " \
              "WHERE user = %s"
        val = (user,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def new_account(cls, pwd, user):
        if Data.get_usernames(user):
            sql = "UPDATE accounts " \
                  "SET password = %s " \
                  "WHERE username = %s"
            val = (pwd, user)
        else:
            sql = "INSERT INTO accounts (username, password) " \
                  "VALUES (%s, %s)"
            val = (user, pwd)
        MYCURSOR.execute(sql, val)
        MYDB.commit()

    @classmethod
    def get_password(cls, r, user):
        sql = "SELECT password FROM accounts WHERE username = %s"
        val = (user,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        if r in myresult:
            return True
        else:
            return False

    @classmethod
    def get_usernames(cls, r):
        sql = "SELECT username FROM accounts WHERE username = %s"
        val = (r,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        if myresult == None:
            return False
        else:
            return True

    @classmethod
    def get_categories(cls):
        sql = "SELECT DISTINCT category FROM categories"
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchall()
        categories = []
        for i in myresult:
            categories.append(i[0])
        return categories

    @classmethod
    def search(cls, r, category):
        sql = "SELECT * " \
              "FROM products " \
              "WHERE MATCH(product_name)" \
              "AGAINST (%s) " \
              "AND _id in (SELECT id_product " \
              "FROM categories " \
              "WHERE category = %s)"
        val = (r, category)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    @classmethod
    def count_product(cls, category):
        sql = "SELECT COUNT(*) FROM categories WHERE category = %s"
        val = (category,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def get_products(self, category):
        sql = "SELECT * " \
              "FROM products " \
              "WHERE _id in (SELECT id_product " \
              "FROM categories " \
              "WHERE category = %s)"
        val = (category,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    @classmethod
    def get_product(self, id):
        sql = "SELECT * " \
              "FROM products " \
              "WHERE _id = %s"
        val = (id,)
        MYCURSOR.execute(sql, val)
        myresult = MYCURSOR.fetchone()
        return Data(myresult)

    @classmethod
    def delete_categories(cls, category):
        sql = "DELETE FROM categories WHERE category = %s"
        val = (category,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        print(MYCURSOR.rowcount, "record(s) deleted")
        sql = "DELETE FROM products WHERE _id NOT IN (SELECT id_product FROM categories)"
        MYCURSOR.execute(sql)
        MYDB.commit()
        print(MYCURSOR.rowcount, "record(s) deleted")
        sql = "DELETE FROM ingredients WHERE id_product NOT IN (SELECT _id FROM products)"
        MYCURSOR.execute(sql)
        MYDB.commit()
        print(MYCURSOR.rowcount, "record(s) deleted")
        return False

class Data_substitut_score:
    def __init__(self):
        self.sugar = self.count_score("sugar")
        self.salt = self.count_score("salt")
        self.fat = self.count_score("fat")
        self.energy = self.count_score("energy")
        self.nutriscore = self.count_score("nutriscore")
        self.all = self.count_all()

    def get_products(self, var):
        sql = "SELECT products.id, " \
              "products.product_name, " \
              "products._id, " \
              "products.nutriscore, " \
              "products.sugar, " \
              "products.salt, " \
              "products.fat, " \
              "products.energy " \
              "FROM substituts " \
              "INNER JOIN products " \
              "ON substituts.id_product = products._id " \
              "WHERE substituts." + var + " = 1 " \
                "ORDER BY substituts.searchscore DESC, products." + var
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchall()
        list_products = []
        for i in myresult:
            product = Data(i)
            list_products.append(product)
        return list_products

    def count_all(self):
        sql = "SELECT COUNT(*) " \
              "FROM substituts "
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    def count_score(self, var):
        sql = "SELECT COUNT(*) " \
              "FROM substituts " \
              "WHERE " + var + " = 1"
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchone()
        return myresult[0]

    @classmethod
    def init_substitut(cls, id):
        sql = "TRUNCATE TABLE substituts "
        MYCURSOR.execute(sql)
        MYDB.commit()

        sql = "INSERT INTO substituts (id_product)" \
              "SELECT DISTINCT id_product " \
              "FROM categories " \
              "WHERE category in " \
              "(SELECT category " \
              "FROM categories " \
              "WHERE id_product = %s)"
        val = (id,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        cls.init_stat(id, "sugar")
        cls.init_stat(id, "salt")
        cls.init_stat(id, "fat")
        cls.init_stat(id, "energy")
        cls.init_stat(id, "nutriscore")
        cls.init_score_search(id)

    @classmethod
    def init_stat(cls, id, var):
        sql = "UPDATE substituts " \
              "SET " + var + " = 1 " \
                             "WHERE id_product in " \
                             "(SELECT _id " \
                             "FROM products " \
                             "WHERE " + var + " != 'non communiqué' " \
                                              "AND " + var + " < (SELECT " + var + " " \
                                                                                   "FROM products WHERE _id = %s))  "
        val = (id,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()

        sql = "UPDATE substituts " \
              "SET " + var + " = 0 " \
                             "WHERE id_product in " \
                             "(SELECT _id " \
                             "FROM products " \
                             "WHERE " + var + " = 'non communiqué' OR " \
                                              "" + var + " >= (SELECT " + var + " " \
                                                                                "FROM products WHERE _id = %s)) "
        val = (id,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()

    @classmethod
    def init_score_search(cls, id):
        sql = "SELECT id_product " \
              "FROM substituts"
        MYCURSOR.execute(sql)
        myresult = MYCURSOR.fetchall()
        for i in myresult:
            sql = "UPDATE substituts " \
                  "SET searchscore = (SELECT COUNT(*) " \
                  "FROM ingredients " \
                  "WHERE id_product = %s " \
                  "AND ingredient_name in " \
                  "(SELECT ingredient_name " \
                  "FROM ingredients " \
                  "WHERE id_product = %s)) " \
                  "WHERE id_product = %s"
            val = (i[0], id, i[0])
            MYCURSOR.execute(sql, val)
            MYDB.commit()

class Datas_New_product:

    def __init__(self, data, category):
        self.product = Datas_product(data)
        self.ingredients = Datas_ingredients(data["ingredients"])
        self.category = category

    def insert(self):
        self.product.insert(self.category)
        self.ingredients.insert(self.product.id)

class Datas_product:
    def __init__(self, data):
        self.name = self.get_name(data)
        self.id = data["_id"]
        self.nutriscore = self.get_nutriscore(data)
        self.sugar = self.get_sugar(data["nutriments"])
        self.salt = self.get_salt(data["nutriments"])
        self.fat = self.get_fat(data["nutriments"])
        self.energy = self.get_energy(data["nutriments"])

    def insert(self, category):
        val = (category,
               self.id)
        sql = "INSERT IGNORE INTO categories (category, id_product) " \
              "VALUES (%s, %s)"
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        val = (self.name,
               self.id,
               self.nutriscore,
               self.sugar,
               self.salt,
               self.fat,
               self.energy
               )
        sql = "INSERT IGNORE INTO products (product_name, _id, nutriscore, sugar, salt, fat, energy) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        MYCURSOR.execute(sql, val)
        MYDB.commit()

    def get_name(self, data):
        if "product_name_fr" in data.keys():
            return data["product_name_fr"]
        elif "product_name" in data.keys():
            return data["product_name"]
        elif "brands" in data.keys():
            return data["brands"]
        else:
            return "nom_inconnu"

    def get_nutriscore(self, data):
        if "nutriscore_grade" in data.keys():
            return data["nutriscore_grade"]
        else:
            return "non communiqué"

    def get_salt(self, data):
        if "salt" in data.keys():
            return data["salt"]
        else:
            return "non communiqué"

    def get_sugar(self, data):
        if "sugars" in data.keys():
            return data["sugars"]
        else:
            return "non communiqué"

    def get_fat(self, data):
        if "fat" in data.keys():
            return data["fat"]
        else:
            return "non communiqué"

    def get_energy(self, data):
        if "energy" in data.keys():
            return data["energy"]
        else:
            return "non communiqué"

class Datas_ingredients:

    def __init__(self, data):
        self.ingredients = self.get_ingredients(data)

    def insert(self, id_product):
        for i in self.ingredients:
            val = (i.name,
                   i.rank,
                   i.percent,
                   id_product
                   )
            sql = "INSERT IGNORE INTO ingredients (ingredient_name, rank, percent, id_product) " \
                  "VALUES (%s, %s, %s, %s)"
            MYCURSOR.execute(sql, val)
            MYDB.commit()

    def get_ingredients(self, data):
        ingredients = []
        for i in range(10):
            if i < len(data):
                ingredient = Datas_ingredient(data[i])
                ingredients.append(ingredient)
        return ingredients

class Datas_ingredient:
    def __init__(self, data):
        self.name = data["text"]
        self.percent = self.get_percent_max(data)
        self.rank = self.get_rank(data)

    def get_rank(self, data):
        if "rank" in data.keys():
            return data["rank"]
        else:
            return 99

    def get_percent_max(self, data):
        if "percent_max" in data.keys():
            return data["percent_max"]
        else:
            return 0
