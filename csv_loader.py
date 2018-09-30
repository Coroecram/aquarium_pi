#!/usr/bin/python

import psycopg2

#def insert_csv_data():

if __name__ == '__main__':
    create_table = "ALTER TABLE lima_test (id SERIAL PRIMARY KEY, observed_at TIMESTAMPTZ, ph FLOAT(2), water_temp FLOAT(2), lux FLOAT(2), air_temp FLOAT(2), humidity FLOAT(2));"
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect("host=localhost dbname=aquarium_data user=pi password=raspberry")
        # create a new cursor
        cur = conn.cursor()
        cur.execute(create_table)
        # with open('/home/pi/Documents/aquarium_pi/20180720.csv', 'r') as f:
        #     cur.copy_from(f, 'cabrini_tank_2018 ', sep=',', columns=('observed_at','ph_read','temp_read','lux_read'))

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
