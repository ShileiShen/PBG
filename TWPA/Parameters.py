"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""
import numpy

filename = '2um420Res_L3mm_4cells_11x4chip_20W_242W_120h_2gap_4all_chip.gds'
filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/2018'  # for Windows
# filepath = '/Users/mykhailo/Documents/UNSW/PBG'  #for Mac

# Parameters ##  ALL UNITS IN MICRONS

chip_length = 1300
chip_width = 3000

l_long = 6.4
t_long = 0.25

l_mid = 1.2
t_mid = 1.05

l_short = 0.6
t_short = 1.05

gap = 4  # gap between the Zlow and the ground plane
w_gnd = 300  # width of the single ground plane for CPW structure

# number of Zlow-Zhigh cascades from each side of the resonator in case of
# transimission line (NOT USED)
number = 200

# R_inner_low = 700 / 2 #radius for Round
#R_inner_high = 900 / 2
R = 30  # radius for arc, const for low and high TL
d_angle = numpy.pi / 10000  # arc builder step

spec = {'layer': 1, 'datatype': 1, 'number_of_points': 0.01}  # finese of arc
spec_arc_res = {'layer': 1, 'datatype': 1, 'number_of_points': 0.1}

# standard specifications for Path polygon
spec_path = {'layer': 1, 'datatype': 1}
spec_path_chip = {'layer': 2, 'datatype': 1}
# standard specifications for Rectangular polygon used for Resonator creation
spec_res = {'layer': 0, 'datatype': 1}
step_polygon = 0.1  # check stepper for polygon builder

edge_offset = 1250  # free space left from the top of the chip before starting resonator
# distance between the resonator and the start of meander in vertical direction
resonator_y_offset = 1200
min_side_offset = 1250  # distance from the long side of the chip
angle_error = 2 * d_angle
# -500 # last meander side offset excluding radius of the bend
last_meander_side_offset = chip_width / 2

t_final = 200  # the additional CPW for 50 Ohms match to PCB CPW-grounded
gap_final = 130
l_taper = 600  # length of the tapered element
# l_final=300 #length of the polygon after it was tapered, will be
# parametrised according to the chip length

# comment it out if not creating gnd plane
# homogenous for the gap CPW
# l_long = 6.4-0.5
# t_long = 0.25+0.5
#
# l_mid = 1.2+0.5
# t_mid = 1.05+0.5
#
# l_short = 0.6+0.4
# t_short = 1.05+0.5

