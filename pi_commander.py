#!/usr/bin/python

import serial
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

def read_line():
	"""
	taken from the ftdi library and modified to
	use the ezo line separator "\r"
	"""
	lsl = len('\r')
	line_buffer = []
	while True:
		next_char = ser.read(1).decode()
		if next_char == '':
			break
		line_buffer.append(next_char)
		if (len(line_buffer) >= lsl and
				line_buffer[-lsl:] == list('\r')):
			break
	return ''.join(line_buffer)

def read_lines():
	"""
	also taken from ftdi lib to work with modified readline function
	"""
	lines = []
	try:
		while True:
			line = read_line()
			if not line:
				break
				ser.flush_input()
			lines.append(line)
		return lines

	except serial.SerialException as e:
		print("Error, ", e)
		return None

def send_cmd(cmd):
	"""
	Send command to the Atlas pH Sensor.
	Before sending, add Carriage Return at the end of the command.
	:param cmd:
	:return:
	"""
	buf = cmd + "\r"     	# add carriage return
	try:
		ser.write(buf.encode('utf-8'))
		return True
	except serial.SerialException as e:
		print("Error, ", e)
		return None

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
	print("    Any commands entered are passed to the pH reader via UART except:")
	print("    Stream,xx.x command continuously polls the board every xx.x seconds and streams to plotly (https://plot.ly/~Pythagoraspberry/25)")
	print("    Pressing ctrl-c will stop the polling\n")
	print("    Press enter to receive all data in buffer (for continuous mode) \n")

	# to get a list of ports use the command:
	# python -m serial.tools.list_ports
	# in the terminal
	usbport = '/dev/ttyAMA0' # change to match your pi's setup

	print("Opening serial port now...")

	try:
		ser = serial.Serial(usbport, 9600, timeout=0)
	except serial.SerialException as e:
		print("Error, ", e)
		sys.exit(0)

	while True:
		input_val = input("Enter command: ")

		# continuous polling command automatically polls the board
		if input_val.upper().startswith("POLL"):
			delaytime = float(str.split(input_val, ',')[1])

			send_cmd("C,0") # turn off continuous mode
			#clear all previous data
			time.sleep(1)
			ser.flush()

			# get the information of the board you're polling
			print("Polling sensor every %0.2f seconds, press ctrl-c to stop polling" % delaytime)

			try:
				last_plot_time = datetime.datetime.now()
				last_avg_time = datetime.datetime.now()

				sensor_data = initialize_sensor_data()
				avg_sensor_data = initialize_sensor_data()
				while True:
					time_now = datetime.datetime.now()
					send_cmd("R")
					lines = read_lines()
					for i in range(len(lines)):
						# print("line",lines[i])
						if lines[i][0] != '*':
							# print("Response: " , lines[i])
							ph_reads.append(lines[i])
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

						aws.insert_data(avg_sensor_data['ph'],
						 			   avg_sensor_data['wtemp'],
									   avg_sensor_data['lux'],
									   avg_sensor_data['atemp'],
									   avg_sensor_data['hum'] )

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
				send_cmd("FIND")
			elif input_val.upper() == "WT":
				print("Water Temperature: " + thermometer.read_temp())
			elif input_val.upper() == "AT":
				hum, atemp = dht.read(22, 4)
				print("Air Temperature: " + atemp)
			elif input_val.upper() == "HUM":
				hum, atemp = dht.read(22, 4)
				print("Humidity: " + hum)
			elif input_val.upper() == "AMB":
				hum, atemp = dht.read(22, 4)
				print("Air Temperature: " + atemp)
				print("Humidity: " + hum)
			elif input_val.upper() == "LUX":
				print("Lux: " + luxsensor.read_lux())
			else:
				send_cmd(input_val)
				time.sleep(1.3)
				lines = read_lines()
				for i in range(len(lines)):
					print(lines[i])
