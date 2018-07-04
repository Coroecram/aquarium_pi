#!/usr/bin/python
 
import psycopg2
import datetime
 
def insert_data(time, ph, temp, lux):
    	
    sql = """INSERT INTO aquarium_data
             VALUES(%s,%s,%s,%s) RETURNING id;"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect("host=localhost dbname=test_python user=test_user password=test")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, ('DEFAULT', time, ph, temp, lux))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    return True