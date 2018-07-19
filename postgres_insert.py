#!/usr/bin/python

import psycopg2
import datetime
import os

def insert_data(time, ph, temp, lux):

    sql = """INSERT INTO aquarium_data
             VALUES(%s,%s,%s,%s) RETURNING id;"""
    conn = None
    connAWS  = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect("host=localhost dbname=test_python user=test_user password=test")
        connAWS = psycopg2.connect("host=" + os.environ["AWS_PG_HOST"] + " dbname=aquarium user=" + os.environ["AWS_PG_USER"] + " password=" + os.environ["AWS_PG_PW"])

        # create a new cursor
        cur = conn.cursor()
        curAWS = connAWS.cursor()
        # execute the INSERT statement
        cur.execute(sql, ('DEFAULT', time, ph, temp, lux))
        curAWS.execute(sql, ('DEFAULT', time, ph, temp, lux))
        # commit the changes to the database
        conn.commit()
        connAWS.commit()
        # close communication with the database
        cur.close()
        curAWS.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if connAWS is not None:
            connAWS.close()
    return True
