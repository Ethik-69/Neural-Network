#! /usr/bin/python
# -*- coding: utf-8 -*-
# input: food plus proche
# output: Up, Right, Down, Left
import sys
import random

try:
    import pygame
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)

import constants
from cell import Cell
from cell import EvilCell
from grid import Grid
from graph import Graph
from interface import Interface


class Simulation(object):
    def __init__(self):
        pygame.init()

        width = int(constants.pixel_size * constants.width * 1.5)
        height = constants.pixel_size * constants.height
        self.window = pygame.display.set_mode((width, height))

        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()
        self.background.fill((10, 10, 10))

        pygame.display.set_caption('Simulation')

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.interface = Interface(self.window)
        self.graph = Graph()
        self.grid = Grid()
        self.grid.random_grid()

        self.cells = []
        self.evil_cells = []
        self.init_population()

        self.time = 0
        self.run = True
        self.view_sensors = False
        self.is_stop = False
        self.population = None
        self.average_fitness = 0
        self.average_evil_fitness = 0
        self.average_error = 0.0
        self.average_evil_error = 0.0
        self.average_output = [0, 0]

        self.play_pause_button = None
        self.sensors_button = None
        self.bad_cell_button = None

    def add_cell(self):
        """ Create a new cell """
        return Cell(self.grid,
                    constants.n_inputs,
                    constants.n_hidden,
                    constants.n_outputs,
                    (255, 255, 255))

    def add_evil_cell(self):
        """ Create a new evil cell """
        return EvilCell(self.grid,
                    constants.n_inputs,
                    constants.n_hidden,
                    constants.n_outputs,
                    (255, 0, 0))

    def init_population(self):
        """ Initialise all cells """
        while len(self.cells) != constants.population_limit:
            self.cells.append(self.add_cell())

    def rand(self, a, b):
        return (b - a) * random.random() + a

    def reset_cells(self):
        """ Put back has zero all cells """
        print("[*] Reset self.cells pos and feeding")
        for cell in self.cells:
            cell.init(self.grid)

    def stop(self):
        """ Pygame pause loop """
        is_stop = True
        self.create_buttons()

        MOUSEDOWN = False
        while is_stop:
            self.window.fill((10, 10, 10))

            self.interface.update("stop", self.view_sensors)

            self.grid.display(self.window)

            self.interface.display_info(self.average_fitness,
                                        self.average_evil_fitness,
                                        len(self.cells),
                                        len(self.evil_cells),
                                        self.average_output,
                                        self.average_error,
                                        self.average_evil_error)

            mouse_xy = pygame.mouse.get_pos()

            self.update_all_cells_stop(mouse_xy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    elif event.key == K_SPACE:
                        is_stop = False
                elif event.type == MOUSEBUTTONDOWN:
                    MOUSEDOWN = True
                    if event.button == 1:  # left click add/del food
                        if self.play_pause_button.collidepoint(mouse_xy):
                            is_stop = False
                        elif self.bad_cell_button.collidepoint(mouse_xy):
                            self.evil_cells.append(self.add_evil_cell())
                        elif self.sensors_button.collidepoint(mouse_xy):
                            if self.view_sensors:
                                self.view_sensors = False
                            else:
                                self.view_sensors = True
                        if mouse_xy[0] < constants.width * constants.pixel_size:
                            for cell in self.cells:
                                if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                                    print("[*] Cell Chosen")
                                    self.interface.cell_to_display = cell
                elif event.type == MOUSEBUTTONUP:
                    MOUSEDOWN = False

            if mouse_xy[0] < constants.width * constants.pixel_size and MOUSEDOWN:
                self.change_cell_on_click(mouse_xy)

            pygame.time.wait(0)
            pygame.display.flip()

    def change_cell_on_click(self, mouse_xy):
        """ Add or Del food """
        if self.grid.grid[(mouse_xy[0]) / constants.pixel_size][mouse_xy[1] / constants.pixel_size] != 1:
            self.grid.grid[(mouse_xy[0]) / constants.pixel_size][mouse_xy[1] / constants.pixel_size] = 1
        else:
            self.grid.grid[(mouse_xy[0]) / constants.pixel_size][mouse_xy[1] / constants.pixel_size] = 0

    def update_all_cells_main(self):
        # Update and Draw all cells  -----------------------------------
        for cell in self.cells:
            if cell.alive:
                self.average_error += cell.error
                self.average_fitness += cell.feeding
                cell.update(self.grid)
                self.average_output[0] += cell.brain.array_output[0]
                self.average_output[1] += cell.brain.array_output[1]
                if self.view_sensors and not cell.view_sensors:
                    cell.view_sensors = True
                elif not self.view_sensors:
                    cell.view_sensors = False

            else:
                self.cells.remove(cell)

        # Update and Draw all bad cells  -----------------------------------
        for cell in self.evil_cells:
            if cell.alive:
                self.average_evil_error += cell.error
                self.average_evil_fitness += cell.feeding
                cell.update(self.grid)
                if self.view_sensors and not cell.view_sensors:
                    cell.view_sensors = True
                elif not self.view_sensors:
                    cell.view_sensors = False

            else:
                self.cells.remove(cell)

    def update_all_cells_stop(self, mouse_xy):
        # Update and Draw cells
        for cell in self.cells:
            if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                print("[*] Cell Chosen")
                self.interface.cell_to_display = cell

        # Update and Draw evil cells
        for cell in self.evil_cells:
            if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                print("[*] Evil Cell Chosen")
                self.interface.cell_to_display = cell

    def end(self):
        print("[*] Evil cells Win !")
        print("[*] Evil population: %s" % len(self.evil_cells))
        print("[*] Average Error: %s" % self.average_error)
        print("[*] Average Fitness: %s" % self.average_fitness)

    def create_buttons(self):
        self.play_pause_button = pygame.draw.rect(self.window, (50, 50, 50), [constants.pixel_size * constants.width + 40,
                                                                   constants.pixel_size * constants.height / 2 + 400,
                                                                   50, 50])

        self.sensors_button = pygame.draw.rect(self.window, (255, 255, 255),
                                         [constants.pixel_size * constants.width + 140,
                                          constants.pixel_size * constants.height / 2 + 400,
                                         50, 50])

        self.bad_cell_button = pygame.draw.rect(self.window, (255, 255, 255),
                                           [constants.pixel_size * constants.width + 240,
                                           constants.pixel_size * constants.height / 2 + 400,
                                           50, 50])

    def reset_averages(self):
        self.average_fitness = 0
        self.average_evil_fitness = 0
        self.average_output = [0, 0]
        self.average_error = 0.0
        self.average_evil_error = 0.0

    def calc_averages(self):
        self.average_output[0] /= len(self.cells)
        self.average_output[1] /= len(self.cells)
        self.average_fitness /= len(self.cells)
        self.average_error /= len(self.cells)
        if len(self.evil_cells) != 0:
            self.average_evil_fitness /= len(self.evil_cells)
            self.average_evil_error /= len(self.evil_cells)

    def main(self):
        """ Pygame main loop """
        self.create_buttons()

        while self.run:

            if len(self.cells) == 0:
                self.end()

            self.window.fill((10, 10, 10))

            self.interface.update("start", self.view_sensors)
            self.grid.display(self.window)
            self.grid.update(self.window)
            self.grid.clean_grid()

            self.interface.display_info(self.average_fitness,
                                        self.average_evil_fitness,
                                        len(self.cells),
                                        len(self.evil_cells),
                                        self.average_output,
                                        self.average_error,
                                        self.average_evil_error)

            self.reset_averages()
            self.update_all_cells_main()
            self.calc_averages()

            self.time += 1

            if self.time % 25 == 0:
                self.graph.update(self.time, self.average_error)

            mouse_xy = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    elif event.key == K_SPACE:
                        self.stop()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click add/del food
                        if self.play_pause_button.collidepoint(mouse_xy):
                            self.stop()
                        elif self.bad_cell_button.collidepoint(mouse_xy):
                            self.evil_cells.append(self.add_evil_cell())
                        elif self.sensors_button.collidepoint(mouse_xy):
                            if self.view_sensors:
                                self.view_sensors = False
                            else:
                                self.view_sensors = True

            pygame.time.wait(0)
            pygame.display.flip()


if __name__ == "__main__":
    simu = Simulation()
    simu.main()


# TODO: food object !
# TODO: correction bug radar, bord de map
# TODO: corection bug black follow red ! (cell when eat/move calls)

# TODO: Refacto + doc

# IDEA: enemy detection (priority ? avoid enemy or got to food ?)
# IDEA: no more than 1 cell per case
# IDEA: add position allies
# IDEA: add color to food (different color = different values) and give it to the network
