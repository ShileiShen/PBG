# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 19:15:12 2018

@author: Mykhailo Savytskyi 
"""
import gdspy
import Position
import numpy
import PGB_v3_meander as pgb
#%% 
## Parameters ##  ALL UNITS IN MICRONS

filename1 ='/PBG_large.gds'
filename2 ='/GND.gds'
filename ='/PBG_GND.gds'
filepath = 'C:/A_MYKHAILO/simulations/Pattern/EBL designes/PBG/PGB_meander/L3000um_8cells_788L_20W_27Ohms'

l_Zhigh=3000
t_Zhigh=250

l_Zlow=3000
t_Zlow=250

l_res=788   #length of lambda/2 resonator at 7.3 GHz
t_res=2+2*123 #width of the resonator

gap_Zlow=4 #gap between the Zlow and the ground plane
gap_Zhigh=115 #gap between the Zhigh and the ground plane
#w_gnd=300  #width of the single ground plane for CPW structure

#w_c=4 #C finger width
#h_c=50 #C finger height
#w_sep=4 #C finger separation
#h_sep=2 #C finger vertical distance from ground plane fingers to resonator
#delta_x=0 #offset for starting point of C fingers
#
#c_gap=0
#c_length=0
## End of parameters ##
spec = {'number_of_points': 0.5}

def resonator(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    res=gdspy.Rectangle( ( position.x, position.y+0.5*(t_Zlow-t_res)), ( position.x + l_res, position.y+0.5*(t_Zlow-t_res) + t_res ) )
    cell.add(res)
    position.x=position.x+l_res
    return cell
    
#%%    
def bendLeftZlow(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=700/2-gap_Zlow
    R=R_inner + t_Zlow
    l_residual=l_Zlow- numpy.pi*(R_inner+R)/2
   

 
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    
    l_residual=l_Zlow- numpy.pi*(R_inner+R)/2
    
    position.y=center_y-R
    position.x=center_x
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    
    position.x=position.x+l_residual    
    return cell
    
#%%    
def bendLeftZhigh(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2-gap_Zhigh
    R=R_inner + t_Zhigh
    l_residual=l_Zlow- numpy.pi*(R_inner+R)/2

    position.y=position.y +0.5*(t_Zlow-t_Zhigh)
 
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    
    l_residual=l_Zhigh- numpy.pi*(R_inner+R)/2
    
    position.y=center_y-R
    position.x=center_x
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.x=position.x+l_residual  
    position.y=position.y -0.5*(t_Zlow-t_Zhigh)
    return cell
    
#%%
def bendLeftZhigh2(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2-gap_Zhigh
    R=R_inner + t_Zhigh
    l_residual=l_Zhigh- numpy.pi*(R_inner+R)/2
    
    position.y=position.y +0.5*(t_Zlow-t_Zhigh)   

    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l_residual, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.x=position.x-l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y-R-0.5*(t_Zlow-t_Zhigh)
    
    return cell

#%%
def bendLeftZhighEqual(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2-gap_Zhigh
    R=R_inner + t_Zhigh
    l_residual=0.5*(l_Zhigh- numpy.pi*(R_inner+R)/2)
    
    position.y=position.y +0.5*(t_Zlow-t_Zhigh)   

    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l_residual, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.x=position.x-l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y-R
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.y= center_y-R-0.5*(t_Zlow-t_Zhigh)
    position.x=position.x+l_residual
    return cell

#%%
def bendLeftZlowEqual(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=700/2-gap_Zlow
    R=R_inner + t_Zlow
    l_residual=0.5*(l_Zlow- numpy.pi*(R_inner+R)/2)
      
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    
    position.x=position.x-l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y-R
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    
    position.y= center_y-R
    position.x=position.x+l_residual
    return cell

    
#%%
def bendRightZhighEqual(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2-gap_Zhigh
    R=R_inner + t_Zhigh
    l_residual=0.5*(l_Zhigh- numpy.pi*(R_inner+R)/2)
    
    position.y=position.y +0.5*(t_Zlow-t_Zhigh)   

    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.x=position.x+l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-2.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y-R
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l_residual, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.y= center_y-R-0.5*(t_Zlow-t_Zhigh)
    position.x=position.x-l_residual
    return cell    
    
#%%
def bendRightZlowEqual(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=700/2-gap_Zlow
    R=R_inner + t_Zlow
    l_residual=0.5*(l_Zlow - numpy.pi*(R_inner+R)/2)
     
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    
    position.x=position.x+l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-2.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y-R
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    
    position.y= center_y-R
    position.x=position.x-l_residual
    return cell    
#%%
def bendLeftZlow2(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=700/2-gap_Zlow
    R=R_inner + t_Zlow
    l_residual=l_Zlow- numpy.pi*(R_inner+R)/2

    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    
    position.x=position.x-l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y-R
    return cell
#%%    
def bendRightZhigh(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2-gap_Zhigh
    R=R_inner + t_Zhigh
    position.y=position.y +0.5*(t_Zlow-t_Zhigh)

    center_y=position.y-R_inner
    center_x=position.x
    
    Zhigh1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-2.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zhigh1)
    
    
    l_residual=l_Zhigh- numpy.pi*(R_inner+R)/2
    
    position.y=center_y-R
    position.x=center_x-l_residual
    
    Zhigh2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zhigh) )
    cell.add(Zhigh2)
    
    position.y=position.y- 0.5*(t_Zlow-t_Zhigh)   
    return cell    
    
#%%
def bendRightZhighRes(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2 -gap_Zhigh
    R=R_inner + t_Zhigh
    l1=0
    l2=350
    l_residual=(l_Zhigh- numpy.pi*(R_inner+R)/2)-l1-l2
    
    position.y=position.y +0.5*(t_Zlow-t_Zhigh)   

    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l1, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.x=position.x+l1
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-1.5*numpy.pi,
        final_angle=-2.0*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y
    position.x=position.x+R_inner
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+t_Zhigh, position.y-l_residual) )
    cell.add(Zlow2)
    
    position.y= position.y-l_residual
    
    
    
    center_y=position.y
    center_x=position.x-R_inner
    
    Zlow3=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-2.0*numpy.pi,
        final_angle=-2.5*numpy.pi,
        **spec)
    cell.add(Zlow3)
    
    position.y= center_y-R
    position.x=center_x
    
    Zlow4 = gdspy.Rectangle( (position.x, position.y),   (position.x-l2, position.y+t_Zhigh) )
    cell.add(Zlow4)
    
    position.y= center_y-R-0.5*(t_Zlow-t_Zhigh)
    position.x=position.x-l2
    
    position.x=position.x-l_res
    
    return cell    

    
    
#%%
def bendLeftZhighRes(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=900/2 -gap_Zhigh
    R=R_inner + t_Zhigh
    l1=350
    l2=0
    l_residual=(l_Zhigh- numpy.pi*(R_inner+R)/2)-l1-l2
    
    position.y=position.y +0.5*(t_Zlow-t_Zhigh)   
    position.x=position.x-l_res
    
    
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x-l1, position.y+t_Zhigh) )
    cell.add(Zlow2)
    
    position.x=position.x-l1
    
    center_y=position.y-R_inner
    center_x=position.x
    
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-1.0*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
    
    position.y= center_y
    position.x=position.x-R
    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+t_Zhigh, position.y-l_residual) )
    cell.add(Zlow2)
    
    position.y= position.y-l_residual
    
    
    center_y=position.y
    center_x=position.x+R
    
    Zlow3=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-0.5*numpy.pi,
        final_angle=-1.0*numpy.pi,
        **spec)
    cell.add(Zlow3)
    
    position.y= center_y-R
    position.x=center_x
    
    Zlow4 = gdspy.Rectangle( (position.x, position.y),   (position.x+l2, position.y+t_Zhigh) )
    cell.add(Zlow4)
    
    position.y= center_y-R-0.5*(t_Zlow-t_Zhigh)
    position.x=position.x+l2
    
    
    
    return cell   
    
#%%  
def bendRightZlow2(position,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
    R_inner=700/2-gap_Zlow
    R=R_inner + t_Zlow
    l_residual=l_Zlow- numpy.pi*(R_inner+R)/2

    Zlow2 = gdspy.Rectangle( (position.x, position.y),   (position.x+l_residual, position.y+t_Zlow) )
    cell.add(Zlow2)
    position.x=position.x+l_residual
    
    center_y=position.y-R_inner
    center_x=position.x
       
    Zlow1=gdspy.Round(
        (center_x, center_y),
        R,
        inner_radius=R_inner,
        initial_angle=-2.5*numpy.pi,
        final_angle=-1.5*numpy.pi,
        **spec)
    cell.add(Zlow1)
         
    position.y=center_y-R
    return cell

#%%

cell=gdspy.Cell('PGB_frame')
cursor= Position.Position()


#cell.add(pgb.Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell.add(pgb.Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell.add(pgb.Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))    
#cell=bendRightZhigh(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#cell.add(pgb.ZlowBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell.add(pgb.ZhighBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell=bendLeftZlowEqual(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#cell.add(pgb.Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell=resonator(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#cell.add(pgb.Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell=bendRightZlowEqual(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#cell.add(pgb.ZhighBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell.add(pgb.ZlowBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell=bendLeftZhigh2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#cell.add(pgb.Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell.add(pgb.Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#cell.add(pgb.Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))


#%% Meander 2

cell.add(pgb.Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
cell=bendRightZhigh(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendLeftZlow(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)   
cell=bendRightZhigh(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendLeftZlow(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
cell=bendRightZhigh(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendLeftZlow(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
cell=bendRightZhighRes(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=resonator(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendLeftZhighRes(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
cell=bendRightZlow2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendLeftZhigh2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendRightZlow2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
cell=bendLeftZhigh2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell=bendRightZlow2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
cell=bendLeftZhigh2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
cell.add(pgb.Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))

gdspy.gds_print(filepath + filename1, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath + filename1 + '"')
#gdspy.LayoutViewer()   
print('Larger Cell Finished!') 
#%%
cell_gnd=gdspy.Cell('GND')

gnd=gdspy.Rectangle( ( 0,500) , ( 4305, -15750 ) )
cell_gnd.add(gnd)

gdspy.gds_print(filepath  + filename2, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath + filename2 + '"')
#gdspy.LayoutViewer()   

#%% Substraction

print(len(cell.elements))

for i in range(len(cell.elements)):
    cell_gnd.add(gdspy.fast_boolean(cell_gnd.elements[i], cell.elements[i], 'not'))

cell_final=gdspy.Cell('GND_frame')
cell_final.add(cell_gnd.elements[len(cell_gnd.elements)-1])
#%% 
## Generate GDS ##
## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##
## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(filepath +  filename, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath + filename + '"')

## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##
## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer()
print('GND Finished!')