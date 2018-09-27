# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:32:20 2017

@author: Mykhailo Savytskyi 
"""
#import numpy as np
import gdspy
#import scipy.constants as scc

print('Using gdspy module version ' + gdspy.__version__)

#%%
# Parameters ##  ALL UNITS IN MICRONS

filename = '118umRes_Fingers_66umGap_8150L.gds'
filepath = 'C:/A_MYKHAILO/simulations/Pattern/EBL designes/PBG/resonator'

l_Zhigh = 3650
t_Zhigh = 16

l_Zlow = 3650
t_Zlow = 204

l_res = 8150  # length of lambda/2 resonator at 7.3 GHz
t_res = 118  # width of the resonator

gap = 22  # gap between the Zlow and the ground plane
w_gnd = 500  # width of the single ground plane for CPW structure

number = 5  # number of Zlow-Zhigh cascades from each side of the resonator

w_c = 4  # C finger width
h_c = 0  # C finger height
w_sep = 4  # C finger separation
h_sep = 66  # C finger vertical distance from ground plane fingers to resonator
delta_x = 0  # offset for starting point of C fingers


c_gap = 2
c_length = 50
## End of parameters ##

#%% creation of basic PBG structure with lambda/2 resonator

cell = gdspy.Cell('PGB')

k = 0
for i in range(number):

    Zlow1 = gdspy.Rectangle((0 + k * (l_Zlow + l_Zhigh), 0),
                            (l_Zlow + k * (l_Zlow + l_Zhigh), t_Zlow))

    Zhigh1 = gdspy.Rectangle((l_Zlow + k * (l_Zlow + l_Zhigh), (t_Zlow - t_Zhigh) / 2.),
                             (l_Zlow + l_Zhigh + k * (l_Zlow + l_Zhigh), (t_Zlow - t_Zhigh) / 2. + t_Zhigh))
#    cell.add(Zlow1)
#    cell.add(Zhigh1)
    k = k + 1

res = gdspy.Rectangle((k * (l_Zlow + l_Zhigh), (t_Zlow - t_res) / 2.),
                      (k * (l_Zlow + l_Zhigh) + l_res, (t_Zlow - t_res) / 2. + t_res))
cell.add(res)


c_left = gdspy.Rectangle((k * (l_Zlow + l_Zhigh) - c_gap - c_length, (t_Zlow - t_res) / 2.),
                         (k * (l_Zlow + l_Zhigh) - c_gap, (t_Zlow - t_res) / 2. + t_res))
cell.add(c_left)

c_right = gdspy.Rectangle((k * (l_Zlow + l_Zhigh) + l_res + c_gap, (t_Zlow - t_res) / 2.),
                          (k * (l_Zlow + l_Zhigh) + l_res + c_gap + c_length, (t_Zlow - t_res) / 2. + t_res))
cell.add(c_right)

offset_X1 = k * (l_Zlow + l_Zhigh) + l_res
k = 0
for i in range(number):

    Zlow2 = gdspy.Rectangle((offset_X1 + l_Zhigh + k * (l_Zlow + l_Zhigh), 0),
                            (offset_X1 + l_Zlow + l_Zhigh + k * (l_Zlow + l_Zhigh), t_Zlow))

    Zhigh2 = gdspy.Rectangle((offset_X1 + k * (l_Zlow + l_Zhigh), (t_Zlow - t_Zhigh) / 2.),
                             (offset_X1 + l_Zhigh + k * (l_Zlow + l_Zhigh), (t_Zlow - t_Zhigh) / 2. + t_Zhigh))
#    cell.add(Zlow2)
#    cell.add(Zhigh2)
    k = k + 1

offset_X2 = offset_X1 - l_res

#gnd_upper=gdspy.Rectangle( (0 ,t_Zlow+gap), (offset_X1+offset_X2 , t_Zlow+gap+w_gnd) )
#gnd_bottom=gdspy.Rectangle( (0 ,-gap), (offset_X1+offset_X2 ,-gap-w_gnd) )


gnd_upper = gdspy.Rectangle((k * (l_Zlow + l_Zhigh), t_Zlow + gap),
                            (k * (l_Zlow + l_Zhigh) + l_res, t_Zlow + gap + w_gnd))
gnd_bottom = gdspy.Rectangle(
    (k * (l_Zlow + l_Zhigh), -gap), (k * (l_Zlow + l_Zhigh) + l_res, -gap - w_gnd))

# cell.add(gnd_bottom)
# cell.add(gnd_upper)

print("total length of the structure: %2.1f and width: %2.1f" %
      (offset_X1 + offset_X2, 2 * w_gnd + 2 * gap + t_Zlow))


#%% Adding C fingers to the resonator
#
x_init = k * (l_Zlow + l_Zhigh)  # x coordinate where the resonator starts
y_init = t_Zlow / 2 + t_res / 2  # upper y coordinate of the resonator
#
#
x_start = x_init + delta_x  # start of C fingers on the resonator


def addCfinger(x0, y0, positive):
    if positive:
        cFinger = gdspy.Rectangle((x0, y0), (x0 + w_c, y0 + h_c))
    else:
        cFinger = gdspy.Rectangle((x0, y0), (x0 + w_c, y0 - h_c))
    cell.add(cFinger)


x_step = 2 * w_c + 2 * w_sep
# number of C fingers in one raw from one side only
number_of_fingers = (l_res - 2 * delta_x + x_step) // (x_step)

for j in range(number_of_fingers):
    addCfinger(x_start + j * x_step, y_init, 1)
    addCfinger(x_start + j * x_step, y_init - t_res, 0)


#%%additional ground planes for resonator
gndRes_h = gap + t_Zlow / 2 - t_res / 2 - \
    h_sep - h_c  # width of additional ground plane

gndRes_upper = gdspy.Rectangle((x_start - c_gap - c_length, t_Zlow + gap),
                               (x_start + l_res - 2 * delta_x + w_c + c_gap + c_length, t_Zlow + gap - gndRes_h))
gndRes_bottom = gdspy.Rectangle((x_start - c_gap - c_length, -gap),
                                (x_start + l_res - 2 * delta_x + w_c + c_gap + c_length, -gap + gndRes_h))
cell.add(gndRes_bottom)
cell.add(gndRes_upper)

#%%C fingers from additional ground planes

y_start_up = t_Zlow + gap - gndRes_h
y_start_down = -gap + gndRes_h


for i in range(number_of_fingers - 1):

    """ fingers connected to ground planes """

    x_var1 = x_start + (i + 1) * (x_step) - w_sep - w_c
    y_var1 = y_start_down

    x_var2 = x_var1 + w_c
    y_var2 = y_var1 + h_c

    #down_finger = CreatePath([(x_var1,y_var1),(x_var2,y_var2)],w_c,layer=0)
    down_finger = gdspy.Rectangle((x_var1, y_var1), (x_var2, y_var2))

    y_var1_up = y_start_up
    y_var2_up = y_var1_up - h_c

    #up_finger = CreatePath([(x_var1,y_var1_up),(x_var2,y_var2_up)],w_c,layer=0)
    up_finger = gdspy.Rectangle((x_var1, y_var1_up), (x_var2, y_var2_up))

    cell.add(down_finger)
    cell.add(up_finger)


#%%
""" Adding ground plane transition structure """


#lowLeftGND = gdspy.PolyPath([(x_init, -gap), (x_start, -gap)],[0,2*gndRes_h], layer=0, max_points=199)

pointsLowLeft = [(x_init, -gap), (x_start, -gap), (x_start, -gap + gndRes_h)]
pointsLowRight = [(x_start + l_res - 2 * delta_x + w_c, -gap), (x_start + l_res - 2 *
                                                                delta_x + w_c, -gap + gndRes_h), (x_start + l_res - 2 * delta_x + delta_x, -gap)]
pointsTopLeft = [(x_init, t_Zlow + gap), (x_start, t_Zlow +
                                          gap), (x_start, t_Zlow + gap - gndRes_h)]
pointsTopRight = [(x_start + l_res - 2 * delta_x + w_c, t_Zlow + gap), (x_start + l_res - 2 *
                                                                        delta_x + delta_x, t_Zlow + gap), (x_start + l_res - 2 * delta_x + w_c, t_Zlow + gap - gndRes_h)]

lowLeftGND = gdspy.Polygon(pointsLowLeft, 0)
lowRightGND = gdspy.Polygon(pointsLowRight, 0)
topLeftGND = gdspy.Polygon(pointsTopLeft, 0)
topRightGND = gdspy.Polygon(pointsTopRight, 0)

# cell.add(lowLeftGND)
# cell.add(lowRightGND)
# cell.add(topLeftGND)
# cell.add(topRightGND)


#%%
## Generate GDS ##
## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##
# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(filepath + '\ ' + filename, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath + '\ ' + filename + '"')

## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##
# View the layout using a GUI.  Full description of the controls can
# be found in the online help at http://gdspy.sourceforge.net/
gdspy.LayoutViewer()
print('Finished!')
