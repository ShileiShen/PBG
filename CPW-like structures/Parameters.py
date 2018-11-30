import numpy

filename = '2um420Res_L3mm_4cells_11x4chip_20W_242W_120h_2gap_4all_chip.gds'
filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/2018/IDC_50Ohms'  # for Windows
# filepath = '/Users/mykhailo/Documents/UNSW/PBG'  #for Mac

# Parameters ##  ALL UNITS IN MICRONS

chip_length = 11000
chip_width = 4000

l_Zhigh = 3000
t_Zhigh = 20

l_Zlow = 3000
t_Zlow = 242

l_res = 420  # length of lambda/2 resonator at 7.3 GHz
t_res = 2  # width of the resonator
res_R = 100  # arc radius for resonator without IDC
gap_res = 2  # gap for CPW resonator

gap = 4  # gap between the Zlow and the ground plane
w_gnd = 300  # width of the single ground plane for CPW structure

# number of Zlow-Zhigh cascades from each side of the resonator in case of
# transimission line (NOT USED)
number = 3

w_c = 4  # C finger width
h_c = 120  # C finger height
w_sep = 4  # C finger separation
h_sep = 2  # C finger vertical distance from ground plane fingers to resonator
delta_x = 0  # offset for starting point of C fingers

# R_inner_low = 700 / 2 #radius for Round
#R_inner_high = 900 / 2
R = 450  # radius for arc, const for low and high TL
d_angle = numpy.pi / 1000  # arc builder step

c_gap = 0  # coupling capacitor separation
c_length = 0  # length of the polygon that has coupling capacitor

spec = {'layer': 1, 'datatype': 1, 'number_of_points': 0.9}  # finese of arc
spec_arc_res = {'layer': 1, 'datatype': 1, 'number_of_points': 0.1}

# standard specifications for Path polygon
spec_path = {'layer': 1, 'datatype': 1}
spec_path_chip = {'layer': 2, 'datatype': 1}
# standard specifications for Rectangular polygon used for Resonator creation
spec_res = {'layer': 0, 'datatype': 1}
step_polygon = 5  # check stepper for polygon builder

edge_offset = 1000  # free space left from the top of the chip before starting resonator
# distance between the resonator and the start of meander in vertical direction
resonator_y_offset = 1200
min_side_offset = 700  # distance from the long side of the chip
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
# t_homogeneous = 250
# t_final = t_final + 2 * gap_final
# t_Zlow = t_homogeneous
# t_Zhigh = t_homogeneous
# t_res = t_res + 2*gap_res + 2*h_sep + 2*h_c
