#!/usr/bin/python3.7
# -*-coding: utf-8-*

import database_user as user  # database_user.py
import pymysql


class DBConnect:
    def __init__(self):
        self.init_db_connection()

    def init_db_connection(self):
        try:
            self.__db_connection = pymysql.connect(host=f"{user.host}",
                                                   user=f"{user.benutzer}",
                                                   password=f"{user.passwd}",
                                                   database=f"{user.db_connection}")
            print("\n    +++Database connected+++")
        except Exception as e:
            print(e)

    def insert_aktuelle_position(self, current_pos_unten, current_pos_oben):
        try:
            with self.__db_connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO
                                    current_pos(current_pos_unten, current_pos_oben)
                                    VALUES ({current_pos_unten},{current_pos_oben})""")
                self.__db_connection.commit()

        except Exception as e:
            print(e)

    def insert_error_message(self, message):
        try:
            with self.__db_connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO
                                    errors(message)
                                    VALUES ({message})""")
                self.__db_connection.commit()
        except:
            pass
