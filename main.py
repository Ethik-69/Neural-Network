#! /usr/bin/python
# -*- coding: utf-8 -*-
# input: food plus proche
# output: Up, Right, Down, Left
import sys
import random
import pygame

from pygame.locals import *
import matplotlib.pyplot as plt

import constants
from network import *
from time_made_home import *


class Grid(object):
    def __init__(self):
        self.height = constants.height
        self.width = constants.width
        self.pixel_size = constants.pixel_size
        self.chance_food = constants.chance_food
        self.chance_add_random_food = constants.chance_add_random_food
        self.grid = [[0] * self.width for i in xrange(self.height)]
        self.color_swich = {0: [0, 0, 0],
                            1: [0, 100, 100],
                            2: [250, 10, 10],
                            3: [0, 0, 80]}

    def random_grid(self):
        """Initialise la grille aleatoirement"""
        for i in xrange(self.height):
            for j in xrange(self.width):
                if random.random() < self.chance_food:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0

    def add_random_food(self):
        """Ajoute aleatoirement un case nourriture au hasard"""
        if random.random() < self.chance_add_random_food:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[x][y] != 3:
                self.grid[x][y] = 1

    def display(self, window):
        """Affiche la grille case par case"""
        for ligne in xrange(self.height):
            for colone in xrange(self.width):
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
        """nettoie la grille pour 'voir' les senseur"""
        for i in range(constants.width):
            for j in range(constants.height):
                if self.grid[i][j] == 2:
                    self.grid[i][j] = 1
                elif self.grid[i][j] == 3:
                    self.grid[i][j] = 0

    def update(self, window):
        self.add_random_food()
        self.add_random_food()
        # self.clean_grid()


class Cell(object):
    def __init__(self, name, grid, first_gen=False, weight_in=[], weight_out=[]):
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
        """Initialise les valeurs par default"""
        self.x = 0
        self.y = 0
        self.feeding = 0
        self.random_pos(grid)
        self.alive = True
        self.life = Rebour(self.name)
        self.life.start([00, 02, 00])
        self.sensor = [0, 0]

    def create_brain(self, first_gen, weight_in, weight_out):
        """Crée le cerveau (Neural Network)"""
        if first_gen:
            self.brain = Network(constants.n_inputs, constants.n_hidden, constants.n_outputs, True)
        else:
            self.brain = Network(constants.n_inputs, constants.n_hidden, constants.n_outputs, False, weight_in, weight_out)

    def random_pos(self, grid):
        randm = True
        while randm:
            self.x = random.randint(0, int(constants.width - 1))
            self.y = random.randint(0, int(constants.width - 1))
            if grid.grid[self.x][self.y] == 0:
                randm = False

    def display(self, window):
        """Ajuste la couleur en fonction de la vie"""
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
        window.fill([255, life, 255],
                    (self.x * constants.pixel_size, self.y * constants.pixel_size,
                     constants.pixel_size - 1, constants.pixel_size - 1))

    def capture(self, grid):
        """ 'Detecte' la cellule/case contenant de la nourriture la plus proche"""
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
        """ 'Mange' la nourriture si la cellule est sur la 'bonne' case"""
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
        """Met à jour la cellule"""
        self.num_update += 1
        self.capture(grid.grid)
        self.brain.update(self.sensor)
        targets = [0.4, 0.4, 0.4, 0.4]
        if self.sensor == [0, 0]:
            pass
        else:
            if self.sensor[0] < 0:
                targets[3] = 0.6
                targets[1] = 0.4
            elif self.sensor[0] > 0:
                targets[1] = 0.6
                targets[3] = 0.4
            if self.sensor[1] < 0:
                targets[0] = 0.6
                targets[2] = 0.4
            elif self.sensor > 0:
                targets[0] = 0.4
                targets[2] = 0.6
        print(self.sensor, targets)
        self.error = 0.0
        self.error = self.brain.back_propagate(targets)
        self.move()
        # self.collapse_window(grid)
        self.life.update()
        self.total_life_time.update()
        if self.life.isFinish:
            self.alive = False
        self.live_update(grid)

    def move(self):
        """Déplace la cellule en fonction des sorties du reseau de neurones"""
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


class Graph(object):
    def __init__(self):
        plt.style.use('ggplot')
        plt.xlabel('Time')
        plt.ylabel('Fitness')
        self.x = [0]
        self.y = [0]
        self.best = [0]
        self.axis_x = 1
        self.axis_y = 1
        plt.axis([0, self.axis_x, 0, self.axis_y])
        plt.ion()
        plt.show()

    def update(self, x, y, best_cell):
        self.x.append(x)
        self.y.append(y)
        self.best.append(best_cell)

        if self.axis_x < x:
            self.axis_x = x
        else:
            pass

        if self.axis_y < y:
            self.axis_y = y
        if self.axis_y < best_cell:
            self.axis_y = best_cell

        plt.axis([0, self.axis_x * 1.1, 0, self.axis_y * 1.1])
        plt.plot(self.x, self.y, color='black', label="average fitness")
        plt.plot(self.x, self.best, color='blue', label="best cell")
        plt.draw()


class Interface(object):
    def __init__(self, window):
        self.window = window
        self.cell_to_display = None

    def update(self, mode):
        pygame.draw.line(self.window, (255, 255, 255),
                         (constants.pixel_size * constants.width, 0),
                         (constants.pixel_size * constants.width, constants.pixel_size * constants.height))

        pygame.draw.line(self.window, (255, 255, 255),
                         (constants.pixel_size * constants.width, constants.pixel_size * constants.height / 2),
                         (constants.pixel_size * constants.width * 1.5, constants.pixel_size * constants.height / 2))

        if mode == "start":
            pygame.draw.rect(self.window, (255, 255, 255),
                             [constants.pixel_size * constants.width + 52, constants.pixel_size * constants.height / 2 + 408,
                              10, 30])
            pygame.draw.rect(self.window, (255, 255, 255),
                             [constants.pixel_size * constants.width + 72, constants.pixel_size * constants.height / 2 + 408,
                              10, 30])
        elif mode == "stop":
            pygame.draw.polygon(self.window, (255, 255, 255),
                               [(constants.pixel_size * constants.width + 52, constants.pixel_size * constants.height / 2 + 408),
                                (constants.pixel_size * constants.width + 79, constants.pixel_size * constants.height / 2 + 422),
                                (constants.pixel_size * constants.width + 52, constants.pixel_size * constants.height / 2 + 438)])

        # Display chosen cell
        if self.cell_to_display is not None:
            self.display_cell_info()
            self.display_neural_net()

    def display_cell_info(self):
        """Affiche les infos de la cellule sélèctionnée à l'écran"""
        font = pygame.font.Font('fonts/visitor1.ttf', 20)

        text = font.render("fitness:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 50,
                                 centery=13)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.feeding), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 110,
                                 centery=13)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Pos:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 30,
                                 centery=30)
        self.window.blit(text, text_pos)

        text = font.render("x:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 100,
                                 centery=30)
        self.window.blit(text, text_pos)

        text = font.render("y:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 190,
                                 centery=30)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.x), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 140,
                                 centery=30)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.y), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 230,
                                 centery=30)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Input:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 43,
                                 centery=47)
        self.window.blit(text, text_pos)

        text = font.render("x:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 100,
                                 centery=47)
        self.window.blit(text, text_pos)

        text = font.render("y:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 190,
                                 centery=47)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.sensor[0], 3), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 140,
                                 centery=47)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.sensor[1], 3), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 230,
                                 centery=47)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Output:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 50,
                                 centery=64)
        self.window.blit(text, text_pos)

        text = font.render("Up:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 120,
                                 centery=64)
        self.window.blit(text, text_pos)

        text = font.render("Right:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 260,
                                 centery=64)
        self.window.blit(text, text_pos)

        text = font.render("down:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 120,
                                 centery=77)
        self.window.blit(text, text_pos)

        text = font.render("left:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 260,
                                 centery=77)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(round(self.cell_to_display.brain.array_output[0], 3)), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 190,
                                 centery=64)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(round(self.cell_to_display.brain.array_output[1], 3)), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 320,
                                 centery=64)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(round(self.cell_to_display.brain.array_output[2], 3)), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 190,
                                 centery=77)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(round(self.cell_to_display.brain.array_output[3], 3)), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 320,
                                 centery=77)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Error:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 40,
                                 centery=90)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.error), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 180,
                                 centery=90)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Update:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 50,
                                 centery=110)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(self.cell_to_display.num_update), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 150,
                                 centery=110)
        self.window.blit(text, text_pos)

    def display_neural_net(self):
        font = pygame.font.Font('fonts/visitor1.ttf', 15)

        text = font.render("Not Activated", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 390,
                                 centery=constants.pixel_size * constants.height / 2 - 10)
        self.window.blit(text, text_pos)

        text = font.render("Activated", 1, (255, 20, 20))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 370,
                                 centery=constants.pixel_size * constants.height / 2 - 30)
        self.window.blit(text, text_pos)

        # Inputs ----------------------------------------------------------------

        for i in range(len(self.cell_to_display.brain.array_inputs) - 1):
            pygame.draw.circle(self.window, (255, 255, 255),
                               (constants.pixel_size * constants.width + 80, 230 + i * 70),
                               10)

            # Values
            text = font.render(str(self.cell_to_display.brain.array_inputs[i]), 1, (255, 255, 255))
            text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 50,
                                     centery=230 + i * 70)
            self.window.blit(text, text_pos)

            # Lines
            for j in range(len(self.cell_to_display.brain.array_hidden)):
                pygame.draw.line(self.window, (255, 255, 255),
                                 (constants.pixel_size * constants.width + 80, 230 + i * 70),
                                 (constants.pixel_size * constants.width + 230, 160 + j * 70))

        # Hidden ----------------------------------------------------------------

        for i in range(len(self.cell_to_display.brain.array_hidden)):
            pygame.draw.circle(self.window, (255, 255, 255),
                               (constants.pixel_size * constants.width + 230, 160 + i * 70),
                               10)
            # Values
            text = font.render(str(round(self.cell_to_display.brain.array_hidden[i], 3)), 1, (255, 255, 255))
            text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 230,
                                     centery=130 + i * 70)
            self.window.blit(text, text_pos)

            # Lines
            for j in range(len(self.cell_to_display.brain.array_output)):
                pygame.draw.line(self.window, (255, 255, 255),
                                 (constants.pixel_size * constants.width + 230, 160 + i * 70),
                                 (constants.pixel_size * constants.width + 400, 160 + j * 70))

        # Outputs ----------------------------------------------------------------

        for i in range(len(self.cell_to_display.brain.array_output)):
            if self.cell_to_display.brain.array_output[i] > 0.5:
                pygame.draw.circle(self.window, (255, 20, 20),
                                   (constants.pixel_size * constants.width + 400, 160 + i * 70),
                                   10)
            else:
                pygame.draw.circle(self.window, (255, 255, 255),
                                   (constants.pixel_size * constants.width + 400, 160 + i * 70),
                                   10)

            text = font.render(str(round(self.cell_to_display.brain.array_output[i], 3)), 1, (255, 255, 255))
            text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 400,
                                     centery=130 + i * 70)
            self.window.blit(text, text_pos)

    def display_info(self, average_fitness, best_cells, generation, len_cells, len_dead_cells, average_output):
        """Affiche les infos sur la simulation à l'écran"""
        font = pygame.font.Font('fonts/visitor1.ttf', 20)

        text = font.render("Generation: ", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 72,
                                 centery=constants.pixel_size * constants.height / 2 + 15)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(generation), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 155,
                                 centery=constants.pixel_size * constants.height / 2 + 15)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Population Number:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 110,
                                 centery=constants.pixel_size * constants.height / 2 + 45)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(len_cells), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 230,
                                 centery=constants.pixel_size * constants.height / 2 + 45)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Dead Population Number:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 140,
                                 centery=constants.pixel_size * constants.height / 2 + 62)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(len_dead_cells), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 290,
                                 centery=constants.pixel_size * constants.height / 2 + 62)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Average Fitness:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 97,
                                 centery=constants.pixel_size * constants.height / 2 + 100)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(average_fitness), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 230,
                                 centery=constants.pixel_size * constants.height / 2 + 100)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Best Cells:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 72,
                                 centery=constants.pixel_size * constants.height / 2 + 130)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(best_cells), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 230,
                                 centery=constants.pixel_size * constants.height / 2 + 150)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        text = font.render("Average Output:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 97,
                                 centery=constants.pixel_size * constants.height / 2 + 180)
        self.window.blit(text, text_pos)

        text = font.render("x:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 60,
                                 centery=constants.pixel_size * constants.height / 2 + 200)
        self.window.blit(text, text_pos)

        text = font.render("y:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 60,
                                 centery=constants.pixel_size * constants.height / 2 + 220)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(round(average_output[0], 3)), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 100,
                                 centery=constants.pixel_size * constants.height / 2 + 200)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(round(average_output[1], 3)), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 100,
                                 centery=constants.pixel_size * constants.height / 2 + 220)
        self.window.blit(text, text_pos)


def add_cell(grid, first_gen, weight_in=[], weight_out=[]):
    return Cell('cell', grid, first_gen, weight_in, weight_out)


def init_population(grid, cells):
    cells = cells
    while len(cells) != constants.population_limit:
        cells.append(add_cell(grid, True))
    return cells


# Display ----------------------------------------------------------------


def print_info(cell):
    """Print les infos d'une cellule"""
    print("#########################################################")
    print("[*] Feeding: " + str(cell.feeding))
    print("[*] Input: " + str(cell.sensor))
    print("[*] Genome In: " + str(cell.genome_in))
    print("[*] Genome out: " + str(cell.genome_out))
    print("[*] Output: " + str(cell.brain.array_output))
    print("[*] Life: " + str(cell.life.Time))


# Algo genetique ----------------------------------------------------------


def sort_population(cells):
    """Trie la population en fonction de la nourriture manger (fitness)"""
    print("[*] Sort Population")
    return sorted(cells, key=lambda x: x.feeding, reverse=True)


def mutate_population(population):
    """Fais muter les individues de la population"""
    print("[*] Mutate Population")
    for individual in population:
        if random.random() <= constants.mutate_chance:
            print("[*] Mutate")
            first_place_to_mutate = constants.choice([0, 1])
            second_place_to_mutate_in = int(random.random() * len(individual.genome_in[0]) - 1)
            second_place_to_mutate_out = int(random.random() * len(individual.genome_out[0]) - 1)
            individual.genome_in[first_place_to_mutate][second_place_to_mutate_in] = rand(0.0, 1.0)
            individual.genome_out[first_place_to_mutate][second_place_to_mutate_out] = rand(0.0, 1.0)
    return population


def crossover_population(cells, population, grid):
    """Création de nouvelle cellule grace à celle encore en vie"""
    print("[*] Crossover Population")
    childs = []
    count_child = 0
    while len(childs) != constants.population_limit - len(cells) - (constants.population_limit/10):
        weight_in = []
        weight_out = []
        mother = constants.choice(population)
        father = constants.choice(population)

        # selection father ----------------------------------------
        count = 0

        # Aléatoire
        while father.genome_in == mother.genome_in or father.genome_out == mother.genome_out:
            print("New father")
            if count > 5:  # Pour que ça ne prenne pas 3 siècles...
                break
            father = constants.choice(population)
            count += 1

        if count > 5:
            count = 0
            # Le "premier" qui vient
            for individual in population:
                if individual.genome_in == mother.genome_in or individual.genome_out == mother.genome_out:
                    count += 1
                else:
                    father = individual
                    break
                if count >= len(population):
                    father = constants.choice(population)

        # Création de l'enfant ---------------------------------------

        for i in range(len(mother.genome_in)):
            if random.random() > 0.5:
                weight_in.append(mother.genome_in[i])
            else:
                weight_in.append(father.genome_in[i])

        for i in range(len(mother.genome_out)):
            if random.random() > 0.5:
                weight_out.append(mother.genome_out[i])
            else:
                weight_out.append(father.genome_out[i])

        print(weight_in)
        print(weight_out)
        print('---------------------------------------------')

        childs.append(add_cell(grid, False, weight_in, weight_out))
        count_child += 1

    cells += childs
    return cells


def next_gen(cells, grid, cells_to_save):
    print("Number Of Cells For Natural Selection: " + str(len(cells)))
    population = sort_population(cells)

    #print("[*] Cut Population")
    #population = population[:len(population)/2]  # /2

    # save cell.feeding for display
    best_cells = []
    for i in range(constants.population_limit/10):
        best_cells.append(population[i].feeding)

    cells = crossover_population(cells, population, grid)

    # Add random cell
    print("[*] Add Random Cells")
    while len(cells) != constants.population_limit:
        cells.append(add_cell(grid, True))

    cells = mutate_population(cells)

    return cells, best_cells, cells_to_save


# -------------------------------------------------------------------------


def rand(a, b):
    return (b - a) * random.random() + a


def reset_cells(cells, grid):
    """Remet à "0" toute les cellules"""
    print("[*] Reset Cells pos and feeding")
    for cell in cells:
        cell.init(grid)
    return cells


# Sauvegarde/Chargement des Genomes ---------------------------------------------------


def save(to_save, stage):
    file_name = 'saved_weight' + str(stage) + '.txt'
    with open(file_name, 'a+') as file:
        for entre in to_save:
            file.write("genome_in: " + str(entre.genome_in) + "\n")
            file.write("genome_out: " + str(entre.genome_out) + "\n")


def next_stage(cells, stage):
    save(cells, stage)
    stage += 1
    return 0, stage


def load_genome():
    import saved_genome
    weight_in = []
    weight_out = []
    for gen in saved_genome.genome:
        if len(weight_in) > len(weight_out):
            weight_out.append(gen)
        else:
            weight_in.append(gen)
    return weight_in, weight_out


def init_population_with_gen(grid, weight_in, weight_out):
    cells = []
    for i in range(len(weight_in)):
        cells.append(Cell('cell', grid, False, weight_in[i], weight_out[i]))
    return cells


# -------------------------------------------------------------------------

def stop(window, inter, grid, average_fitness, best_cells, generation, len_cells, len_dead_cells, average_output, cells):
    is_stop = True
    start_button = pygame.draw.rect(window, (55, 50, 50), [constants.pixel_size * constants.width + 40,
                                                           constants.pixel_size * constants.height / 2 + 400,
                                                           50, 50])
    while is_stop:
        window.fill((10, 10, 10))

        inter.update("stop")

        grid.display(window)

        inter.display_info(average_fitness, best_cells, generation, len_cells, len_dead_cells, average_output)

        mouse_xy = pygame.mouse.get_pos()

        # Update and Draw cells
        for cell in cells:
            if cell.alive:
                cell.display(window)
            if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                print("[*] Cell Chosen")
                inter.cell_to_display = cell

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_SPACE:
                    is_stop = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Click gauche ajoute/supprime de la nourriture
                    if start_button.collidepoint(mouse_xy):
                        is_stop = False
                    if mouse_xy[0] < 960:
                        if grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] != 1:
                            grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] = 1
                        else:
                            grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] = 0

                        for cell in cells:
                            if cell.x == mouse_xy[0] / constants.pixel_size and cell.y == mouse_xy[1] / constants.pixel_size:
                                print("[*] Cell Chosen")
                                inter.cell_to_display = cell

        pygame.time.wait(0)
        pygame.display.flip()


def main():
    pygame.init()

    window = pygame.display.set_mode((int(constants.pixel_size * constants.width * 1.5),
                                      constants.pixel_size * constants.height))

    background = pygame.Surface(window.get_size())
    background = background.convert()
    background.fill((10, 10, 10))

    pygame.display.set_caption('Creature Simulation')

    window.blit(background, (0, 0))
    pygame.display.flip()

    inter = Interface(window)
    #graph = Graph()
    grid = Grid()
    grid.random_grid()

    cells = []
    # weight_in, weight_out = load_genome()
    # cells = init_population_with_gen(grid, weight_in, weight_out)
    cells = init_population(grid, cells)

    time = 0
    stage = 0
    run = True
    generation = 0
    best_cells = []
    dead_cells = []
    cells_to_save = []
    average_fitness = 0
    average_output = [0, 0]
    stop_button = pygame.draw.rect(window, (55, 50, 50), [constants.pixel_size * constants.width + 40,
                                                          constants.pixel_size * constants.height / 2 + 400,
                                                          50, 50])
    while run:
        window.fill((10, 10, 10))

        inter.update("start")
        grid.update(window)
        grid.display(window)
        time += 1
        # Next Stage
        if generation == constants.generation_per_stage:
            generation, stage = next_stage(cells, stage)

        # Next Generation
        if len(cells) <= constants.population_limit / 2:
            print("[*] Next Generation")
            cells, best_cells, cells_to_save = next_gen(cells, grid, cells_to_save)
            #graph.update(time, average_fitness, best_cells[0])
            dead_cells = []
            grid.random_grid()
            cells = reset_cells(cells, grid)
            generation += 1
            print("[*] Launch Generation")

        inter.display_info(average_fitness, best_cells, generation, len(cells), len(dead_cells), average_output)

        average_fitness = 0
        average_output = [0, 0]

        # Update and Draw cells
        for cell in cells:
            if cell.alive:
                average_fitness += cell.feeding
                cell.update(grid)
                average_output[0] += cell.brain.array_output[0]
                average_output[1] += cell.brain.array_output[1]
                cell.display(window)
            else:
                dead_cells.append(cell)
                cells.remove(cell)

        average_output[0] /= len(cells)
        average_output[1] /= len(cells)
        average_fitness /= len(cells)

        mouse_xy = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(cells_to_save, "quit")
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    save(cells_to_save, "quit")
                    sys.exit(0)
                elif event.key == K_e:
                    save(cells, "e")
                elif event.key == K_SPACE:
                    stop(window, inter,
                         grid, average_fitness,
                         best_cells, generation,
                         len(cells), len(dead_cells),
                         average_output, cells)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Click gauche ajoute/supprime de la nourriture
                    if stop_button.collidepoint(mouse_xy):
                        stop(window, inter,
                             grid, average_fitness,
                             best_cells, generation,
                             len(cells), len(dead_cells),
                             average_output, cells)
                    if mouse_xy[0] < 960:
                        if grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] != 1:
                            grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] = 1
                        else:
                            grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] = 0

        pygame.time.wait(0)
        pygame.display.flip()


if __name__ == "__main__":
    main()

# TODO: Refacto + doc
# TODO: Changer interface
# TODO: Algo génétique inutile, a supprimer/modifier
