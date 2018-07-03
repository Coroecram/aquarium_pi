#!/usr/bin/python

import thermometer_read
from serial import SerialException
import datetime
import plotly.plotly as plotly

ph_stream 	= None
temp_stream = None
lux_stream 	= None
username       = 'pythagoraspberry'
api_key           = 'Ip5BaQ26ySV1XLHGPbHC'

def start_stream():
	plotly.sign_in(username, api_key)
	ph_stream 	  = plotly.Stream('jwsvoct79r')
	temp_stream   = plotly.Stream('jzdg3fs9du')
	lux_stream 	  = plotly.Stream('ecdqbv0uc9')

	ph_stream.open()
	temp_stream.open()
	lux_stream.open()

	trace_ph = plotly.Scatter(
	    x=[],
	    y=[],
	   stream=ph_stream,
	    yaxis='y'
	)

	trace_temp = plotly.Scatter(
	    x=[],
	    y=[],
	    stream=temp_stream,
	    yaxis='y2'
	)

	trace_lux = plotly.Scatter(
	    x=[],
	    y=[],
	    stream=temp_stream,
	    yaxis='y3'
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

	data = Data([trace_ph, trace_temp, trace_lux])
	fig = Figure(data=data, layout=layout)

	plotly.plot(fig, filename='Cabrini Aquarium Lux, pH and Temperature', fileopt='overwrite')

def stream_data(times, ph, temp, lux):
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # Write the data to your plotly stream
	ph_stream.write({'x': times, 'y': ph})
	temp_stream.write({'x': times, 'y': temp})
	lux_stream.write({'x': times, 'y': lux})

def end_stream():
	stream.close()
