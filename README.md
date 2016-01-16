# Behavioral tracer
Transferred my video tracing code from Matlab to Python. 
This Python code utilizes various libraries, check dependencies first!

### Mouse tracer
#### Latest version: `mouse_tracker3_multiple.py`
This script processes one or multiple videos (.mov,...). Output: .csv file with tracing information and .png screenshot of the trace in the same folder as input video. See `/example` folder for test movie and output.

Example usage: 
```
mouse_tracker3_multiple.py -s 10 -v 'example/olf5_1.mov'
``` 
* `-s`: How many frames should be skipped
* `-v`: Video file to be processed; comma separated list possible

**Dependencies:** 
* OpenCV 3.0 
* Numpy
* Scipy
* imutils
* TQDM 

!['Screen shot'](Screen_Shot.jpg)

### Post Process Trace
#### Latest version: `2D_histogram_multiple_3D.py`
This script processes the output .csv files of the tracing script (see above). Output: `all_paths_[...].csv`: Names and calculated distances (as example) of analyzed traces. `[...].csv_3D.png`: 3D representation of mouse path (path over time in seconds). `group average.png`: Group average of all analyzed .csv traces. 

Example usage: 
```
2D_histogram_multiple_3D.py -f "example"
``` 
* `-f`: Give (top) folder of .csv files. Will search through folder tree for all available .csv files. 

**Dependencies:** 
* Numpy
* Scipy
* imutils
* Matplotlib

!['Trace and 2D histogram'](example/olf5_1.mov_2016-01-16_17-44-01.csv.png)
!['3D trace representation'](example/olf5_1.mov_2016-01-16_17-44-01.csv_3D.png)



