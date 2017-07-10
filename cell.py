#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import random
import constants
from network import *
from time_made_home import *

try:
    import pygame
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)


class Cell(pygame.sprite.Sprite):
    def __init__(self, name, grid, all_sprites, first_gen=False, weight_in=[], weight_out=[]):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.x = 0
        self.y = 0
        self.random_pos(grid)
        self.name = name
        self.alive = True
        self.life = Rebour(self.name)
        self.total_life_time = Chrono(self.name)
        self.life.start([00, 02, 00])
        self.total_life_time.start()
        self.feeding = 0  # fitness

        self.sensor = [0, 0]
        self.sensor_range = 1

        self.brain = None
        self.num_update = 0
        self.error = 0.0
        self.create_brain(first_gen, weight_in, weight_out)

        self.genome_in = self.brain.weights_inputs
        self.genome_out = self.brain.weights_outputs

    def init(self, grid):
        """ Put back all data to the default values """
        self.x = 0
        self.y = 0
        self.feeding = 0
        self.random_pos(grid)
        self.alive = True
        self.life = Rebour(self.name)
        self.life.start([00, 02, 00])
        self.sensor = [0, 0]

    def create_brain(self, first_gen, weight_in, weight_out):
        """ Create brain (Neural Network)"""
        if first_gen:
            self.brain = Network(constants.n_inputs, constants.n_hidden, constants.n_outputs, True)
        else:
            self.brain = Network(constants.n_inputs, constants.n_hidden, constants.n_outputs, False, weight_in, weight_out)

    def random_pos(self, grid):
        """ Select a random position """
        randm = True
        while randm:
            self.x = random.randint(0, int(constants.width - 1))
            self.y = random.randint(0, int(constants.width - 1))
            if grid.grid[self.x][self.y] == 0:
                randm = False

    def display(self, window):
        """
        Select the color of the cell with the life left and drawn the cell
        """
        if len(str(self.life.Time[1])) == 1:
            min = "0" + str(self.life.Time[1])
        else:
            min = str(self.life.Time[1])

        if len(str(self.life.Time[2])) == 1:
            sec = "0" + str(self.life.Time[2])
        else:
            sec = str(self.life.Time[2])

        life = int(str(self.life.Time[0]) + min + sec)
        if life > 255:
            life = 255

        # drawn cell

        # commented : upscale cells =)
        #if self.feeding > 20:
        #    window.fill([255, life, 255],
        #                (self.x * constants.pixel_size, self.y * constants.pixel_size,
        #                 (constants.pixel_size - 1) * (self.feeding / 20), (constants.pixel_size - 1) * (self.feeding / 20)))
        #else:
        window.fill([255, life, 255],
                    (self.x * constants.pixel_size, self.y * constants.pixel_size,
                    constants.pixel_size - 1, constants.pixel_size - 1))

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
                        else:
                            pass
                            # grid[x][y] = 3  # Pour "voir" les senseurs
                    except:
                        pass
            if self.sensor == [0, 0] and self.sensor_range < constants.sensor_limit:
                self.sensor_range += 1
            else:
                sensor_on = False
                # "traduit" la position de la nourriture pour le reseau de neurones
                self.sensor = [(float(self.sensor[0] - self.x))/10, (float(self.sensor[1] - self.y))/10]
                # self.sensor = [self.sensor[0] - self.x, self.sensor[1] - self.y]

    def live_update(self, grid):
        """ If the cell is on food, 'eat' it """
        if grid.grid[self.x][self.y] == 1 or grid.grid[self.x][self.y] == 2:
            grid.grid[self.x][self.y] = 0
            self.feeding += 1
            self.life.Time[2] += 20

        if self.life.Time[2] > 99:
            self.life.Time[1] += 1
            self.life.Time[2] -= 99

        if self.life.Time[1] > 59:
            self.life.Time[0] += 1
            self.life.Time[1] -= 59

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

        self.move()
        self.life.update()
        self.total_life_time.update()
        if self.life.isFinish:
            self.alive = False
        self.live_update(grid)

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
