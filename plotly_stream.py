#!/usr/bin/python

import plotly.plotly as plotly
import plotly.graph_objs as go

def stream_data(datetimes, pH, temp, lux):
	trace_ph = go.Scatter(
		name='ph_readings',
		x=datetimes,
	    y=pH,
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

	trace_lux = go.Scatter(
		name='lux_readings',
		x=datetimes,
	    y=lux,
	    yaxis='y3',
		marker = dict(
		 	color='#2ca02c'
		)
	)

	layout = go.Layout(
	    title='Aquarium RPi - pH,Temperature, and Lux',
	    yaxis=dict(
	    	title='pH',
			titlefont=dict(
            	color='#1f77b4'
	        ),
        	tickfont=dict(
            	color='#1f77b4'
        	),
			dtick=0.25,
			range=[6.5, 7.5]
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
			range=[20, 29]
		),
		yaxis3=dict(
	    	title='Lux',
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
			range=[0,225]
		)
	)

	data = [trace_ph, trace_temp, trace_lux]
	fig = dict(data=data, layout=layout)
	print('Plotting')
	plotly.plot(fig, filename='Aquarium RPi - pH,Temperature, and Lux', fileopt='extend', auto_open=False)
