# Tracing Script written in Python 
Transferred tracing code from Matlab to Python. 
This Python code utilizes various libraries, check dependencies first!

## Mouse tracer
### Last version: `mouse_tracker3_multiple.py`
This script processes one or multiple videos (.mov,...). Output: .csv file with tracing information and .png screenshot of the trace in the same folder as input video. See `/example` folder for test output.

Example usage: 
```
mouse_tracker3_multiple.py -s 10 -v '../blabla.mov'
```
Argument: 
`-s`: How many frames should be skipped
'-v': Video file to be processed; comma separated list possible

**Dependencies:** 
* Numpy
* Scipy
* imutils
* OpenCV 3.0 
* TQDM 

!['Screen shot'](Screen_Shot.jpg)

## Post Process Trace
### Last version: `2D_histogram_multiple_3D.py`
This script processes the output .csv files of the tracing script (see above).

**Dependencies:** 
* Numpy
* Scipy
* imutils
* Matplotlib

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


!['Screen shot'](example_output_2Dhistogram.jpg)

