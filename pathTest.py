# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 16:40:49 2018

@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

import gdspy
import numpy
#import scipy.constants as scc

print('Using gdspy module version ' + gdspy.__version__)

#%%
# Parameters ##  ALL UNITS IN MICRONS

filename = 'path_L1.gds'
#filepath = 'C:/A_MYKHAILO/simulations/Pattern/EBL designes/PBG/2018'
filepath = '/Users/mykhailo/Documents/UNSW/PBG'


l_res = 8100 / 2   # length of lambda/2 resonator at 7.3 GHz
t_res = 100  # width of the resonator
gap_res = 75  # resonator gap for Lk=0

## End of parameters ##
#%%
# ------------------------------------------------------------------ #
#      PATHS
# ------------------------------------------------------------------ #

path_cell = gdspy.Cell('PATHS')

# Start a path from the origin with width 1.
path1 = gdspy.Path(1, (0, 0))

# Add a straight segment to the path in layer 1, datatype 1, with length
# 3, going in the '+x' direction. Since we'll use this layer/datatype
# configuration again, we can setup a dict containing this info.
spec = {'layer': 1, 'datatype': 1}
path1.segment(3, '+x', **spec)

# Add a curve to the path by specifying its radius as 2 and its initial
# and final angles.
path1.arc(2, -numpy.pi / 2.0, numpy.pi / 6.0, **spec)

# Add another segment to the path in layer 1, with length 4 and
# pointing in the direction defined by the last piece we added above.
path1.segment(4, **spec)

# Add a curve using the turn command.  We specify the radius 2 and
# turning angle. The agnle can also be specified with 'l' and 'r' for
# left and right turns of 90 degrees, or 'll' and 'rr' for 180 degrees.
path1.turn(2, -2.0 * numpy.pi / 3.0, **spec)

# Final piece of the path.  Add a straight segment and tapper the path
# width from the original 1 to 0.5.
path1.segment(3, final_width=0.5, **spec)
path_cell.add(path1)

path_cell.add(
    gdspy.Round(
        (23.5, 7),
        15,
        inner_radius=14,
        initial_angle=-2.0 * numpy.pi / 3.0,
        final_angle=-numpy.pi / 3.0,
        layer=2))


#%%
## Generate GDS ##
## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##
# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath + "\ " + filename + '"')

## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##
# View the layout using a GUI.  Full description of the controls can
# be found in the online help at http://gdspy.sourceforge.net/
# gdspy.LayoutViewer()
print('Finished!')
