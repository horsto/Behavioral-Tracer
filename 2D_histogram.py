# make 2D histogram from loaded tracing data 

import numpy as np
import argparse
import imutils
from datetime import datetime
from scipy import misc
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import colormaps as cm
from collections import deque
import os

date_print = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
print date_print

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file",
	help="path to .csv file you want to have analyzed")
args = vars(ap.parse_args())

print "File to be analyzed: " + args["file"]

time_ms = []
x_coord = []
y_coord = []

all_path = [] # if you want to analyze multiple files

# extract the information from loaded columns
with open(args["file"],"r") as saved_pts:
    for line in saved_pts:
        #print line
        time_ms.append(float(line.split(',')[0]))
        x_coord.append(float(line.split(',')[1]))
        y_coord.append(float(line.split(',')[2]))
#close file again
saved_pts.close()

diff_x_coord = np.diff(x_coord)
diff_y_coord = np.diff(y_coord)

total_path = deque()

#calculate and filter path length
for idx in xrange(len(diff_x_coord)):
	total_path.append(math.sqrt(diff_x_coord[idx]**2+diff_y_coord[idx]**2))

# show histogram of all calculated paths: 
num_bins = 30
n, bins, patches = plt.hist(total_path, num_bins, normed=1, facecolor='black', alpha=0.5)
# add a 'best fit' line
plt.xlabel('Path lengths')
plt.ylabel('Probability')
plt.title('Histogram of path lengths')
# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.tick_params(labelsize=10) 
fig.tight_layout()
plt.show()
plt.savefig(args["file"] + "histogram.png", dpi=150, bbox_inches='tight')
plt.close('all')

# throw away paths that don't match the minimum length:

total_path_filtered = np.sum(filter(lambda x: x > 1, total_path))	
print "Total path: " + str(total_path_filtered)	

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

# cbar = fig.colorbar(im, fraction=0.032, pad=0, ticks=[0, int(np.amax(H).reshape((1,-1))/2), 
# 	int(np.amax(H).reshape((1,-1)))])
# cbar.ax.set_yticklabels(['0', str(int(np.amax(H).reshape((1,-1))/2)),
#  	str(int(np.amax(H).reshape((1,-1))))])  
# cbar.ax.tick_params(labelsize=10) 

fig.tight_layout()
plt.show()
plt.savefig(args["file"] + ".png", dpi=150, bbox_inches='tight')
plt.close(fig)
