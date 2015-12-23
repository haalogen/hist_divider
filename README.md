# hist_divider
This is a script for dividing the histogram of Grayscale image into N intervals ("shades of gray"), 
by the means of integral sums of the histogram.


####Idea: 
All intervals should have approximately equal integral sums.



####Input: 
  * **img_fname** -- Image filename 
  * **N**         -- Wanted number of intervals



####Output:
  * **intervals** -- array (of pairs) of shape (N, 2); each pair: [left_margin, right_margin]
