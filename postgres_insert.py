#!/usr/bin/python

import psycopg2
import datetime
import os

def insert_data(time, ph, wtemp, lux, atemp, hum):

    sql = """INSERT INTO lima_test(observed_at, ph, water_temp, lux, air_temp, humidity) VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"""

    conn = None
    connAWS  = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect("host=localhost dbname=aquarium_data user=pi password=raspberry")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (time, ph, wtemp, lux, atemp, hum))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("LOCAL PG")
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True
