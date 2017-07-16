#! /usr/bin/python
# -*- coding: utf-8 -*-
import constants

try:
    import pygame
    from pygame import gfxdraw
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)


class Interface(object):
    def __init__(self, window):
        self.window = window
        self.cell_to_display = None

    def draw_arc(self, surface, center, radius, start_angle, stop_angle, color):
        x,y = center
        start_angle = int(start_angle%360)
        stop_angle = int(stop_angle%360)
        gfxdraw.arc(surface, x, y, radius, start_angle, stop_angle, color)


    def update(self, mode, view_sensors):
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

        self.draw_sensors_icone(view_sensors)

        # Display chosen cell
        if self.cell_to_display is not None:
            self.display_cell_info()
            self.display_neural_net()

    def draw_sensors_icone(self, view_sensors):
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     35, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     34, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     33, 225, 315, (255, 255, 255))


        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     28, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     27, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     26, 225, 315, (255, 255, 255))


        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     21, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     20, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     19, 225, 315, (255, 255, 255))


        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     14, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     13, 225, 315, (255, 255, 255))
        self.draw_arc(self.window, (constants.pixel_size * constants.width + 165,
                                    constants.pixel_size * constants.height / 2 + 440),
                                     12, 225, 315, (255, 255, 255))

        pygame.draw.circle(self.window, (255, 255, 255),
                           (constants.pixel_size * constants.width + 166,
                            constants.pixel_size * constants.height / 2 + 440),
                           6, 0)

        if view_sensors:
            pygame.draw.line(self.window, (255, 0, 0),
                            (constants.pixel_size * constants.width + 140, constants.pixel_size * constants.height / 2 + 400),
                            (constants.pixel_size * constants.width + 190, constants.pixel_size * constants.height / 2 + 450), 3)

            pygame.draw.line(self.window, (255, 0, 0),
                            (constants.pixel_size * constants.width + 190, constants.pixel_size * constants.height / 2 + 400),
                            (constants.pixel_size * constants.width + 140, constants.pixel_size * constants.height / 2 + 450), 3)

    def display_text(self, font, text, color, x, y):
        text = font.render(text, 1, color)
        text_pos = text.get_rect(centerx=x, centery=y)
        self.window.blit(text, text_pos)

    def display_cell_info(self):
        """ Display selected cell data """
        font = pygame.font.Font('fonts/visitor1.ttf', 20)

        self.display_text(font, "fitness:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 50, 13)

        self.display_text(font, "{}".format(self.cell_to_display.feeding),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 130, 13)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Pos:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 30, 30)

        self.display_text(font, "x:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 100, 30)

        self.display_text(font, "y:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 190, 30)

        self.display_text(font, "{}".format(self.cell_to_display.x),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 140, 30)

        self.display_text(font, "{}".format(self.cell_to_display.y),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230, 30)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Input:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 43, 47)

        self.display_text(font, "x:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 100, 47)

        self.display_text(font, "y:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 190, 47)

        self.display_text(font, "{}".format(self.cell_to_display.sensor[0], 3),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 140, 47)

        self.display_text(font, "{}".format(self.cell_to_display.sensor[1], 3),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230, 47)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Output:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 50, 64)

        self.display_text(font, "Up:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 120, 64)

        self.display_text(font, "Right:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 260, 64)

        self.display_text(font, "down:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 120, 77)

        self.display_text(font, "left:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 260, 77)

        self.display_text(font, "{}".format(round(self.cell_to_display.brain.array_output[0], 3)),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 190, 64)

        self.display_text(font, "{}".format(round(self.cell_to_display.brain.array_output[1], 3)),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 320, 64)

        self.display_text(font, "{}".format(round(self.cell_to_display.brain.array_output[2], 3)),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 190, 77)

        self.display_text(font, "{}".format(round(self.cell_to_display.brain.array_output[3], 3)),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 320, 77)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Error:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 45, 90)

        self.display_text(font, "{}".format(self.cell_to_display.error),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 180, 90)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Update:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 50, 110)

        self.display_text(font, "{}".format(self.cell_to_display.num_update),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 150, 110)

    def display_neural_net(self):
        font = pygame.font.Font('fonts/visitor1.ttf', 15)

        self.display_text(font, "Not Activated",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 388,
                          constants.pixel_size * constants.height / 2 - 13)

        self.display_text(font, "Activated",
                          (255, 20, 20),
                          constants.pixel_size * constants.width + 370,
                          constants.pixel_size * constants.height / 2 - 30)

        # Inputs ----------------------------------------------------------------

        inputs_names = ['X', 'Y']

        for i in range(len(self.cell_to_display.brain.array_inputs) - 1):
            pygame.draw.circle(self.window, (255, 255, 255),
                               (constants.pixel_size * constants.width + 80,
                               230 + i * 70), 10)

            # Values
            text = font.render(str(self.cell_to_display.brain.array_inputs[i]),
                               1,
                               (255, 255, 255))
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
        """ Display simulation data """
        font = pygame.font.Font('fonts/visitor1.ttf', 20)

        self.display_text(font, "Population Number:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 110,
                          constants.pixel_size * constants.height / 2 + 45)

        self.display_text(font, "{}".format(len_cells),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230,
                          constants.pixel_size * constants.height / 2 + 45)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "{}".format(len_cells),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230,
                          constants.pixel_size * constants.height / 2 + 45)

        text = font.render("Dead Population Number:", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 140,
                                 centery=constants.pixel_size * constants.height / 2 + 62)
        self.window.blit(text, text_pos)

        self.display_text(font, "{}".format(len_cells),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230,
                          constants.pixel_size * constants.height / 2 + 45)

        text = font.render("{}".format(len_dead_cells), 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=constants.pixel_size * constants.width + 290,
                                 centery=constants.pixel_size * constants.height / 2 + 62)
        self.window.blit(text, text_pos)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Average Fitness:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 97,
                          constants.pixel_size * constants.height / 2 + 100)

        self.display_text(font, "{}".format(average_fitness),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230,
                          constants.pixel_size * constants.height / 2 + 100)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Best Cells:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 72,
                          constants.pixel_size * constants.height / 2 + 130)

        self.display_text(font, "{}".format(best_cells),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 230,
                          constants.pixel_size * constants.height / 2 + 150)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Average Output:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 97,
                          constants.pixel_size * constants.height / 2 + 180)

        self.display_text(font, "x:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 60,
                          constants.pixel_size * constants.height / 2 + 200)

        self.display_text(font, "y:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 60,
                          constants.pixel_size * constants.height / 2 + 220)

        self.display_text(font, "{}".format(round(average_output[0], 3)),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 100,
                          constants.pixel_size * constants.height / 2 + 200)

        self.display_text(font, "{}".format(round(average_output[1], 3)),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 100,
                          constants.pixel_size * constants.height / 2 + 220)

        # -------------------------------------------------------------------------------------

        self.display_text(font, "Average Error:",
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 97,
                          constants.pixel_size * constants.height / 2 + 240)

        self.display_text(font, "{}".format(average_error),
                          (255, 255, 255),
                          constants.pixel_size * constants.width + 280,
                          constants.pixel_size * constants.height / 2 + 240)
