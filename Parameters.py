import numpy

filename = '2umRes_L3mm_4cells_MEANDER0.gds'
filepath = 'C:/Users/z5119993/A_MYKHAILO/simulations/Pattern/EBL designes/PBG/Reflection'  #for Windows
#filepath = '/Users/mykhailo/Documents/UNSW/PBG'  #for Mac
#Parameters ##  ALL UNITS IN MICRONS

chip_length = 10000
chip_width = 4000

edge_offset=1000

l_Zhigh = 3000
t_Zhigh = 20

l_Zlow = 3000
t_Zlow = 242

l_res = 788/2  #length of lambda/2 resonator at 7.3 GHz
t_res = 2  #width of the resonator

gap = 4  #gap between the Zlow and the ground plane
w_gnd = 300  #width of the single ground plane for CPW structure

number = 4  #number of Zlow-Zhigh cascades from each side of the resonator in case of transimission line

w_c = 4  #C finger width
h_c = 100  #C finger height
w_sep = 4  #C finger separation
h_sep = 2  #C finger vertical distance from ground plane fingers to resonator
delta_x = 0  #offset for starting point of C fingers

R_inner_low = 700 / 2 #radius for Round
R_inner_high = 900 / 2
R = 800/2 #radius for arc, const for low and high TL
l1 = 800
l1_Zlow=800+600
l2 = 500
l3=l_Zhigh-numpy.pi*R -l1 -l2
l2_Zlow=l_Zlow-numpy.pi*R-l1_Zlow

c_gap = 0 #coupling capacitor separation
c_length = 0 #length of the polygon that has coupling capacitor

spec = {'number_of_points': 0.5} #finese of arc

spec_path = {'layer': 1, 'datatype': 1} #standard specifications for Path polygon

