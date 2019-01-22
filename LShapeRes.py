"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""
import gdspy
import Position
import numpy
#import scipy.constants as scc

print('Using gdspy module version ' + gdspy.__version__)

#%%
# Parameters ##  ALL UNITS IN MICRONS

filename = 'inner_path_L2600_WIDE.gds'
filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/Reflection/Sonnet'
# filepath='/Users/mykhailo/Documents/UNSW/PBG'

chip_length = 11000
chip_width = 4000
l_res = 2600# length of lambda/2 resonator at 7.3 GHz

# t_res=20 #width of the resonator
# gap_res=10 #resonator gap for Lk=0

t_res = 20  # width of the resonator
#gap_res = 10  # resonator gap for Lk=0
gap_res = 2  # resonator gap for Lk=7.4388
# standard specifications for Path polygon
spec_path = {'layer': 1, 'datatype': 1}
spec_path_chip = {'layer': 2, 'datatype': 1}
spec = {'layer': 1, 'datatype': 1, 'number_of_points': 0.9}  # finese of arc
min_side_offset = 800
min_top_offset = 1000
c_gap = 50

t_input = 100
gap_input = 37
l_input = 1000
l_taper = 1000
width_res = t_res

gnd_end_length = 200

#Comment it out if not creating GND plane
width_res=t_res+2*gap_res
t_input = t_input + 2*gap_input


## End of parameters ##


def write():
    gdspy.write_gds(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
    print('gds file saved to "' + filepath + "/" + filename + '"')
    print('PathCreator Finished!')


def initPath(width):
    path = gdspy.Path(width, (position.x, position.y))
    return path

def createPoly(width, length, direction='+x', final_width=None, spec_path=spec_path):
    path = initPath(width)
    path.segment(length, direction, final_width=final_width, **spec_path)
    cell.add(path)
    if (direction == '+x'):
        position.move_x(length)
    elif (direction == '-x'):
        position.move_x(-length)
    elif(direction == '+y'):
        position.move_y(length)
    elif(direction == '-y'):
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
            length += numpy.pi * R / 2
        while length < total_length:
            createPoly(width, step, direction='-y')
            length += step

    if direction == '-x':
        while position.x > min_side_offset + R:
            createPoly(width, step, direction=direction)
            length += step
        if length < total_length:
            createArc(width, R, numpy.pi / 2.0, numpy.pi)
            length += numpy.pi * R / 2
        while length < total_length:
            createPoly(width, step, direction='-y')
            length += step


cell = gdspy.Cell('PathCreator')
# define chip
position=Position.Position()
createPoly(chip_length,chip_width, spec_path=spec_path_chip)

# define path
position = Position.Position()

position.move_y(chip_length / 2 - min_top_offset)
position.move_x(min_side_offset)


first_meander_draw(total_length=l_res, width=width_res,
                   step=10, direction='+x', R=450)
# createPoly(width_res, l_res,
#            direction='-y', final_width=None)

# position.move_y(-c_gap)
createPoly(width_res, chip_length / 2 + position.y - l_input - l_taper,
           direction='-y', final_width=None)

createPoly(width=width_res, length=l_taper, direction='-y', final_width=t_input)  # tapering at the end


l_final = chip_length / 2 - abs(position.y) - gnd_end_length
createPoly(width=t_input, length=l_final, direction='-y')
#position.move_y(-gap_input)
l_final = chip_length / 2 - abs(position.y)
createPoly(width=t_input, length=l_final, direction='-y')
write()
####################################################

# draw in -x direction

# define path
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
