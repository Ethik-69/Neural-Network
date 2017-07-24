#! /usr/bin/python
# -*- coding: utf-8 -*-
import constants
import random

from cell import Cell
from cell import EvilCell


class Grid(object):
    def __init__(self):
        self.height = constants.height
        self.width = constants.width
        self.pixel_size = constants.pixel_size
        self.chance_food = constants.chance_food
        self.chance_add_random_food = constants.chance_add_random_food
        self.grid = [[0] * self.width for i in xrange(self.height)]
        self.color_swich = {0: [0, 0, 0],  # Empty
                            1: [0, 100, 100],  # Foods
                            2: [250, 10, 10],
                            3: [0, 0, 80],  # Cells Sensors
                            4: [0, 255, 0]}  # Evil Cells Sensors

    def random_grid(self):
        """ Initialise the grid with random 'values' """
        for i in xrange(self.height):
            for j in xrange(self.width):
                if random.random() < self.chance_food:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0

    def add_random_food(self):
        """ Add some food in the grid at random position """
        for i in range(3):
            if random.random() < self.chance_add_random_food:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.grid[x][y] != 3:
                    self.grid[x][y] = 1

    def display(self, window):
        """ Display the grid case by case """
        for ligne in xrange(self.height):
            for colone in xrange(self.width):
                try:
                    window.fill(self.grid[ligne][colone].color,
                                (ligne * self.pixel_size,
                                 colone * self.pixel_size,
                                 self.pixel_size - 1,
                                 self.pixel_size - 1))
                except:
                    try:
                        colour = self.color_swich[self.grid[ligne][colone]]
                    except:
                        colour = [255, 255, 255]

                    if colour != [0, 0, 0]:
                        window.fill(colour, (ligne * self.pixel_size,
                                             colone * self.pixel_size,
                                             self.pixel_size - 1,
                                             self.pixel_size - 1))

    def clean_grid(self):
        """ Clean the grid if 'view sensors' is active """
        for i in range(constants.width):
            for j in range(constants.height):
                if self.grid[i][j] == 2:
                    self.grid[i][j] = 1
                elif self.grid[i][j] == 3:
                    self.grid[i][j] = 0
                elif self.grid[i][j] == 4:
                    self.grid[i][j] = 0

    def update(self, window):
        self.add_random_food()
        self.add_random_food()
