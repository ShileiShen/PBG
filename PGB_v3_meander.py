# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:26:07 2018

@author: Mykhailo Savytskyi 
"""
import gdspy
import Position
import numpy
from Parameters import *

print('Using gdspy module version ' + gdspy.__version__)

# %% function that adds Z low block
def Zlow(position, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
	Zlow1 = gdspy.Rectangle((position.x, position.y), (position.x + l_Zlow, position.y + t_Zlow))

	return Zlow1


# %%
def Zhigh(position, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)
	Zhigh = gdspy.Rectangle((position.x, position.y), (position.x + l_Zhigh, position.y + t_Zhigh))
	position.x = position.x + l_Zhigh
	position.y = position.y - 0.5 * (t_Zlow - t_Zhigh)
	return Zhigh


# %%
def bendRightZlow(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=700/2
	R = R_inner + t_Zlow

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	l_residual = l_Zlow - numpy.pi * (R_inner + R) / 2

	position.y = center_y - R
	position.x = center_x - l_residual

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	return cell


# %%
def bendRightZhigh(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	center_y = position.y - R_inner
	center_x = position.x

	Zhigh1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zhigh1)

	l_residual = l_Zhigh - numpy.pi * (R_inner + R) / 2

	position.y = center_y - R
	position.x = center_x - l_residual

	Zhigh2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zhigh))
	cell.add(Zhigh2)

	position.y = position.y - 0.5 * (t_Zlow - t_Zhigh)
	return cell


# %%
def bendRightZlow2(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=700/2
	R = R_inner + t_Zlow
	l_residual = l_Zlow - numpy.pi * (R_inner + R) / 2

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zlow))
	cell.add(Zlow2)
	position.x = position.x + l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R
	return cell


# %%
def ZhighBack(position, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x - l_Zhigh

	Zhigh = gdspy.Rectangle((position.x, position.y), (position.x + l_Zhigh, position.y + t_Zhigh))
	position.y = position.y - 0.5 * (t_Zlow - t_Zhigh)
	return Zhigh


# %%
def ZlowBack(position, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
	position.x = position.x - l_Zlow
	Zlow = gdspy.Rectangle((position.x, position.y), (position.x + l_Zlow, position.y + t_Zlow))
	return Zlow


# %%
def bendLeftZlow(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=700/2
	R = R_inner + t_Zlow
	l_residual = l_Zlow - numpy.pi * (R_inner + R) / 2

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	l_residual = l_Zlow - numpy.pi * (R_inner + R) / 2

	position.y = center_y - R
	position.x = center_x

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	position.x = position.x + l_residual
	return cell


# %%
def bendLeftZhigh(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l_residual = l_Zlow - numpy.pi * (R_inner + R) / 2

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	l_residual = l_Zhigh - numpy.pi * (R_inner + R) / 2

	position.y = center_y - R
	position.x = center_x

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x + l_residual
	position.y = position.y - 0.5 * (t_Zlow - t_Zhigh)
	return cell


# %%
def bendLeftZhigh2(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l_residual = l_Zhigh - numpy.pi * (R_inner + R) / 2

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x - l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)

	return cell


# %%
def bendRightZhigh2(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l_residual = l_Zhigh - numpy.pi * (R_inner + R) / 2

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x + l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)

	return cell


# %%
def bendLeftZhighEqual(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l_residual = 0.5 * (l_Zhigh - numpy.pi * (R_inner + R) / 2)

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x - l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x + l_residual
	return cell


# %%
def bendLeftZlowEqual(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=700/2
	R = R_inner + t_Zlow
	l_residual = 0.5 * (l_Zlow - numpy.pi * (R_inner + R) / 2)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	position.x = position.x - l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	position.y = center_y - R
	position.x = position.x + l_residual
	return cell


# %%
def bendRightZhighEqual(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l_residual = 0.5 * (l_Zhigh - numpy.pi * (R_inner + R) / 2)

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x + l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l_residual, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x - l_residual
	return cell


# %%
def bendRightZhighRes(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l1 = 0
	l2 = 350
	l_residual = (l_Zhigh - numpy.pi * (R_inner + R) / 2) - l1 - l2

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l1, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x + l1

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-1.5 * numpy.pi,
		final_angle=-2.0 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y
	position.x = position.x + R_inner
	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + t_Zhigh, position.y - l_residual))
	cell.add(Zlow2)

	position.y = position.y - l_residual

	center_y = position.y
	center_x = position.x - R_inner

	Zlow3 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.0 * numpy.pi,
		final_angle=-2.5 * numpy.pi,
		**spec)
	cell.add(Zlow3)

	position.y = center_y - R
	position.x = center_x

	Zlow4 = gdspy.Rectangle((position.x, position.y), (position.x - l2, position.y + t_Zhigh))
	cell.add(Zlow4)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x - l2

	position.x = position.x - l_res

	return cell


# %%
def bendLeftZhighRes(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=900/2
	R = R_inner + t_Zhigh
	l1 = 350
	l2 = 0
	l_residual = (l_Zhigh - numpy.pi * (R_inner + R) / 2) - l1 - l2

	position.y = position.y + 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x - l_res

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l1, position.y + t_Zhigh))
	cell.add(Zlow2)

	position.x = position.x - l1

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-1.0 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y
	position.x = position.x - R
	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + t_Zhigh, position.y - l_residual))
	cell.add(Zlow2)

	position.y = position.y - l_residual

	center_y = position.y
	center_x = position.x + R

	Zlow3 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.0 * numpy.pi,
		**spec)
	cell.add(Zlow3)

	position.y = center_y - R
	position.x = center_x

	Zlow4 = gdspy.Rectangle((position.x, position.y), (position.x + l2, position.y + t_Zhigh))
	cell.add(Zlow4)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x + l2

	return cell


# %%
def bendRightZlowEqual(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=700/2
	R = R_inner + t_Zlow
	l_residual = 0.5 * (l_Zlow - numpy.pi * (R_inner + R) / 2)

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	position.x = position.x + l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-2.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	position.y = center_y - R
	position.x = position.x - l_residual
	return cell

	# %%


def bendRightZlowEND(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	R = R_inner + t_Zlow
	l1 = 350
	l2 = 0
	l_residual = (l_Zlow - numpy.pi * (R_inner + R) / 2) - l1 - l2

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + l1, position.y + t_Zlow))
	cell.add(Zlow2)

	position.x = position.x + l1

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-1.0 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y
	position.x = position.x - R
	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x + t_Zhigh, position.y - l_residual))
	cell.add(Zlow2)

	position.y = position.y - l_residual

	center_y = position.y
	center_x = position.x + R

	Zlow3 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.0 * numpy.pi,
		**spec)
	cell.add(Zlow3)

	position.y = center_y - R
	position.x = center_x

	Zlow4 = gdspy.Rectangle((position.x, position.y), (position.x + l2, position.y + t_Zhigh))
	cell.add(Zlow4)

	position.y = center_y - R - 0.5 * (t_Zlow - t_Zhigh)
	position.x = position.x + l2

	return cell


# %%
def bendLeftZlow2(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner):
	# R_inner=700/2
	R = R_inner + t_Zlow
	l_residual = l_Zlow - numpy.pi * (R_inner + R) / 2

	Zlow2 = gdspy.Rectangle((position.x, position.y), (position.x - l_residual, position.y + t_Zlow))
	cell.add(Zlow2)

	position.x = position.x - l_residual

	center_y = position.y - R_inner
	center_x = position.x

	Zlow1 = gdspy.Round(
		(center_x, center_y),
		R,
		inner_radius=R_inner,
		initial_angle=-0.5 * numpy.pi,
		final_angle=-1.5 * numpy.pi,
		**spec)
	cell.add(Zlow1)

	position.y = center_y - R
	return cell


# %%
def resonator(position, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow):
	res = gdspy.Rectangle((position.x, position.y + 0.5 * (t_Zlow - t_res)),
	                      (position.x + l_res, position.y + 0.5 * (t_Zlow - t_res) + t_res))
	cell.add(res)
	##%% Adding C fingers to the resonator

	x_init = position.x  # x coordinate where the resonator starts
	y_init = position.y + 0.5 * (t_Zlow - t_res) + t_res  # upper y coordinate of the resonator

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

	gndRes_upper = gdspy.Rectangle((position.x, position.y + t_Zlow + gap),
	                               (position.x + l_res, position.y + t_Zlow + gap - gndRes_h))
	gndRes_bottom = gdspy.Rectangle((position.x, position.y - gap), (position.x + l_res, position.y - gap + gndRes_h))
	cell.add(gndRes_bottom)
	cell.add(gndRes_upper)

	##%%C fingers from additional ground planes

	y_start_up = position.y + t_Zlow + gap - gndRes_h
	y_start_down = position.y - gap + gndRes_h

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

	position.x = position.x + l_res

	return cell


# %% Meander
# cell=gdspy.Cell('PGB')
# cursor=Position.Position()
#
# cell.add(Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell.add(Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#
# cell.add(Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell=bendRightZhigh(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#
# cell.add(ZlowBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell.add(ZhighBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#
# cell=bendLeftZlowEqual(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
# cell.add(Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#
# cell=resonator(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
# cell.add(Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#
# cell=bendRightZlowEqual(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
##
# cell.add(ZhighBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell.add(ZlowBack(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell=bendLeftZhigh2(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#
# cell.add(Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell.add(Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
# cell.add(Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))


# %% Meander 2
cell = gdspy.Cell('PGB')
cursor = Position.Position()

cell.add(Zlow(cursor, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
cell = bendRightZhigh(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)

cell = bendLeftZlow(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)
cell = bendRightZhigh(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)

cell = bendLeftZlow(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)
cell = bendRightZhigh(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)

cell = bendLeftZlow(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)
cell = bendRightZhighRes(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)

cell = resonator(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)

cell = bendLeftZhighRes(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)
cell = bendRightZlow2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)

cell = bendLeftZhigh2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)

cell = bendRightZlow2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)
cell = bendLeftZhigh2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)

cell = bendRightZlow2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)
cell = bendLeftZhigh2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_high)
cell = bendRightZlow2(cursor, cell, l_Zhigh, l_Zlow, t_Zhigh, t_Zlow, R_inner_low)
# %% No meander
# cell=gdspy.Cell('PGB')
# cursor=Position.Position()
#
# for i in range(number):
#    cell.add(Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#    cell.add(Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#    
##cell=resonator(cursor,cell,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow)
#    
# for i in range(number):
#    cell.add(Zhigh(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))
#    cell.add(Zlow(cursor,l_Zhigh, l_Zlow, t_Zhigh, t_Zlow))


# %%
## Generate GDS ##
## ------------------------------------------------------------------ ##
##	OUTPUT															  ##
## ------------------------------------------------------------------ ##
## Output the layout to a GDSII file (default to all created cells).
## Set the units we used to micrometers and the precision to nanometers.
gdspy.gds_print(filepath + "/" + filename, unit=1.0e-6, precision=1.0e-9)
print('gds file saved to "' + filepath + "/" + filename + '"')

## ------------------------------------------------------------------ ##
##	VIEWER															  ##
## ------------------------------------------------------------------ ##
## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
# gdspy.LayoutViewer()
print('PGB Finished!')
