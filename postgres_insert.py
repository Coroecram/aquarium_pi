#!/usr/bin/python

import psycopg2
import datetime
import os

def insert_data(time, ph, temp, lux):

    sql = """INSERT INTO cabrini_tank_2018(observed_at, ph_read, temp_read, lux_read) VALUES(%s,%s,%s,%s) RETURNING id;"""

    conn = None
    connAWS  = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect("host=localhost dbname=aquarium_data user=pi password=raspberry")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (time, ph, temp, lux))
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
