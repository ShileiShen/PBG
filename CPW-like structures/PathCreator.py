"""
@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""
import gdspy
import Position
import numpy
from Parameters import *

print('Using gdspy module version ' + gdspy.__version__)

# fuction that writes the created structure to gds file


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

# building IDC resonator


def resonator():
    createPoly(t_res, l_res, spec_path=spec_res)
    # %% Adding C fingers to the resonator
    position.move_x(-l_res)

    x_init = position.x  # x coordinate where the resonator starts
    y_init = position.y + 0.5 * t_res  # upper y coordinate of the resonator

    x_start = x_init + delta_x  # start of C fingers on the resonator

    def addCfinger(x0, y0, positive):
        if positive:
            cFinger = gdspy.Rectangle(
                (x0, y0), (x0 + w_c, y0 + h_c), **spec_res)
        else:
            cFinger = gdspy.Rectangle(
                (x0, y0), (x0 + w_c, y0 - h_c), **spec_res)
        cell.add(cFinger)

    x_step = 2 * w_c + 2 * w_sep
    # number of C fingers in one raw from one side only
    number_of_fingers = (l_res - 2 * delta_x + x_step) // (x_step)

    for j in range(round(number_of_fingers)):
        addCfinger(x_start + j * x_step, y_init, 1)
        addCfinger(x_start + j * x_step, y_init - t_res, 0)

    # %%additional ground planes for resonator
    gndRes_h = gap + t_Zlow / 2 - t_res / 2 - \
        h_sep - h_c  # width of additional ground plane

    gndRes_upper = gdspy.Rectangle((position.x, position.y + t_Zlow / 2 + gap),
                                   (position.x + l_res, position.y + t_Zlow / 2 + gap - gndRes_h), **spec_res)
    gndRes_bottom = gdspy.Rectangle((position.x, position.y - t_Zlow / 2 - gap),
                                    (position.x + l_res, position.y - t_Zlow / 2 - gap + gndRes_h), **spec_res)
    cell.add(gndRes_bottom)
    cell.add(gndRes_upper)

    # %%C fingers from additional ground planes
    y_start_up = position.y + t_Zlow / 2 + gap - gndRes_h
    y_start_down = position.y - t_Zlow / 2 - gap + gndRes_h

    # fingers connected to ground planes
    for i in range(round(number_of_fingers) - 1):
        x_var1 = x_start + (i + 1) * (x_step) - w_sep - w_c
        y_var1 = y_start_down

        x_var2 = x_var1 + w_c
        y_var2 = y_var1 + h_c

        # down_finger = CreatePath([(x_var1,y_var1),(x_var2,y_var2)],w_c,layer=0)
        down_finger = gdspy.Rectangle(
            (x_var1, y_var1), (x_var2, y_var2), **spec_res)

        y_var1_up = y_start_up
        y_var2_up = y_var1_up - h_c

        # up_finger = CreatePath([(x_var1,y_var1_up),(x_var2,y_var2_up)],w_c,layer=0)
        up_finger = gdspy.Rectangle(
            (x_var1, y_var1_up), (x_var2, y_var2_up), **spec_res)

        cell.add(down_finger)
        cell.add(up_finger)

    position.x = position.move_x(l_res)

    return cell


def poly_minus_x_draw(total_length, width, step, side_offset=min_side_offset):
    while (position.x > side_offset + R) and (position.length < total_length):
        createPoly(width, step, direction=position.direction)
        position.length += step


def poly_plus_x_draw(total_length, width, step, side_offset=min_side_offset):
    while (position.x < chip_width - side_offset - R) and (position.length < total_length):
        createPoly(width, step, direction=position.direction)
        position.length += step


def arc_minus_x_draw(d_angle, total_length, width):

    for n in range(round(numpy.pi / d_angle)):
        if (position.length < total_length) and (position.angle <= 3 * numpy.pi / 2):
            createArc(width, R, position.angle, position.angle + d_angle)
            position.length += d_angle * R
            position.add_angle(d_angle)
        else:
            break

    if (position.angle >= 3 * numpy.pi / 2):
        position.change_direction()
        position.arcContinue = False
        position.angle = -numpy.pi / 2
    else:
        position.arcContinue = True


def arc_half_minus_x_draw(d_angle, total_length, width):

    for n in range(round((numpy.pi / 2) / d_angle)):
        if (position.length < total_length) and (position.angle <= numpy.pi):
            createArc(width, R, position.angle, position.angle + d_angle)
            position.length += d_angle * R
            position.add_angle(d_angle)
        else:
            break

    if (position.angle >= numpy.pi):
        position.change_direction()
        position.arcContinue = False
        position.angle = -numpy.pi / 2
    else:
        position.arcContinue = True


def arc_plus_x_draw(d_angle, total_length, width):

    for n in range(round(numpy.pi / d_angle)):
        if (position.length < total_length) and (position.angle >= -3 * numpy.pi / 2):
            createArc(width, -R, position.angle, position.angle - d_angle)
            position.length += d_angle * R
            position.add_angle(-d_angle)
        else:
            break

    if (position.angle <= -3 * numpy.pi / 2):
        position.change_direction()
        position.arcContinue = False
        position.angle = numpy.pi / 2
    else:
        position.arcContinue = True


def arc_half_plus_x_draw(d_angle, total_length, width):

    for n in range(round((numpy.pi / 2) / d_angle)):
        if (position.length < total_length) and (position.angle >= -3 * numpy.pi / 2):
            createArc(width, -R, position.angle, position.angle - d_angle)
            position.length += d_angle * R
            position.add_angle(-d_angle)
        else:
            break

    if (position.angle <= -3 * numpy.pi / 2):
        position.change_direction()
        position.arcContinue = False
        position.angle = numpy.pi / 2
    else:
        position.arcContinue = True

# The main function that creates meanders


def meander_draw(total_length, width, step):

    if position.arcContinue == False:

        if position.direction == '-x':
            poly_minus_x_draw(total_length, width, step)
            if position.length < total_length:
                arc_minus_x_draw(d_angle, total_length, width)
            if position.length < total_length:
                meander_draw(total_length, width, step)

        if position.direction == '+x':
            poly_plus_x_draw(total_length, width, step)
            if position.length < total_length:
                arc_plus_x_draw(d_angle, total_length, width)
            if position.length < total_length:
                meander_draw(total_length, width, step)

    else:
        if position.angle < 0:
            arc_plus_x_draw(d_angle, total_length, width)
        else:
            arc_minus_x_draw(d_angle, total_length, width)
        if position.length < total_length:
            meander_draw(total_length, width, step)

    print(str(position.length) + '/')


# Overwritten meander_draw function to meet requirements for the last meander
def last_meander_draw(total_length, width, step):
    if position.arcContinue == False:

        if position.direction == '-x':
            poly_minus_x_draw(total_length, width, step,
                              last_meander_side_offset)
            if position.length < total_length:
                arc_half_minus_x_draw(d_angle, total_length, width)
            if position.length < total_length:
                #meander_draw(total_length, width, step)
                position.direction = '-y'
                while (position.length < total_length):
                    createPoly(width, step, direction=position.direction)
                    position.length += step

        if position.direction == '+x':
            poly_plus_x_draw(total_length, width, step,
                             last_meander_side_offset)
            if position.length < total_length:
                arc_half_plus_x_draw(d_angle, total_length, width)
            if position.length < total_length:
                #meander_draw(total_length, width, step)
                position.direction = '-y'
                while (position.length < total_length):
                    createPoly(width, step, direction=position.direction)
                    position.length += step

    else:
        if position.angle < 0:
            arc_half_plus_x_draw(d_angle, total_length, width)
        else:
            arc_half_minus_x_draw(d_angle, total_length, width)
        if position.length < total_length:
            last_meander_draw(total_length, width, step)

    print(str(position.length) + '/')


# Overwritten meander_draw function to meet requirements for the first meander
def first_meander_draw(total_length, width, step, direction):
    length = 0
    if direction == '+x':
        while position.x < chip_width - min_side_offset - R:
            createPoly(width, step, direction=direction)
            length += step
        if length < total_length:
            createArc(t_Zhigh, -R, -numpy.pi / 2.0, -numpy.pi)
            length += numpy.pi * R / 2
        if length < total_length:
            while position.y > chip_length / 2 - edge_offset - resonator_y_offset:
                createPoly(width, step, direction='-y')
                length += step
        if length < total_length:
            createArc(t_Zhigh, R, 0 * numpy.pi / 2.0, -numpy.pi / 2)
            length += numpy.pi * R / 2
        if length < total_length:
            createPoly(t_Zhigh, total_length - length, direction='-x')


def taper(initial_width, final_width, length, direction, step=step_polygon):
    a = (1 / float(length)) * numpy.log(final_width / float(initial_width))

    previous_width = initial_width
    for i in range(step, length, step):
        width = initial_width * numpy.exp(a * float(i))
        # print("Taper - i is %f \n\t a is %f \n\t exp is %f \n\t width is %f" % (i, a, numpy.exp(a * i), width))

        createPoly(width=previous_width, length=step,
                   direction=direction, final_width=width)
        previous_width = width


# END of FUNCTION definitions
##########################################################################
# Constracting the actual design by using function defined above


cell = gdspy.Cell('PathCreator')
# #define chip
position = Position.Position()
createPoly(chip_length, chip_width, spec_path=spec_path_chip)

# #draw a structure
position = Position.Position(
    x=chip_width / 2 - l_res / 2, y=chip_length / 2 - edge_offset)

resonator()

first_meander_draw(total_length=l_Zhigh, width=t_Zhigh,
                   direction='+x', step=step_polygon)
position.change_direction()

for i in range(number):  # number of repetitions
    print('new')
    position.length = 0  # before building new TL, the initial length should be set to zero
    meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
    position.length = 0
    print('new')
    meander_draw(total_length=l_Zhigh, width=t_Zhigh, step=step_polygon)
    position.length = 0


#meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
position.length = 0
last_meander_draw(total_length=l_Zlow, width=t_Zlow, step=step_polygon)
position.length = 0


createPoly(width=t_Zlow, length=l_taper, direction='-y',
           final_width=t_final)  # tapering at the end
#taper(t_Zlow, t_final, l_taper, direction='-y', step=step_polygon)

l_final = chip_length / 2 - abs(position.y)
createPoly(width=t_final, length=l_final, direction='-y')

write()  # writing the final structure to gds file
