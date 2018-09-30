#!/usr/bin/python

import plotly.plotly as plotly
import plotly.graph_objs as go
from plotly.exceptions import PlotlyRequestError

def stream_aqua_data(datetimes, ph, temp):
	trace_ph = go.Scatter(
		name='ph_readings',
		x=datetimes,
	    y=ph,
		marker = dict(
		 	color='#1f77b4'
		)
	)

	trace_temp = go.Scatter(
		name='temp_readings',
		x=datetimes,
	    y=temp,
	    yaxis='y2',
		marker = dict(
		 	color='#ff7f0e'
		)
	)

	layout = go.Layout(
	    title='Aquarium RPi - pH and Temperature',
	    yaxis=dict(
	    	title='ph',
			titlefont=dict(
            	color='#1f77b4'
	        ),
        	tickfont=dict(
            	color='#1f77b4'
        	),
			dtick=0.25,
			range=[6.5, 7.25]
	    ),
	    yaxis2=dict(
	        title='Celsius',
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
		)
	)

	data = [trace_ph, trace_temp]
	fig = dict(data=data, layout=layout)
	print('Plotting')
	try:
		plotly.plot(fig, filename='Aquarium RPi - pH and Temperature', fileopt='extend', auto_open=False)
		return True
	except PlotlyRequestError as err:
		print(err)
		return False
