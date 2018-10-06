#!/usr/bin/python

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
from vendor import i2c
from http.client import HTTPException
import sys
import datetime
import time
import string
import board
import busio
import thermometer_read as thermometer
import luxsensor_read as luxsensor
import Adafruit_DHT as dht
import plotly_aqua_stream as aqua_py
import plotly_air_stream as air_py
import postgres_insert as pg
import aws_insert as aws


def average(data):
	sum = 0
	for read in data:
		sum += float(read)
	return float('%.2f' % (sum / len(data)))

def sensor_average(output, input):
	output['ph'].append(average(input['ph']))
	output['temp'].append(average(input['temp']))
	output['lux'].append(average(input['lux']))
	output['atemp'].append(average(input['atemp']))
	output['hum'].append(average(input['hum']))
	output['time'].append(datetime.datetime.now())
	return output

def initialize_sensor_data():
	return {
				'ph'    : [],
				'wtemp' : [],
				'lux'   : [],
				'atemp' : [],
				'hum'   : [],
				'time'  : []
			}

def append_sensor_data(sensor_data, ph, wtemp, lux, atemp, hum, time):
		sensor_data['ph'].append(ph)
		sensor_data['wtemp'].append(wtemp)
		sensor_data['lux'].append(lux)
		sensor_data['atemp'].append(atemp)
		sensor_data['hum'].append(hum)
		sensor_data['time'].append(time)

if __name__ == '__main__':
	device = i2c.AtlasI2C() 	# creates the I2C port object, specify the address or bus if necessary

	print("    Any commands entered are passed to the pH reader via UART except:")
	print("    Stream,xx.x command continuously polls the board every xx.x seconds and streams to plotly (https://plot.ly/~Pythagoraspberry/25)")
	print("    Pressing ctrl-c will stop the polling\n")
	print("    Press enter to receive all data in buffer (for continuous mode) \n")

	while True:
		input_val = input("Enter command: ")

		if input_val.upper().startswith("LIST_ADDR"):
			devices = device.list_i2c_devices()
			for i in range(len (devices)):
				print(devices[i])

		# address command lets you change which address the Raspberry Pi will poll
		elif input_val.upper().startswith("ADDRESS"):
			addr = int(string.split(input, ',')[1])
			device.set_i2c_address(addr)
			print("I2C address set to " + str(addr))

		# continuous polling command automatically polls the board
		elif input_val.upper().startswith("POLL"):
			delaytime = float(str.split(input_val, ',')[1])

			device.query("C,0") # turn off continuous mode
			#clear all previous data
			time.sleep(1)

			# get the information of the board you're polling
			print("Polling sensor every %0.2f seconds, press ctrl-c to stop polling" % delaytime)

			try:
				last_plot_time = datetime.datetime.now()
				last_avg_time = datetime.datetime.now()

				sensor_data = initialize_sensor_data()
				avg_sensor_data = initialize_sensor_data()

				while True:
					time_now = datetime.datetime.now()
					ph    = device.query("R")
					wtemp = thermometer.read_temp()
					lux = luxsensor.read_lux()
					hum, atemp = dht.read(22, 4)
					append_sensor_data(sensor_data, ph, wtemp, lux, atemp, hum, time_now)
					print("Time: ", time_now)
					print("pH Response: " , ph)
					print("thermometer response: ", wtemp)
					print("lux response: ", lux)
					print("ambient temp response: ", atemp)
					print("ambient humidity response: ", hum)
					time_since_last_avg = (time_now - last_avg_time).seconds
					if time_since_last_avg > 300:
						last_avg_time = time_now
						sensor_average(avg_sensor_data, sensor_data)

						pg.insert_data(avg_sensor_data['ph'],
						 			   avg_sensor_data['wtemp'],
									   avg_sensor_data['lux'],
									   avg_sensor_data['atemp'],
									   avg_sensor_data['hum'] )

						# aws.insert_data(avg_sensor_data['ph'],
						#  			   avg_sensor_data['wtemp'],
						# 			   avg_sensor_data['lux'],
						# 			   avg_sensor_data['atemp'],
						# 			   avg_sensor_data['hum'] )

						time_since_last_plot = ((time_now - last_plot_time).seconds / 60)
						if time_since_last_plot > 60: # Push to Plotly every 60 minutes
						  try:
						    aqua_streamed = aqua_py.stream_aqua_data(avg_sensor_data)
						    air_streamed = air_py.stream_air_data(avg_sensor_data)
						    if aqua_streamed and air_streamed:
						      avg_sensor_data = initialize_sensor_data()
						      last_plot_time = time_now
						  except HTTPException as e:
						    print("HTTPException: {0}".format(e))
						time.sleep(delaytime)
						except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
						print("Continuous streaming stopped")
						py.end_stream()



		# if not a special keyword, pass commands straight to board
		else:
			if len(input_val) == 0:
				device.query("FIND")
			elif input_val.upper() == "WT":
				print("Water Temperature: ", thermometer.read_temp())
			elif input_val.upper() == "AT":
				hum, atemp = dht.read(22, 4)
				print("Air Temperature: ", atemp)
			elif input_val.upper() == "HUM":
				hum, atemp = dht.read(22, 4)
				print("Humidity: ", hum)
			elif input_val.upper() == "AMB":
				hum, atemp = dht.read(22, 4)
				print("Air Temperature: ", atemp)
				print("Humidity: ", hum)
			elif input_val.upper() == "LUX":
				print("Lux: ", luxsensor.read_lux())
			else:
				print(device.query(input_val))
