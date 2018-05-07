"""
@author: Mykhailo Savytskyi
"""
import gdspy
import Position
import numpy
from Parameters import *

print('Using gdspy module version ' + gdspy.__version__)

def write():
	gdspy.write_gds(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
	print('gds file saved to "' + filepath + "/" + filename + '"')
	print('PathCreator Finished!')
	

def initPath(width):
	path = gdspy.Path(width, (position.x, position.y))
	return path

def createPoly(width, length, direction='+x'):
	path=initPath(width)
	path.segment(length, direction, **spec_path)
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
	if abs(angle2-angle1)==numpy.pi:
		if (angle1<0):
			if (angle2 < angle1):
				position.move_y(-2 * abs(radius))
			if (angle2 > angle1):
				position.move_y(2 * abs(radius))
		else:
			position.move_y(-2 * abs(radius))
	if abs(angle2 - angle1) == numpy.pi/2:
		#position.move_x(abs(radius))
		if (angle2<angle1):
			position.move_y(-abs(radius))
			if (angle1<0):
				position.move_x(abs(radius))
			else:
				position.move_x(-abs(radius))
		if (angle2>angle1):
			position.move_y(abs(radius))
			position.move_x(abs(radius))


def resonator():
	createPoly(t_res,l_res)
	##%% Adding C fingers to the resonator
	position.move_x(-l_res)

	x_init = position.x  # x coordinate where the resonator starts
	y_init = position.y + 0.5*t_res  # upper y coordinate of the resonator

	x_start = x_init + delta_x  # start of C fingers on the resonator

	def addCfinger(x0, y0, positive):
		if positive:
			cFinger = gdspy.Rectangle((x0, y0), (x0 + w_c, y0 + h_c))
		else:
			cFinger = gdspy.Rectangle((x0, y0), (x0 + w_c, y0 - h_c))
		cell.add(cFinger)

	x_step = 2 * w_c + 2 * w_sep
	number_of_fingers = (l_res - 2 * delta_x + x_step) // (x_step)  # number of C fingers in one raw from one side only

	for j in range(round(number_of_fingers)):
		addCfinger(x_start + j * x_step, y_init, 1)
		addCfinger(x_start + j * x_step, y_init - t_res, 0)

	##%%additional ground planes for resonator
	gndRes_h = gap + t_Zlow / 2 - t_res / 2 - h_sep - h_c  # width of additional ground plane

	gndRes_upper = gdspy.Rectangle((position.x, position.y + t_Zlow/2 + gap),
	                               (position.x + l_res, position.y + t_Zlow/2 + gap - gndRes_h))
	gndRes_bottom = gdspy.Rectangle((position.x, position.y - t_Zlow/2-gap), (position.x + l_res, position.y - t_Zlow/2-gap + gndRes_h))
	cell.add(gndRes_bottom)
	cell.add(gndRes_upper)

	##%%C fingers from additional ground planes
	y_start_up = position.y + t_Zlow/2 + gap - gndRes_h
	y_start_down = position.y - t_Zlow/2-gap + gndRes_h

	# fingers connected to ground planes
	for i in range(round(number_of_fingers) - 1):
		x_var1 = x_start + (i + 1) * (x_step) - w_sep - w_c
		y_var1 = y_start_down

		x_var2 = x_var1 + w_c
		y_var2 = y_var1 + h_c

		# down_finger = CreatePath([(x_var1,y_var1),(x_var2,y_var2)],w_c,layer=0)
		down_finger = gdspy.Rectangle((x_var1, y_var1), (x_var2, y_var2))

		y_var1_up = y_start_up
		y_var2_up = y_var1_up - h_c

		# up_finger = CreatePath([(x_var1,y_var1_up),(x_var2,y_var2_up)],w_c,layer=0)
		up_finger = gdspy.Rectangle((x_var1, y_var1_up), (x_var2, y_var2_up))

		cell.add(down_finger)
		cell.add(up_finger)

	position.x = position.move_x(l_res)

	return cell

#define chip
position=Position.Position()
cell = gdspy.Cell('PathCreator')
createPoly(chip_length,chip_width)

position=Position.Position(x=chip_width/2-l_res/2, y=chip_length/2-edge_offset)

resonator()

createPoly(t_Zhigh,l1)
createArc(t_Zhigh, -R, -numpy.pi / 2.0, -numpy.pi)
createPoly(t_Zhigh,l2, direction='-y')
createArc(t_Zhigh, R, 0*numpy.pi/2.0, -numpy.pi/2)
createPoly(t_Zhigh, l3, direction='-x')

createPoly(t_Zlow, l1_Zlow, direction='-x')
createArc(t_Zlow, R, numpy.pi/2.0, 3*numpy.pi/2)
createPoly(t_Zlow, l2_Zlow, direction='+x')

createPoly(t_Zhigh, -(l2_Zlow-l1_Zlow)+l3, direction='+x')
createArc(t_Zhigh, -R, -numpy.pi / 2.0, -3*numpy.pi/2)
createPoly(t_Zhigh, -(-(l2_Zlow-l1_Zlow)+l3) - numpy.pi*R+l_Zhigh, direction='-x')
print(-(l2_Zlow-l1_Zlow)+l3)
write()
