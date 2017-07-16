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

        self.inter = Interface(self.window)
        self.graph = Graph()
        self.grid = Grid()
        self.grid.random_grid()

        self.cells = []
        self.init_population()

        self.time = 0
        self.stage = 0
        self.run = True
        self.view_sensors = False
        self.is_stop = False
        self.population = None
        self.generation = 0
        self.best_cells = []
        self.dead_cells = []
        self.cells_to_save = []
        self.average_fitness = 0
        self.average_error = 0.0
        self.average_output = [0, 0]

    def add_cell(self):
        """ Create a new cell """
        return Cell(self.grid,
                    constants.n_inputs,
                    constants.n_hidden,
                    constants.n_outputs)

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
        start_button = pygame.draw.rect(self.window, (50, 50, 50),
                                        [constants.pixel_size * constants.width + 40,
                                        constants.pixel_size * constants.height / 2 + 400,
                                        50, 50])

        sensors_button = pygame.draw.rect(self.window, (255, 255, 255),
                                          [constants.pixel_size * constants.width + 140,
                                          constants.pixel_size * constants.height / 2 + 400,
                                          50, 50])

        MOUSEDOWN = False
        while is_stop:
            self.window.fill((10, 10, 10))

            self.inter.update("stop", self.view_sensors)

            self.grid.display(self.window)

            self.inter.display_info(self.average_fitness,
                                    self.best_cells,
                                    self.generation,
                                    len(self.cells),
                                    len(self.dead_cells),
                                    self.average_output,
                                    self.average_error)

            mouse_xy = pygame.mouse.get_pos()

            # Update and Draw self.cells
            for cell in self.cells:
                if cell.alive:
                    cell.display(self.window)
                if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                    print("[*] Cell Chosen")
                    self.inter.cell_to_display = cell

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
                        if start_button.collidepoint(mouse_xy):
                            is_stop = False
                        if sensors_button.collidepoint(mouse_xy):
                            if self.view_sensors:
                                self.view_sensors = False
                            else:
                                self.view_sensors = True
                        if mouse_xy[0] < constants.width * constants.pixel_size:
                            for cell in self.cells:
                                if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                                    print("[*] Cell Chosen")
                                    self.inter.cell_to_display = cell
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

    def main(self):
        """ Pygame main loop """
        stop_button = pygame.draw.rect(self.window, (50, 50, 50), [constants.pixel_size * constants.width + 40,
                                                                   constants.pixel_size * constants.height / 2 + 400,
                                                                   50, 50])

        sensors_button = pygame.draw.rect(self.window, (255, 255, 255),
                                         [constants.pixel_size * constants.width + 140,
                                          constants.pixel_size * constants.height / 2 + 400,
                                         50, 50])

        while self.run:
            self.window.fill((10, 10, 10))

            self.inter.update("start", self.view_sensors)
            self.grid.display(self.window)
            self.grid.update(self.window)
            self.grid.clean_grid()

            self.time += 1

            self.inter.display_info(self.average_fitness,
                                    self.best_cells,
                                    self.generation,
                                    len(self.cells),
                                    len(self.dead_cells),
                                    self.average_output,
                                    self.average_error)

            self.average_fitness = 0
            self.average_output = [0, 0]
            self.average_error = 0.0

            # Update and Draw self.cells
            for cell in self.cells:
                if cell.alive:
                    self.average_error += cell.error
                    self.average_fitness += cell.feeding
                    cell.update(self.grid)
                    self.average_output[0] += cell.brain.array_output[0]
                    self.average_output[1] += cell.brain.array_output[1]
                    if self.view_sensors:
                        cell.view_sensors = True
                    else:
                        cell.view_sensors = False

                    cell.display(self.window)
                else:
                    self.dead_cells.append(cell)
                    self.cells.remove(cell)

            self.average_output[0] /= len(self.cells)
            self.average_output[1] /= len(self.cells)
            self.average_fitness /= len(self.cells)
            self.average_error /= len(self.cells)

            if self.time % 50 == 0:
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
                        if stop_button.collidepoint(mouse_xy):
                            self.stop()
                        if sensors_button.collidepoint(mouse_xy):
                            if self.view_sensors:
                                self.view_sensors = False
                            else:
                                self.view_sensors = True

            pygame.time.wait(0)
            pygame.display.flip()


if __name__ == "__main__":
    simu = Simulation()
    simu.main()

# En cour : Ajout "bad cells" that eat the white cells


# TODO: Refacto + doc
# TODO: add color to food (different color = different values) and give it to the network
# TODO: changer sensor, un nb de case vertical et horizontale ?
