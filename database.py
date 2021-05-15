#!/usr/bin/python3.7
# -*-coding: utf-8-*

import pymysql

import database_user as user  # database_user.py


class DBConnect:
    def __init__(self):
        self.init_db_connection()

    def init_db_connection(self):
        try:
            self.db_connection = pymysql.connect(host=f"{user.host}",
                                                 user=f"{user.benutzer}",
                                                 password=f"{user.passwd}",
                                                 database=f"{user.db_connection}")
            print("\n    +++Database connected+++")
        except Exception as e:
            print(e)

    def insert_aktuell(self, current_pos_unten, current_pos_oben):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO
                                    current_pos(current_pos_unten, current_pos_oben)
                                    VALUES ({current_pos_unten},{current_pos_oben})""")
                self.db_connection.commit()

        except Exception as e:
            print(e)

    def insert_error(self, message):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO
                                    errors(message)
                                    VALUES ({message})""")
                self.db_connection.commit()
        except:
            pass
