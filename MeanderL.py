"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""

from pathLibrary import PathCreatorLibrary as p

filename = 'meanderL_W3um_G5um_L300um.gds'
filepath = 'C:/Users/z5119993/OneDrive - UNSW/research/Anderson'  # for Windows
w = 3  #width of the line
l = 300 - w  #length of the complete line
l_trans = 5 + 2*w  #spacing between lines
N_line_up = 10  #half number of total vertical lines

for i in range(N_line_up):

    p.createPoly(width=w, length=l, direction='+y')
    p.position.x = p.position.x - w/2
    p.createPoly(width=w, length=l_trans, direction='+x')
    p.position.x = p.position.x - w / 2
    p.createPoly(width=w, length=l, direction='-y')
    p.position.x = p.position.x - w / 2
    p.createPoly(width=w, length=l_trans, direction='+x')
    p.position.x = p.position.x - w / 2

p.write()