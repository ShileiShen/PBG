"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

import PathCreatorLibrary as p
from Position import Position
from Parameters import *

p.filename = 'Refl_1um420Res_120h_2gap_4all.gds'
p.filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/Reflection/1umWideRes50nmNbTiN/Relf_1umW_420umL'  # for Windows

p.createPoly(chip_length, chip_width, spec_path=spec_path_chip)

# #draw a structure
p.position = Position(
    x=chip_width / 2 - l_res / 2, y=chip_length / 2 - edge_offset)
p.resonator()


p.first_meander_draw(total_length=l_Zhigh, width=t_Zhigh,
                   direction='+x', step=step_polygon)
p.position.change_direction()

for i in range(number):  # number of repetitions
    print('new')
    p.position.length = 0  # before building new TL, the initial length should be set to zero
    p.meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
    p.position.length = 0
    print('new')
    p.meander_draw(total_length=l_Zhigh, width=t_Zhigh, step=step_polygon)
    p.position.length = 0


#meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
p.position.length = 0
p.last_meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
p.position.length = 0


p.createPoly(width=t_Zlow, length=l_taper, direction='-y',
           final_width=t_final)  # tapering at the end
#taper(t_Zlow, t_final, l_taper, direction='-y', step=step_polygon)

l_final = chip_length / 2 - abs(p.position.y)
p.createPoly(width=t_final, length=l_final, direction='-y')

p.write()  # writing the final structure to gds file
