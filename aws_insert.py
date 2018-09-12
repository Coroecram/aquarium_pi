#!/usr/bin/python

import psycopg2
import datetime
import os

def insert_data(time, ph, wtemp, lux, atemp, hum):
    print("avg ph: " + str(ph))
    print("avg wtemp: " + str(wtemp))
    print("avg lux: " + str(lux))
    print("avg atemp: " + str(atemp))
    print("avg hum: " + str(hum))


    sqlAWS = """INSERT INTO garzon_aquarium_2018(observed_at, ph, water_temp, lux, air_temp, humidity) VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"""

    connAWS  = None
    try:
        # connect to the PostgreSQL database
        connAWS = psycopg2.connect("host=" + os.environ["AWS_PG_HOST_2"] + " dbname=aquarium user=" + os.environ["AWS_PG_USER"] + " password=" + os.environ["AWS_PG_PW"])

        # create a new cursor
        curAWS = connAWS.cursor()
        # execute the INSERT statement
        curAWS.execute(sqlAWS, (time, ph, wtemp, lux, atemp, hum))
        # commit the changes to the database
        connAWS.commit()
        # close communication with the database
        curAWS.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("AWS error")
    finally:
        if connAWS is not None:
            connAWS.close()
    return True
