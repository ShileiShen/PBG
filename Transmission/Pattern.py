"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

import PathCreatorLibrary as p
from Parameters import *
from Position import Position
import numpy

p.filename = 'tr_2um868Res_L3mm_4cells_11x4chip_20W_242W_120h_2gap_4all_WIDE.gds'
p.filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/Transmission/2019'  # for Windows
#p.filepath = '/Users/mykhailo/OneDrive - UNSW/research/patterns/PBG/Transmission/2019' #for Mac

p.position = Position()
p.createPoly(chip_length, chip_width, spec_path=spec_path_chip)

# #draw a structure
p.position = Position(x=chip_width / 2 - l_res / 2, y=chip_length / 2 - edge_offset)

p.resonator()

def create_right_wing():
    p.first_meander_trans(total_length=l_Zhigh, width=t_Zhigh, direction='+x', step=step_polygon)

    p.position.direction = '-y'
    p.position.angle = 0

    for i in range(number):
        print('new')
        p.position.length = 0  # before building new TL, the initial length should be set to zero
        p.meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
        print('new')
        p.position.length = 0
        p.meander_draw(total_length=l_Zhigh, width=t_Zhigh, step=step_polygon)

    print('new')
    p.position.length = 0
    p.meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)

    p.createPoly(width=t_Zlow, length=l_taper, direction='-y', final_width=t_final)  # tapering at the end

    l_final = chip_length / 2 - abs(p.position.y)
    p.createPoly(width=t_final, length=l_final, direction='-y')


def create_left_wing():
    p.position.x = chip_width / 2 - l_res / 2
    p.position.y = chip_length / 2 - edge_offset
    p.first_meander_trans(total_length=l_Zhigh, width=t_Zhigh, direction='-x', step=step_polygon)

    p.position.direction = '-y'
    p.position.angle = numpy.pi

    for i in range(number):
        print('new')
        p.position.length = 0  # before building new TL, the initial length should be set to zero
        p.meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
        print('new')
        p.position.length = 0
        p.meander_draw(total_length=l_Zhigh, width=t_Zhigh, step=step_polygon)

    print('new')
    p.position.length = 0
    p.meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)

    p.createPoly(width=t_Zlow, length=l_taper, direction='-y', final_width=t_final)  # tapering at the end

    l_final = chip_length / 2 - abs(p.position.y)
    p.createPoly(width=t_final, length=l_final, direction='-y')

create_right_wing()
create_left_wing()
p.write()
