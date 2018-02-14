import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

def plot(points,
             title,
             xaxis,
             yaxis,
             legend=[],
             loc = 'upper left',
             filename="output.png",
             ymin=0,
             ymax=100,
             xlim=0):

	rcParams.update({'figure.autolayout': True})
	rcParams.update({'font.size': 12})

	plt.figure() 
	colors = ['#00ff99','#0099ff','#ffcc00','#ff5050','#9900cc','#5050ff','#99cccc','#0de4f6']
	shape = ['s-', 'o-', '^-', 'v-', 'x-', 'h-', 's-', 'o-', '^-']

	# points is a list of dictionary values
	i = 0
	for dict_value in points:
		X = [0] + [x[0] for x in sorted(dict_value.items())]
		Y = [0]
		for x in X:
			if x in dict_value:
				Y.append(dict_value[x])
				ymax = max(dict_value[x] + 50, ymax) 
		plt.plot(X, Y, shape[i], linewidth=2.5,markersize=7,color=colors[i])
		i += 1

	

	#X = points_tuple[0]
	#Y = points_tuple[1]
	#i = 0

	#for ya in Y:
	#	print(ya)
	#	plt.plot(X, ya, shape[i], linewidth=2.5,markersize=7,color=colors[i])
	#	i += 1

	plt.legend(legend,loc=loc, prop={"size": 10})
	plt.title(title)
	plt.xlabel(xaxis)
	plt.ylabel(yaxis)
	plt.ylim(ymin=ymin, ymax=ymax) 
	plt.xlim(xmin=xlim, xmax=X[len(X)-1])
	plt.grid(True)
	plt.savefig(filename)
