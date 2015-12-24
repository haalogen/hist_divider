"""
This is a script for dividing the histogram of Grayscale image into N intervals ("shades of gray"), by the means of integral sums of the histogram.

Idea:

All intervals should have approximately equal integral sums.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image


img_fname = sys.argv[1] # Image filename
N = int(sys.argv[2]) # Wanted number of intervals

fatal_msg = """
N must be less or equal than 128 !!! (or even 100)
because often there are lots of shades that don't have pixels 
of that shade on the picture"""

if N > 128:
    print fatal_msg
    sys.exit(1)
# Output: array (of pairs) of shape (N, 2); 
# each pair: [left_margin, right_margin]
intervals = np.zeros((N, 2))


# Open the image and convert to Grayscale
img = Image.open(img_fname).convert('L') # RGB -> [0..255]

# Color histogram of picture in Grayscale
hist = img.histogram()


# Algorithm
# Calculate integral sums here
full_sum = sum(hist) # Full integral sum (of the whole spectrum)
real_sum = np.zeros(N) # Calculated (real) sums
interval_sum = full_sum // N # Integral sum of each interval

# interval == [left_margin, right_margin]
left_margin = 0 
right_margin = 0

tmp_sum = 0 # Temporary sum
interval_ind = 0 # Interval index: runs from 0 to N-1
# Integrate histogram until tmp_sum >= interval_sum
# Then add new margins; zero tmp_sum
for right_margin in xrange(0, 256): # [0..255]
    tmp_sum += hist[right_margin]
    
    if tmp_sum >= (interval_ind+1) * interval_sum and interval_ind != N-1:
        # add margins of a new interval
        intervals[interval_ind, 0] = left_margin
        intervals[interval_ind, 1] = right_margin
        
        real_sum[interval_ind] = tmp_sum
        interval_ind += 1
        left_margin = right_margin+1
    
# If the last interval wasn't filled, fill it with the rest of spectrum
if interval_ind == N-1: # interval_ind normally runs 0 .. N-1
    intervals[interval_ind, 0] = left_margin
    intervals[interval_ind, 1] = right_margin
    
    real_sum[interval_ind] = tmp_sum
    interval_ind += 1




# Plot the divided histogram
colors = range(0, 256) # [0..255]
plt.plot(colors, hist, 'b') # Plot histogram


x = intervals.ravel() # Flatten intervals to 1D array (as a view)
xmin, xmax, ymin, ymax = plt.axis() # limits of plot
plt.vlines(x, ymin, ymax, colors='r') # Plot margins


lbl = 'Histogram of image: ' + img_fname + \
        '\n Number of intervals:' + str(N)
plt.title(lbl)

print 'Ideal sum:', interval_sum
print 'Full sum:', full_sum
print 'Real partial sums:\n', real_sum
print 'Resulting intervals:\n', intervals
plt.show()

