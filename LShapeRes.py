
import gdspy
import Position
import numpy
#import scipy.constants as scc

print('Using gdspy module version ' + gdspy.__version__)

#%%
## Parameters ##  ALL UNITS IN MICRONS

filename = 'outer_path_L3910.gds'
filepath = 'C:/Users/z5119993/Dropbox/PGB/Reflection'
#filepath='/Users/mykhailo/Documents/UNSW/PBG'

chip_length=10000
chip_width=4000
l_res=3910   #length of lambda/2 resonator at 7.3 GHz
t_res=100 #width of the resonator
gap_res=75 #resonator gap for Lk=0
spec_path = {'layer': 1, 'datatype': 1} #standard specifications for Path polygon
spec = {'layer': 1, 'datatype': 1,'number_of_points': 0.9} #finese of arc
min_side_offset=800
min_top_offset=1000
c_gap=50
## End of parameters ##


def write():
	gdspy.write_gds(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
	print('gds file saved to "' + filepath + "/" + filename + '"')
	print('PathCreator Finished!')

def initPath(width):
	path = gdspy.Path(width, (position.x, position.y))
	return path

def createPoly(width, length, direction='+x', final_width=None):
	path=initPath(width)
	path.segment(length, direction, final_width=final_width, **spec_path)
	cell.add(path)
	if (direction=='+x'):
		position.move_x(length)
	elif (direction=='-x'):
		position.move_x(-length)
	elif(direction=='+y'):
		position.move_y(length)
	elif(direction=='-y'):
		position.move_y((-length))


def createArc(width, radius, angle1, angle2):
	path = initPath(width)
	path.arc(radius, angle1, angle2, **spec)
	cell.add(path)
	cx = position.x - radius * numpy.cos(angle1)
	cy = position.y - radius * numpy.sin(angle1)
	position.x = cx + radius * numpy.cos(angle2)
	position.y = cy + radius * numpy.sin(angle2)


def first_meander_draw(total_length, width, step, direction, R):
	length = 0
	if direction == '+x':
		while position.x < chip_width - min_side_offset - R:
			createPoly(width, step, direction=direction)
			length += step
		if length < total_length:
			createArc(width, -R, -numpy.pi / 2.0, -numpy.pi)
			length += numpy.pi * R/2
		while length < total_length:
			createPoly(width, step, direction='-y')
			length += step

	if direction == '-x':
		while position.x > min_side_offset + R:
			createPoly(width, step, direction=direction)
			length += step
		if length < total_length:
			createArc(width, R, numpy.pi / 2.0, numpy.pi)
			length += numpy.pi * R/2
		while length < total_length:
			createPoly(width, step, direction='-y')
			length += step

cell = gdspy.Cell('PathCreator')
#define chip
# position=Position.Position()
# createPoly(chip_length,chip_width)

#define path
position=Position.Position()

position.move_y(chip_length/2-min_top_offset)
position.move_x(min_side_offset)

width_res=t_res+2*gap_res
#width_res=t_res

first_meander_draw(total_length=l_res, width=width_res, step=10, direction='+x', R=450)
#position.move_y(-c_gap)
createPoly(width_res, chip_length/2+position.y, direction='-y', final_width=None)
write()
####################################################

#draw in -x direction

#define path
# position=Position.Position()
#
# position.move_y(chip_length/2-min_top_offset)
# position.move_x(chip_width-min_side_offset)
# width_res=t_res+2*gap_res
# #width_res=t_res
#
# first_meander_draw(total_length=l_res, width=width_res, step=10, direction='-x', R=450)
# #position.move_y(-c_gap)
# createPoly(width_res, chip_length/2+position.y, direction='-y', final_width=None)
# write()