#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import random
import constants
from network import *

try:
    import pygame
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)


class ParentCell(object):
    def __init__(self, grid, n_inputs, n_hidden, n_outputs, color):
        self.x = 0
        self.y = 0
        self.random_pos(grid)
        self.color = color
        self.alive = True
        self.feeding = 0  # fitness

        self.sensor = [0, 0]
        self.sensor_range = 1
        self.view_sensors = False

        self.brain = None
        self.num_update = 0
        self.error = 0.0
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs
        self.create_brain()

        self.genome_in = self.brain.weights_inputs
        self.genome_out = self.brain.weights_outputs

    def init(self, grid):
        """ Put back all data to the default values """
        self.x = 0
        self.y = 0
        self.feeding = 0
        self.random_pos(grid)
        self.alive = True
        self.sensor = [0, 0]

    def create_brain(self):
        """ Create brain (Neural Network)"""
        self.brain = Network(self.n_inputs, self.n_hidden, self.n_outputs, True)

    def random_pos(self, grid):
        """ Select a random position """
        randm = True
        while randm:
            self.x = random.randint(0, int(constants.width - 1))
            self.y = random.randint(0, int(constants.width - 1))
            if grid.grid[self.x][self.y] == 0:
                randm = False

    def move(self):
        """ Move the cell according to the network outputs """
        # print(self.brain.array_output) [up, right, down, left]

        if self.brain.array_output[0] > 0.5:
            self.y -= 1
            if self.y < 0:
                self.y = constants.height - 1

        if self.brain.array_output[1] > 0.5:
            self.x += 1
            if self.x > constants.width - 1:
                self.x = 0

        if self.brain.array_output[2] > 0.5:
            self.y += 1
            if self.y > constants.height - 1:
                self.y = 0

        if self.brain.array_output[3] > 0.5:
            self.x -= 1
            if self.x < 0:
                self.x = constants.width - 1


class Cell(ParentCell):
    def __init__(self, grid, n_inputs, n_hidden, n_outputs, color):
        ParentCell.__init__(self, grid, n_inputs, n_hidden, n_outputs, color)

    def capture(self, grid):
        """ Detect the nearest grid cell with food in it """
        self.sensor_range = 1
        self.sensor = [0, 0]
        sensor_on = True
        while sensor_on:
            min_x_range = self.x - self.sensor_range
            min_y_range = self.y - self.sensor_range
            if min_x_range < 0:
                min_x_range = 0
            if min_y_range < 0:
                min_y_range = 0
            for x in range(min_x_range, self.x + self.sensor_range):
                for y in range(min_y_range, self.y + self.sensor_range):
                    try:
                        if grid[x][y] == 1:
                            self.sensor = [x, y]
                        elif self.view_sensors:
                            grid[x][y] = 3  # Pour "voir" les senseurs
                    except:
                        pass

            if self.sensor == [0, 0] and self.sensor_range < constants.sensor_limit:
                self.sensor_range += 1
            else:
                sensor_on = False
                # "traduit" la position de la nourriture pour le reseau de neurones
                self.sensor = [(float(self.sensor[0] - self.x))/10, (float(self.sensor[1] - self.y))/10]
                # self.sensor = [self.sensor[0] - self.x, self.sensor[1] - self.y]

    def eat(self, grid):
        """ If the cell is on food, 'eat' it """
        if grid.grid[self.x][self.y] == 1 or grid.grid[self.x][self.y] == 2:
            grid.grid[self.x][self.y] = 0
            self.feeding += 1

    def update(self, grid):
        """ Update the cell """
        self.num_update += 1
        self.capture(grid.grid)
        self.brain.update(self.sensor)

        # Back Propagation
        targets = [0.4, 0.4, 0.4, 0.4]
        if self.sensor == [0, 0]:
            pass
        else:
            if self.sensor[0] < 0:
                targets[1] = 0.4
                targets[3] = 0.6
            elif self.sensor[0] > 0:
                targets[1] = 0.6
                targets[3] = 0.4

            if self.sensor[1] < 0:
                targets[0] = 0.6
                targets[2] = 0.4
            elif self.sensor[1] > 0:
                targets[0] = 0.4
                targets[2] = 0.6

        self.error = 0.0
        self.error = self.brain.back_propagate(targets)

        # ----------------------
        grid.grid[self.x][self.y] = 0
        self.move()
        self.eat(grid)
        grid.grid[self.x][self.y] = self


class EvilCell(ParentCell):
    def __init__(self, grid, n_inputs, n_hidden, n_outputs, color):
        ParentCell.__init__(self, grid, n_inputs, n_hidden, n_outputs, color)

    def capture(self, grid):
        """ Detect the nearest grid cell with food in it """
        self.sensor_range = 1
        self.sensor = [0, 0]
        sensor_on = True
        while sensor_on:
            min_x_range = self.x - self.sensor_range
            min_y_range = self.y - self.sensor_range
            if min_x_range < 0:
                min_x_range = 0
            if min_y_range < 0:
                min_y_range = 0
            for x in range(min_x_range, self.x + self.sensor_range):
                for y in range(min_y_range, self.y + self.sensor_range):
                    try:
                        if isinstance(grid[x][y], Cell):
                            self.sensor = [x, y]
                        elif self.view_sensors and grid[x][y] != 1:
                            grid[x][y] = 4  # Pour "voir" les senseurs
                    except:
                        pass
            if self.sensor == [0, 0] and self.sensor_range < constants.bad_sensor_limit:
                self.sensor_range += 1
            else:
                sensor_on = False
                # "traduit" la position de la nourriture pour le reseau de neurones
                self.sensor = [(float(self.sensor[0] - self.x))/10, (float(self.sensor[1] - self.y))/10]

    def eat(self, grid):
        """ If the cell is on another cell, 'eat' it """
        if isinstance(grid.grid[self.x][self.y], Cell):
            grid.grid[self.x][self.y].alive = False
            self.feeding += 1

    def update(self, grid):
        """ Update the cell """
        self.num_update += 1
        self.capture(grid.grid)
        self.brain.update(self.sensor)

        # Back Propagation
        targets = [0.4, 0.4, 0.4, 0.4]
        if self.sensor == [0, 0]:
            pass
        else:
            if self.sensor[0] < 0:
                targets[1] = 0.4
                targets[3] = 0.6
            elif self.sensor[0] > 0:
                targets[1] = 0.6
                targets[3] = 0.4

            if self.sensor[1] < 0:
                targets[0] = 0.6
                targets[2] = 0.4
            elif self.sensor[1] > 0:
                targets[0] = 0.4
                targets[2] = 0.6

        self.error = 0.0
        self.error = self.brain.back_propagate(targets)

        # ----------------------

        grid.grid[self.x][self.y] = 0
        self.move()
        self.eat(grid)
        grid.grid[self.x][self.y] = self
