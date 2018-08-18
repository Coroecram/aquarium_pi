#!/usr/bin/python

import psycopg2
import datetime
import os

def insert_data(time, ph, temp, lux):
    print("avg ph: " + str(ph))
    print("avg temp: " + str(temp))
    print("avg lux: " + str(lux)) 


    sqlAWS = """INSERT INTO aquarium_data(observed_at, ph_read, temp_read, lux_read) VALUES(%s,%s,%s,%s) RETURNING id;"""

    connAWS  = None
    try:
        # connect to the PostgreSQL database
        connAWS = psycopg2.connect("host=" + os.environ["AWS_PG_HOST"] + " dbname=aquarium user=" + os.environ["AWS_PG_USER"] + " password=" + os.environ["AWS_PG_PW"])

        # create a new cursor
        curAWS = connAWS.cursor()
        # execute the INSERT statement
        curAWS.execute(sqlAWS, (time, ph, temp, lux))
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
