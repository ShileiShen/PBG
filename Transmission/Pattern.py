"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

from pathLibrary import PathCreatorLibrary as p
from Transmission.Parameters import *
from pathLibrary.Position import Position

p.filename = 'tr_2um788Res_L3mm_4cells_11x4chip_20W_242W_120h_2gap_4all.gds'
p.filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/patterns/PBG/Transmission/2019'  # for Windows
#p.filepath = '/Users/mykhailo/OneDrive - UNSW/research/patterns/PBG/Transmission/2019' #for Mac
#p.position = Position()
p.createPoly(chip_length, chip_width, spec_path=spec_path_chip)

# #draw a structure
p.position = Position(
    x=chip_width / 2 - l_res / 2, y=chip_length / 2 - edge_offset)
print(l_res)
p.resonator()

p.first_meander_trans(total_length=l_Zhigh, width=t_Zhigh,
                   direction='+x', step=step_polygon)

print(p.position)


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


p.createPoly(width=t_Zlow, length=l_taper, direction='+x',
           final_width=t_final)  # tapering at the end
#taper(t_Zlow, t_final, l_taper, direction='-y', step=step_polygon)

l_final = chip_length / 2 - abs(p.position.y)


p.write()
