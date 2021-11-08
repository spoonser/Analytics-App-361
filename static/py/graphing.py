# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Graphing functions for Analytics application
# ***************************************************************************

import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas.core.base import DataError
import numpy as np
import pandas as pd
import io
import base64


# ***************************************************************************
# * COLORMAPS --- Register colormaps
# ***************************************************************************
cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


# ***************************************************************************
# * PLOTTING FUNCTIONS - Bar, Line, Scatter, Pie charts
# ***************************************************************************

# Create a barchart
def bar_plot(data, cmap, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	data.plot(kind='bar', x=data.keys()[0], y=data.keys()[1], rot=0)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend('')
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


def line_plot(data, cmap, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	data.plot(kind='bar', x=data.keys()[0], y=data.keys()[1], rot=0)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend('')
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


def scatter_plot(data, cmap, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	data.plot(kind='bar', x=data.keys()[0], y=data.keys()[1], rot=0)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend('')
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


def pie_plot(data, cmap, xlabel='', ylabel='', title=''):
	# Plot figure
	img = io.BytesIO()

	data.plot(kind='bar', x=data.keys()[0], y=data.keys()[1], rot=0)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend('')
	plt.savefig(img, format='png')
	img.seek(0)

	plot_url = base64.b64encode(img.getvalue()).decode()	
	plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

	return plot


# ***************************************************************************
# * Plot selector - Returns one of the above function returns depending
# * on input
# ***************************************************************************

def get_plot(graph_type, data, cmap, xlabel='', ylabel='', title=''):
	if graph_type == 'bar':
		return bar_plot(data, cmap, xlabel, ylabel, title)
	
	if graph_type == 'line':
		return line_plot(data, cmap, xlabel, ylabel, title)

	if graph_type == 'scatter':
		return line_plot(data, cmap, xlabel, ylabel, title)

	if graph_type == 'pie':
		return pie_plot(data, cmap, xlabel, ylabel, title)

	return 'Graph generation failed'