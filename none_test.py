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


def prepend_readings(reads):
	nones = 0
	value = None
	for read in reads:
		if read != None:
			value = read
			break
		nones = nones + 1

	for j in range(nones):
		reads[j] = value

	return reads


def avg_diff_none_reads(reads):
	print("herehere")
	for dim in reads:
		none_count = 0
		idx = 0
		readings = reads[dim]
		for reading in readings:
			print("reading" + str(idx) + ": " + str(reading))
			if reading == None:
				if idx == 0:
					print("here! 51")
					prepend_readings(readings)
					none_count = -1 # To compensate for + 1 at end of loop
				elif none_count == 0:
					pre_base_reading = readings[idx-1]
					print("pre_base_reading: ", pre_base_reading)
				none_count = none_count + 1
			elif none_count > 0:
				n = 1
				difference = reading - pre_base_reading
				from_first_none = idx - none_count
				
				while from_first_none < idx:
					readings[from_first_none] = pre_base_reading + (n * (difference/none_count))
					print("readings: ", readings)
					n = n + 1
					from_first_none = from_first_none + 1
				none_count = 0
			idx = idx + 1
	print("reads: ", reads)
	return reads


def sensor_average(output, reads):	
	avg_diff_none_reads(reads)
	output['ph'].append(average(reads['ph']))
	output['wtemp'].append(average(reads['wtemp']))
	output['lux'].append(average(reads['lux']))
	output['atemp'].append(average(reads['atemp']))
	output['hum'].append(average(reads['hum']))
	output['time'].append(datetime.datetime.now())
	print(output)

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
	reads = initialize_sensor_data()
	output = initialize_sensor_data()
	reads['ph'] = [None, None, None, 1, None, None, None, None, -4000]
	
	sensor_average(output, reads)
