#!/usr/bin/python

import thermometer_read
import ph_commander
from serial import SerialException
import datetime
import plotly.plotly as plotly

# ph_stream_token   = 'jwsvoct79r'
# temp_stream_token = 'jzdg3fs9du'
# username 	      = 'pythagoraspberry'
# api_key     	  = 'Ip5BaQ26ySV1XLHGPbHC'

def start_stream():
	py.sign_in(username, api_key)
	ph_stream 	  = plotly.Stream(stream_tokens[0])
	temp_stream   = plotly.Stream(stream_tokens[1])

	ph_stream.open()
	temp_stream.open()

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
	    title='Raspberry Pi - pH and Temperature',
	    yaxis=YAxis(
	        title='pH'
	    ),
	    yaxis2=YAxis(
	        title='Celsius',
	        side='right',
	        overlaying="y"
	    )
	)

	data = Data([trace_ph, trace_temp])
	fig = Figure(data=data, layout=layout)

	py.plot(fig, filename='Atlas Streaming pH and Temperature', fileopt='overwrite')

def stream_data(ph, temp):
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # Write the data to your plotly stream
	ph_stream.write({'x': time_now, 'y': ph})
	temp_stream.write({'x': time_now, 'y': temp}) 

def end_stream():
	stream.close()