# make 2D histogram from loaded tracing data 
# give it a folder it goes through after the -f --folder tag


import numpy as np
import argparse
import imutils
from datetime import datetime
from scipy import misc
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import colormaps as cm
from collections import deque
import os

date_print = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
print date_print

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder",
	help="path with csv files you want to be analyzed")
args = vars(ap.parse_args())

csv_files = []
root = args["folder"]
for path, subdirs, files in os.walk(root):
    for name in files:
    	extracted_path = os.path.join(path, name)
    	#print extracted_path
        csv_files.append(extracted_path) if "csv" in extracted_path[-3:] else None
	

# check: 
print "Files to be analyzed: "
for element in csv_files:
	print element

all_paths = [] # if you want to analyze multiple files
all_coord_x = []
all_coord_y = []


for idx_csv in xrange(len(csv_files)):

	print "Current file: " + csv_files[idx_csv]

	time_ms = []
	x_coord = []
	y_coord = []

	# extract the information from loaded columns
	with open(csv_files[idx_csv],"r") as saved_pts:
	    for line in saved_pts:
	        #print line
	        time_ms.append(float(line.split(',')[0])/1000)
	        x_coord.append(float(line.split(',')[1]))
	        all_coord_x.append(float(line.split(',')[1]))
	        y_coord.append(float(line.split(',')[2]))
	        all_coord_y.append(float(line.split(',')[2]))
	#close file again
	saved_pts.close()

	diff_x_coord = np.diff(x_coord)
	diff_y_coord = np.diff(y_coord)

	total_path = deque()

	#calculate and filter path length
	for idx in xrange(len(diff_x_coord)):
		total_path.append(math.sqrt(diff_x_coord[idx]**2+diff_y_coord[idx]**2))

	# throw away paths that don't match the minimum length:
	total_path_filtered = np.sum(filter(lambda x: x > 1, total_path))	
	print "Total path: " + str(total_path_filtered)	

	# save in all_paths
	all_paths.append(csv_files[idx_csv] + "," + str(total_path_filtered))

	# Make 2D histogram
	number_bins = 10

	xedges = np.linspace(min(x_coord), max(x_coord), num=number_bins)
	yedges = np.linspace(min(y_coord), max(y_coord), num=number_bins)
	H, xedges, yedges = np.histogram2d(x_coord, y_coord, bins=(xedges, yedges))


	fig = plt.figure(figsize=(15, 8))

	ax = fig.add_subplot(121)
	#ax.set_title('Trace Diagram',fontsize=10)
	plt.plot(x_coord,y_coord,'-k')

	ax.set_xlim(xedges[0], xedges[-1])
	ax.set_ylim(yedges[0], yedges[-1])
	ax.set_aspect('equal')
	ax.invert_yaxis() 
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)


	ax = fig.add_subplot(122)
	#ax.set_title('Interpolated 2D histogram',fontsize=10)
	im = mpl.image.NonUniformImage(ax, interpolation='bilinear', cmap=cm.viridis)
	xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
	ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
	im.set_data(xcenters, ycenters, H)

	ax.images.append(im)
	ax.invert_yaxis() 
	ax.set_xlim(xedges[0], xedges[-1])
	ax.set_ylim(yedges[0], yedges[-1])
	ax.set_aspect('equal')

	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)


	fig.tight_layout()
	plt.show()
	plt.savefig(csv_files[idx_csv] + ".png", dpi=150, bbox_inches='tight',bbox_extra_artists=[ax])
	plt.close('all')


## Add 3D plot

	fig = plt.figure(figsize=(15, 10))

	ax = fig.add_subplot(111)
	#ax.set_title('Trace Diagram',fontsize=10)
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	ax.plot(x_coord,y_coord, time_ms, '-k', linewidth='0.6', alpha=1)
	ax.plot([x_coord[0]],[y_coord[0]], [time_ms[0]], markerfacecolor='b', markeredgecolor='k', marker='o', markersize=6, alpha=0.7)
	ax.plot([x_coord[-1]],[y_coord[-1]], [time_ms[-1]], markerfacecolor='r', markeredgecolor='k', marker='o', markersize=6, alpha=0.7)


	ax.autoscale(enable=True, axis='x', tight='x')
	ax.autoscale(enable=True, axis='y', tight='y')

	plt.xlabel('x',fontsize=10)
	plt.ylabel('y',fontsize=10)
	ax.tick_params(axis='both', which='major', labelsize=9)
	#plt.zlabel('time [s]')
	ax.set_aspect('equal')
	ax.invert_yaxis() 
	ax.pbaspect = [2.0, 0.6, 10]
	#fig.tight_layout()
	plt.show()
	plt.savefig(csv_files[idx_csv] + "_3D.png", dpi=150, bbox_inches='tight',bbox_extra_artists=[ax])
	
	plt.close('all')



# Make 2D histogram for all analyzed paths 

number_bins = 10
xedges = np.linspace(min(all_coord_x), max(all_coord_x), num=number_bins)
yedges = np.linspace(min(all_coord_y), max(all_coord_y), num=number_bins)
H, xedges, yedges = np.histogram2d(all_coord_x, all_coord_y, bins=(xedges, yedges))

fig = plt.figure(figsize=(15, 15))

ax = fig.add_subplot(111)
im = mpl.image.NonUniformImage(ax, interpolation='bilinear', cmap=cm.viridis)
xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im.set_data(xcenters, ycenters, H)

ax.images.append(im)
ax.invert_yaxis() 
ax.set_xlim(xedges[0], xedges[-1])
ax.set_ylim(yedges[0], yedges[-1])
ax.set_aspect('equal')

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

fig.tight_layout()
plt.show()
plt.savefig('/'.join(csv_files[idx_csv].split('/')[:-1]) + "/group average.png", dpi=150, bbox_inches='tight', bbox_extra_artists=[ax])
plt.close('all')

# save all paths_ csv
with open(root + "/all_paths_" + date_print + ".csv","a+") as saved_paths:
    for line in all_paths:
        #print line
        saved_paths.write("%s\n" %line)
        
#close file again
saved_paths.close()
print "Finished!"
print "Saved CSV all paths in folder: " + root


