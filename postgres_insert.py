#!/usr/bin/python

import psycopg2
import datetime
import os

def insert_data(avg_sensor_data, offset):
    idx = idx + offset
    sql = """INSERT INTO """ + os.environ["LOC_PG_TABLE"] + """(observed_at, ph, water_temp, lux, air_temp, humidity) VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"""

    conn = None
    connAWS  = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect("host=" + os.environ["LOC_PG_HOST"] + " dbname=" + os.environ["LOC_PG_DB"] + " user=" + os.environ["LOC_PG_USER"] + " password=" + os.environ["LOC_PG_PW"] + "")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        while(idx < len(avg_sensor_data['time'])):
            cur.execute(sql, (avg_sensor_data['time'][idx], avg_sensor_data['ph'][idx], avg_sensor_data['wtemp'][idx], avg_sensor_data['lux'][idx], avg_sensor_data['atemp'][idx], avg_sensor_data['hum'][idx]))
            idx = idx + 1
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
