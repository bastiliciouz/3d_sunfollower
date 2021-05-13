#!/usr/bin/python3.7
# -*-coding: utf-8-*

import pymysql
import database_user as user        # database_user.py

try:
    db = pymysql.connect(host=f"{user.host}",
                         user=f"{user.benutzer}",
                         password=f"{user.passwd}",
                         database=f"{user.db}")
    print("\n    +++Database connected+++")
except Exception as e:
    print(e)


def aktuell(current_pos_unten, current_pos_oben):
    try:
        with db.cursor() as cursor:
            cursor.execute(f"""INSERT INTO
                                current_pos(current_pos_unten, current_pos_oben)
                                VALUES ({current_pos_unten},{current_pos_oben})""")
            db.commit()

    except Exception as e:
        print(e)


def error(message):
    try:
        with db.cursor() as cursor:
            cursor.execute(f"""INSERT INTO
                                errors(message)
                                VALUES ({message})""")
            db.commit()
    except:
        pass
