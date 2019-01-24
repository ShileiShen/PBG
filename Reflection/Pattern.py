"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

import PathCreatorLibrary as p
from Position import Position
from Parameters import *

p.filename = 'Refl_1um768Res_120h_2gap_4all.gds'
p.filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/Reflection'  # for Windows

p.createPoly(chip_length, chip_width, spec_path=spec_path_chip)

# #draw a structure
p.position = Position(
    x=chip_width / 2 - l_res / 2, y=chip_length / 2 - edge_offset)
p.resonator()

p.first_meander_trans(total_length=l_Zhigh, width=t_Zhigh,
                   direction='+x', step=step_polygon)



print('new')
p.position.length = 0  # before building new TL, the initial length should be set to zero
p.createPoly(width=t_Zlow, length=l_Zlow, direction='-y')
p.position.length = 0
print('new')
p.createPoly(width=t_Zhigh, length=l_Zhigh, direction='-y')
# p.position.length = 0
# p.createPoly(width=t_Zlow, length=l_Zlow, direction='-y')

p.position.length = 0

p.createPoly(width=t_Zlow, length=l_taper, direction='-y',
           final_width=t_final)  # tapering at the end
#taper(t_Zlow, t_final, l_taper, direction='-y', step=step_polygon)

l_final = chip_length / 2 - abs(p.position.y)
p.createPoly(width=t_final, length=l_final, direction='-y')

p.write()
