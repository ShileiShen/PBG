# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:40:58 2018

@author: Mykhailo Savytskyi
@email: m.savytskyi@unsw.edu.au
"""
import numpy


class Position:
    """ Cursor for the PBG structure """

    def __init__(self, x=0, y=0, direction='+x', angle=numpy.pi / 2, arcContinue=False, length=0):
        """

        :rtype: Position
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.angle = angle
        self.arcContinue = arcContinue
        self.length = length

    def move_x(self, value):
        self.x = self.x + value
        return self.x

    def move_y(self, value):
        self.y = self.y + value
        return self.y

    def change_direction(self):
        if self.direction == '+x':
            self.direction = '-x'
        else:
            self.direction = '+x'

    def add_angle(self, value):
        self.angle += value
        return self.angle

    def __str__(self):
        return '(x = {0.x!s}, y = {0.y!s}), length = {0.length!s}'.format(self)

    def __repr__(self):
        #return '({0.x!r}, {0.y!r}, {0.length!r})'.format(self)
        return '(x = {0.x!s}, y = {0.y!s}), length = {0.length!s}'.format(self)

