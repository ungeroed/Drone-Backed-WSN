#!/usr/bin/python2

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy 

def read_data_file(filename):
	data = []
	errors = []

	with open(filename, 'r') as f:
		f.readline()

		for line in f:
			parts = line[:-1].split(' ')
			
			if len(parts[0]) == 0 or len(parts[1]) == 0 or parts[1] == '0':
				errors.append( (int(parts[0]), 1) )
				continue
				
			try:
				distance = int(parts[0])
				value = float(parts[1])
				time = float(parts[2])
			except:
				errors.append( (int(parts[0]), 1) )
				continue

			data.append( (distance, value, time) )

	return data, errors

def group_data(data):
	groups = {}
	for group in set(map(lambda x: x[0], data)):
		groups[group] = []

	for d in data:
		groups[d[0]].append(d[1])

	return groups

def plot(ax, data, style, label, markersize=1):
	data = sorted(data)
	xs = map( lambda x: x[0], data )
	ys = map( lambda x: x[1], data )
	lines = ax.plot(xs, ys, style, markersize=markersize, label=label)
	plt.setp(lines, linewidth=2.0)

def visualize_data(filename, title):
	data, errors = read_data_file(filename)

	data_groups = group_data(data)
	mean_data = [ ( key, numpy.mean(data_groups[key]) ) for key in data_groups ]
	median_data = [ ( key, numpy.median(data_groups[key]) ) for key in data_groups ]
	mode_data = [ ( key, numpy.bincount(data_groups[key]).argmax() ) for key in data_groups ]

	error_groups = group_data(errors)
	error_sums = [ ( key, sum(error_groups[key]) ) for key in error_groups ]

	# Construct the visualization
	fig = plt.figure(1)
	fig.suptitle(title, fontsize=14, fontweight='bold')

	# Data plot
	ax = fig.add_subplot(111)
	plt.xlabel('Distance (cm)')
	plt.ylabel('Sound pressure level (dB)')
	plt.axis([ 0, 330, 130, 200 ])

	plot(ax, data, 'co', 'Data', markersize=0.5)
	plot(ax, mean_data, 'b-', 'Mean')
	plot(ax, median_data, 'g-', 'Median')
	plot(ax, mode_data, 'r-', 'Mode')

	ax.legend()
	ax.grid()

	# Error plot
	#ax2 = fig.add_subplot(212)
	#plt.xlabel('Distance (cm)')
	#plt.ylabel('Number of dropped packages')

	#plot(ax2, error_sums, 'r-', 'Dropped packages')

	#ax2.legend()
	#ax2.grid()

	plt.show()

if __name__ == '__main__':
	#visualize_data('../measurements/radio_ack.csv', 'Radio acknowledge')
	#visualize_data('../measurements/radio_echo.csv', 'Radio echo')
	visualize_data('../measurements/drone_sound.csv', 'Drone sound')
	visualize_data('../measurements/drone_sound_outside.csv', 'Drone sound outside')
	#visualize_data('../measurements/range.csv', 'Range')
