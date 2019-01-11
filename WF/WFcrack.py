"""
@author: Mykhailo Savytskyi
@date: 22/11/2018
@email: m.savytskyi@unsw.edu.au
"""

import gdspy
import Position

print('Using gdspy module version ' + gdspy.__version__)

#%%
# Parameters ##  ALL UNITS IN MICRONS

filename = 'WF200_crack_horiz.gds'
filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/WF_crack'
# filepath='/Users/mykhailo/Documents/UNSW/PBG'

chip_length = 11000
chip_width = 4000
WF = 200
crack_width = 5  # len
spec_path = {'layer': 1, 'datatype': 1}


def write():
    gdspy.write_gds(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
    print('gds file saved to "' + filepath + "/" + filename + '"')
    print('PathCreator Finished!')


def initPath(position, width):
    path = gdspy.Path(width, (position.x, position.y))
    return path


def createPoly(position, width, length, direction='+x', final_width=None, spec_path=spec_path):
    path = initPath(position, width)
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


def draw_vert():
	N = int(chip_width/WF)
	for i in range(N-1):
		position = Position.Position(x=WF + i * WF, y=-chip_length / 2)
		createPoly(position, width=crack_width, length=chip_length, direction='+y')


def draw_horiz():
	N = int(chip_length / WF)
	for i in range(N - 1):
		position = Position.Position(y=-chip_length / 2 + WF + i * WF, x=0)
		createPoly(position, width=crack_width, length=chip_width, direction='+x')
## Constracting the actual design by using function defined above

cell = gdspy.Cell('WF')
#define chip
position = Position.Position()
createPoly(position=position, width=chip_length, length=chip_width, spec_path={'layer': 0, 'datatype': 1})

# #draw a structure
#draw_vert()
draw_horiz()
write()