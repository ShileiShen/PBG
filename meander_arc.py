# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 09:59:20 2018

@author: z5119993
"""

import gdspy
import Position
import numpy
#import scipy.constants as scc

print('Using gdspy module version ' + gdspy.__version__)

#%% 
## Parameters ##  ALL UNITS IN MICRONS

filename = 'path_Test.gds'
filepath = 'C:/A_MYKHAILO/simulations/Pattern/EBL designes/PBG/2018'

l_Zhigh=3000
t_Zhigh=10

l_Zlow=3000
t_Zlow=242

l_res=788   #length of lambda/2 resonator at 7.3 GHz
t_res=2 #width of the resonator

gap=4 #gap between the Zlow and the ground plane
w_gnd=300  #width of the single ground plane for CPW structure

number=4 #number of Zlow-Zhigh cascades from each side of the resonator

w_c=4 #C finger width
h_c=100 #C finger height
w_sep=4 #C finger separation
h_sep=2 #C finger vertical distance from ground plane fingers to resonator
delta_x=0 #offset for starting point of C fingers


c_gap=0
c_length=0
## End of parameters ##

#%%
path_cell = gdspy.Cell('PATHS')

# Start a path from the origin with width 1.
path1 = gdspy.Path(t_Zlow, (0, 0))

R_inner=700/2
R=R_inner + t_Zlow
l_residual=l_Zlow- numpy.pi*(R_inner+R)/2

# Add a straight segment to the path in layer 1, datatype 1, with length
# 3, going in the '+x' direction. Since we'll use this layer/datatype
# configuration again, we can setup a dict containing this info.
spec = {'layer': 1, 'datatype': 1}
path1.segment(l_residual, '+x', **spec)

initial_angle =-2.5*numpy.pi
final_angle=-1.5*numpy.pi


# Add a curve to the path by specifying its radius as 2 and its initial
# and final angles.
path1.arc(R_inner, initial_angle, final_angle, number_of_points=0.5, **spec)


# Add a curve using the turn command.  We specify the radius 2 and
# turning angle. The agnle can also be specified with 'l' and 'r' for
# left and right turns of 90 degrees, or 'll' and 'rr' for 180 degrees.
#path1.turn(R_inner, -2.0 * numpy.pi / 3.0, number_of_points=0.1, **spec)

path_cell.add(path1)


#%% 
## Generate GDS ##
## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##
## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(filepath + "\\" + filename, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath +"\ " + filename + '"')

## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##
## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer()
print('Finished!')