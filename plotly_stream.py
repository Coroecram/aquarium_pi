#!/usr/bin/python

import thermometer_read
from serial import SerialException
import datetime
import plotly.plotly as plotly

username = 'pythagoraspberry'
api_key   = 'Ip5BaQ26ySV1XLHGPbHC'

def start_stream():
	plotly.sign_in(username, api_key)
	ph_stream 	  = plotly.Stream(stream_tokens[0])
	temp_stream   = plotly.Stream(stream_tokens[1])
	lux_stream 	  = plotly.Stream(stream_tokens[2])

	ph_stream.open()
	temp_stream.open()
	lux_stream.open()

	trace_ph = Scatter(
	    x=[],
	    y=[],
	   stream=Stream(
	        token=ph_stream_token
	    ),
	    yaxis='y'
	)

	trace_temp = Scatter(
	    x=[],
	    y=[],
	    stream=Stream(
	        token=temp_stream_token
	    ),
	    yaxis='y2'
	)

	layout = Layout(
	    title='Cabrini Aquarium RPi - Lux, pH and Temperature',
	    yaxis=YAxis(
	        title='pH'
	    ),
	    yaxis2=YAxis(
	        title='Celsius',
	        side='right',
	        overlaying="y"
	    ),
		yaxis3=YAxis(
	        title='Lux',
	        overlaying="y"
	    )
	)

	data = Data([trace_ph, trace_temp])
	fig = Figure(data=data, layout=layout)

	plotly.plot(fig, filename='Cabrini Aquarium Lux, pH and Temperature', fileopt='overwrite')

def stream_data(ph, temp):
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # Write the data to your plotly stream
	ph_stream.write({'x': time_now, 'y': ph})
	temp_stream.write({'x': time_now, 'y': temp})
	lux_stream.write({'x': time_now, 'y': lux})

def end_stream():
	stream.close()
