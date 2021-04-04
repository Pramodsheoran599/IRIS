import mysql.connector
from mysql.connector import Error


def insert_user(new_user):
    conn = None
    c = None
    config = {
        'user': 'root',
        'password': '7726',
        'host': 'localhost',
        'database': 'IRIS',
        'port': '3306',
        'raise_on_warnings': True,
    }
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            c = conn.cursor()  # Creating a Cursor

            query = ("insert into User"
                     "(Username, Password, First_Name, Last_Name, Email_id, Contact)"
                     "values(%s, %s, %s, %s, %s, %s)")

            c.execute(query, new_user)
            conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            c.close()
            conn.close()

# class Database_Operations:
#     def __init__(self):
#
#         self.connection = None
#         self.cursor = None
#         config = {
#             'user': 'root',
#             'password': '7726',
#             'host': 'localhost',
#             'database': 'IRIS',
#             'port': '3306',
#             'raise_on_warnings': True,
#         }
#
#         try:
#             self.connection = mysql.connector.connect(**config)
#             self.cursor = self.connection.cursor()
#         except Error as e:
#             print(e)
#
#         finally:
#             if self.connection is not None and self.connection.is_connected():
#                 self.connection.close()
#
#     def insert_user(self, new_user):
#         if self.connection.is_connected():
#             query = ("insert into User"
#                      "(Username, Password, First_Name, Last_Name, Email_id, Contact)"
#                      "values(%s, %s, %s, %s, %s, %s)")
#
#             self.cursor.execute(query, new_user)
#             self.connection.commit()
