# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:40:58 2018

@author: z5119993
"""


class Position:
	""" Cursor for the PBG structure """

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def add_x(self, value):
		self.x = self.x + value
		return self.x

	def add_y(self, value):
		self.y = self.y + value
		return self.y
