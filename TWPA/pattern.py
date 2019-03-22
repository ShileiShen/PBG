"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

import pathLibrary.PathCreatorLibrary as p
from pathLibrary.Position import Position
from Parameters import *

p.filename = 'test2.gds'
p.filepath = 'C:/Users/HybridQ/Documents/Python/TWPA'  # for Windows

p.createPoly(chip_length, chip_width, spec_path=spec_path_chip)

# for GND
# p.position = Position(
#     x=chip_width / 2+0.25, y=chip_length / 2 - edge_offset)

#draw a structure
p.position = Position(
    x=chip_width / 2, y=chip_length / 2 - edge_offset)

p.position.length = 0  # before building new TL, the initial length should be set to zero

for i in range(number):  # number of repetitions
    for j in range(2):
        print('new1')
        p.meander_draw(total_length=l_long, width=t_long, step=step_polygon)
        p.position.length = 0

        print('new2')
        p.meander_draw(total_length=l_mid, width=t_mid, step=step_polygon)
        p.position.length = 0

    print('new1')
    p.meander_draw(total_length=l_long, width=t_long, step=step_polygon)
    p.position.length = 0

    print('new3')
    p.meander_draw(total_length=l_short, width=t_short, step=step_polygon)
    p.position.length = 0



p.write()  # writing the final structure to gds file
