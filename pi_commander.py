#!/usr/bin/python

import serial
import sys
import time
import string
import board
import busio
import thermometer_read as thermometer
import luxsensor_read as luxsensor
import plotly_stream as py

def read_line():
	"""
	taken from the ftdi library and modified to
	use the ezo line separator "\r"
	"""
	lsl = len('\r')
	line_buffer = []
	while True:
		next_char = ser.read(1)
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

def average(list):
	sum = 0
	for read in list:
		sum += float(read)
	return float('%.2f' % (sum / len(list)))

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
		if input_val.upper().startswith("STREAM"):
			delaytime = float(str.split(input_val, ',')[1])

			send_cmd("C,0") # turn off continuous mode
			#clear all previous data
			time.sleep(1)
			ser.flush()

			# get the information of the board you're polling
			print("Polling sensor every %0.2f seconds, press ctrl-c to stop polling" % delaytime)

			try:
				py.start_stream()
				start_time = datetime.datetime.now()
				ph_reads   = []
				temp_reads = []
				lux_reads  = []
				entries    = 0

				while True:
					send_cmd("R")
					lines = read_lines()
					for i in range(len(lines)):
						# print lines[i]
						if lines[i][0] != '*':
							ph_reads.append(lines[i])
							temp_reads.append(thermometer.read_temp())
							lux_reads.append(luxsensor.read_lux())
							print("pH reading: " + ph_reads[-1])
							print("Temp reading: " + temp_reads[-1])
							print("Lux reading: " + lux_reads[-1])

					time_now = datetime.datetime.now()
					time_since_last = (time_now - start_time).to_minutes()
					if time_since_last > 30: # Push to Plotly every 30 minutes
						try:
							py.stream_data(ph_reads, temp_reads, lux_reads)
							ph_reads, temp_reads, lux_reads = [],[],[]
							start_time = datetime.datetime.now()
						except HTTPException as e:
							print("HTTPException: {0}".format(e))
					time.sleep(delaytime)

			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous streaming stopped")
				end_stream()

		# if not a special keyword, pass commands straight to board
		else:
			if len(input_val) == 0:
				lines = read_lines()
				for i in range(len(lines)):
					print(lines[i])
			elif input_val.upper() == "T":
				print("Temperature: " + read_temp())
			else:
				send_cmd(input_val)
				time.sleep(1.3)
				lines = read_lines()
				for i in range(len(lines)):
					print(lines[i])
