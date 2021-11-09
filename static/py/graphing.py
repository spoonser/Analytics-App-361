# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Graphing functions for Analytics application
# ***************************************************************************

import matplotlib.pyplot as plt
from matplotlib import cm
from pandas.core.base import DataError
import numpy as np
import pandas as pd
import io
import base64


# ***************************************************************************
# * PLOTTING FUNCTIONS - Bar, Line, Scatter, Pie charts
# ***************************************************************************

# Create a barchart
def bar_plot(data, colors, xaxis, yaxis, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	cmap = cm.get_cmap(colors)(np.linspace(0.2, 0.7, len(data)))

	data.plot(kind='bar', x=xaxis, y=yaxis, legend=False, color=cmap, rot=0)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


def line_plot(data, colors, xaxis, yaxis, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	cmap = cm.get_cmap(colors)(np.linspace(0.2, 0.7, len(data)))

	data.plot(kind='line', x=xaxis, y=yaxis, color=cmap, rot=0)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend('')
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


def scatter_plot(data, colors, xaxis, yaxis, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	cmap = cm.get_cmap(colors)(np.linspace(0.2, 0.7, len(data)))

	data.plot(kind='scatter', x=xaxis, y=yaxis, color=cmap)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend('')
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


def pie_plot(data, colors, xaxis, yaxis, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	cmap = cm.get_cmap(colors)(np.linspace(0.2, 0.7, len(data)))

	data.set_index(xaxis, inplace=True)
	print(data.loc[:, data.keys()[0]])
	data.plot.pie(y=yaxis, colors=cmap)
	plt.xlabel('')
	plt.ylabel('')
	plt.title(title)
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


# ***************************************************************************
# * Plot selector - Returns one of the above function returns depending
# * on input
# ***************************************************************************

def get_plot(graph_type, data, colors, xaxis, yaxis, xlabel='', ylabel='', title=''):
	if graph_type == 'bar':
		return bar_plot(data, colors, xaxis, yaxis, xlabel, ylabel, title)
	
	if graph_type == 'line':
		return line_plot(data, colors, xaxis, yaxis, xlabel, ylabel, title)

	if graph_type == 'scatter':
		return line_plot(data, colors, xaxis, yaxis, xlabel, ylabel, title)

	if graph_type == 'pie':
		return pie_plot(data, colors, xaxis, yaxis, xlabel, ylabel, title)

	return 'Graph generation failed'