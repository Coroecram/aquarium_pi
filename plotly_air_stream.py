#!/usr/bin/python

import plotly.plotly as plotly
import plotly.graph_objs as go
from plotly.exceptions import PlotlyRequestError

def stream_air_data(avg_sensor_data):
	trace_lux = go.Scatter(
		name='lux_readings',
		x=avg_sensor_data['time'],
	    	y=avg_sensor_data['lux'],
		marker = dict(
		 color='#1f77b4'
		)
	)

	trace_temp = go.Scatter(
		name='air_temp_readings',
		x=avg_sensor_data['time'],
	   	 y=avg_sensor_data['air_temp'],
	    	yaxis='y2',
		marker = dict(
		 color='#ff7f0e'
		)
	)

	trace_hum = go.Scatter(
		name='hum_readings',
		x=avg_sensor_data['time'],
	    	y=avg_sensor_data['hum'],
	   	 yaxis='y2',
		marker = dict(
		 color='#ff7f0e'
		)
	)

	layout = go.Layout(
	    title='Aquarium RPi - Ambient Lux, Temperature and Humidity',
	    yaxis=dict(
	    	title='Lux',
			titlefont=dict(
            	color='#1f77b4'
	        ),
        	tickfont=dict(
            	color='#1f77b4'
        	),
			dtick=25,
			range=[0, 205]
	    ),
	    yaxis2=dict(
	        title='Temperature`',
			titlefont=dict(
		    	color='#ff7f0e'
			),
			tickfont=dict(
		    	color='#ff7f0e'
			),
			dtick=0.5,
			anchor='free',
			overlaying='y',
			side='left',
			position=0.15,
			range=[20.25, 26.75]
		),
		yaxis3=dict(
	    	title='Humidity',
			    titlefont=dict(
			    color='#2ca02c'
			),
			tickfont=dict(
			    color='#2ca02c'
			),
			dtick=25,
			anchor='x',
			overlaying='y',
			side='right',
			range=[0,100]
		)
	)

	data = [trace_lux, trace_temp, trace_hum]
	fig = dict(data=data, layout=layout)
	print('Plotting')
	try:
		plotly.plot(fig, filename='Aquarium RPi - Ambient Lux, Temperature and Humidity', fileopt='extend', auto_open=False)
		return True
	except PlotlyRequestError as err:
		print(err)
		return False
