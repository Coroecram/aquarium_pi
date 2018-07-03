#!/usr/bin/python

import plotly.plotly as plotly
import plotly.graph_objs as go

def stream_data(datetimes, pH, temp, lux):
	trace_ph = go.Scatter(
		name='ph_readings',
		x=datetimes,
	    y=pH,
	    yaxis='y',
		hoverinfo=[y,x]
	)

	trace_temp = go.Scatter(
		name='temp_readings',
		x=datetimes,
	    y=temp,
	    yaxis='y2',
		hoverinfo=[y,x]
	)

	trace_lux = go.Scatter(
		name='lux_readings',
		x=datetimes,
	    y=lux,
	    yaxis='y3',
		hoverinfo=[y,x]
	)

	layout = go.Layout(
	    title='Aquarium RPi -- Lux, pH and Temperature',
	    yaxis=dict(
	        title='pH',
		titlefont=dict(
            		color='#1f77b4'
	        ),
        	tickfont=dict(
            		color='#1f77b4'
        	)
	    ),
	    yaxis2=dict(
	        title='Celsius',
			titlefont=dict(
		    color='#ff7f0e'
		),
		tickfont=dict(
		    color='#ff7f0e'
		),
		anchor='free',
		overlaying='y',
		side='left',
		position=0.15
	    ),
		yaxis3=dict(
	    	title='Lux',
			    titlefont=dict(
			    color='#d62728'
			),
			tickfont=dict(
			    color='#d62728'
			),
			anchor='x',
			overlaying='y',
			side='right'
		)
	)

	data = [trace_ph, trace_temp, trace_lux]
	fig = dict(data=data, layout=layout)
	print('Plotting')
	plotly.plot(fig, filename='Aquarium -- Lux, pH and Temperature', fileopt='overwrite', auto_open=False)
