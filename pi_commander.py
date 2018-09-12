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
import plotly_stream as py
import postgres_insert as pg
import aws_insert as aws

def average(list):
	sum = 0
	for read in list:
		sum += float(read)
	return float('%.2f' % (sum / len(list)))

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
				plot_start_time = datetime.datetime.now()
				avg_start_time = datetime.datetime.now()
				ph_reads   = []
				temp_reads = []
				lux_reads  = []
				time_reads = []
				avg_time_reads = []
				avg_ph_reads   = []
				avg_temp_reads = []
				avg_lux_reads  = []

				while True:
					time_now = datetime.datetime.now()
					lines = device.query("R")
					# for i in range(len(lines)):
					# 	# print("line",lines[i])
					# 	if lines[i][0] != '*':
					print("pH Response: " , lines)
					print("thermometer response: ", thermometer.read_temp())
					print("lux response: ", luxsensor.read_lux())
					ambient_humidity, ambient_temperature = dht.read(22, 4)
					print("ambient temp response: ", ambient_temperature)
					print("ambient humidity response: ", ambient_humidity)
					# 		ph_reads.append(lines[i])
					# 		temp_reads.append(thermometer.read_temp())
					# 		lux_reads.append(luxsensor.read_lux())
					# 		time_since_last_avg = (time_now - avg_start_time).seconds
					# 		if time_since_last_avg > 300:
					# 			ins_time = datetime.datetime.now()
					# 			ins_ph = average(ph_reads)
					# 			ins_temp = average(temp_reads)
					# 			ins_lux = average(lux_reads)
					# 			avg_time_reads.append(ins_time)
					# 			avg_ph_reads.append(ins_ph)
					# 			avg_temp_reads.append(ins_temp)
					# 			avg_lux_reads.append(ins_lux)
					# 			avg_start_time = time_now
					# 			ph_reads   = []
					# 			temp_reads = []
					# 			lux_reads  = []
					# 			pg.insert_data(ins_time, ins_ph, ins_temp, ins_lux)
					# 			aws.insert_data(ins_time, ins_ph, ins_temp, ins_lux)
					# 		time_since_last_plot = ((time_now - plot_start_time).seconds / 60)
					# 		if time_since_last_plot > 60: # Push to Plotly every 60 minutes
					# 			try:
					# 				streamed = py.stream_data(avg_time_reads, avg_ph_reads, avg_temp_reads, avg_lux_reads)
					# 				if streamed:
					# 					avg_time_reads = []
					# 					avg_ph_reads   = []
					# 					avg_temp_reads = []
					# 					avg_lux_reads  = []
					# 				plot_start_time = time_now
					# 			except HTTPException as e:
					# 				print("HTTPException: {0}".format(e))
					time.sleep(delaytime)

			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous streaming stopped")
				# py.end_stream()

		# if not a special keyword, pass commands straight to board
		else:
			if len(input_val) == 0:
				lines = read_lines()
				for i in range(len(lines)):
					print(lines[i])
			elif input_val.upper() == "T":
				print("Temperature: " + thermometer.read_temp())
			else:
				device.query(input_val)
				time.sleep(1.3)
				lines = read_lines()
				for i in range(len(lines)):
					print(lines[i])
