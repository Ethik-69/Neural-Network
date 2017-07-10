#! /usr/bin/python
# -*- coding: utf-8 -*-
import constants

try:
    import pygame
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)


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
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 130,
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
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 45,
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

        inputs_names = ['X', 'Y']

        for i in range(len(self.cell_to_display.brain.array_inputs) - 1):
            pygame.draw.circle(self.window, (255, 255, 255),
                               (constants.pixel_size * constants.width + 80, 230 + i * 70),
                               10)

            # Values
            text = font.render(str(self.cell_to_display.brain.array_inputs[i]), 1, (255, 255, 255))
            text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 80,
                                     centery=200 + i * 70)
            self.window.blit(text, text_pos)

            # Names
            text = font.render(inputs_names[i], 1, (255, 255, 255))
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

        direction = ['Up', 'Right', 'Down', 'Left']

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

            text = font.render(direction[i], 1, (255, 255, 255))
            text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 450,
                                     centery=160 + i * 70)
            self.window.blit(text, text_pos)

    def display_info(self, average_fitness, best_cells, generation, len_cells, len_dead_cells, average_output, average_error):
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

        # -------------------------------------------------------------------------------------

        text = font.render("Average Error:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 97,
                                 centery=constants.pixel_size * constants.height / 2 + 240)
        self.window.blit(text, text_pos)

        text = font.render("{}".format(average_error), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 280,
                                 centery=constants.pixel_size * constants.height / 2 + 240)
        self.window.blit(text, text_pos)
