#! /usr/bin/python
# -*- coding: utf-8 -*-
# input: food plus proche
# output: x, y
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
        self.display(window)
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
        self.capture(grid.grid)
        self.brain.update(self.sensor)
        self.move()
        # self.collapse_window(grid)
        self.life.update()
        self.total_life_time.update()
        if self.life.isFinish:
            self.alive = False
        self.live_update(grid)

    def move(self):
        """Déplace la cellule en fonction des sorties du reseau de neurones"""
        # print(self.brain.array_output)
        if self.brain.array_output[0] > 0.5:
            self.x += 1
            if self.x > constants.width - 1:
                self.x = 0
        else:
            self.x -= 1
            if self.x < 0:
                self.x = constants.width - 1

        if self.brain.array_output[1] > 0.5:
            self.y += 1
            if self.y > constants.height - 1:
                self.y = 0
        else:
            self.y -= 1
            if self.y < 0:
                self.y = constants.height - 1


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


def add_cell(grid, first_gen, weight_in=[], weight_out=[]):
    return Cell('cell', grid, first_gen, weight_in, weight_out)


def init_population(grid, cells):
    cells = cells
    while len(cells) != constants.population_limit:
        cells.append(add_cell(grid, True))
    return cells


# Display ----------------------------------------------------------------


def display_info(window, average_fitness, best_cells, generation, len_cells, len_dead_cells, average_output):
    """Affiche les infos sur la simulation à l'écran"""
    font = pygame.font.Font('fonts/visitor1.ttf', 20)

    init_text = font.render("Population Number: {}".format(len_cells), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=140, centery=20)
    window.blit(init_text, init_text_pos)

    init_text = font.render("Dead Population Number: {}".format(len_dead_cells), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=165, centery=40)
    window.blit(init_text, init_text_pos)

    init_text = font.render("Generation: {}".format(generation), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=90, centery=60)
    window.blit(init_text, init_text_pos)

    init_text = font.render("Average Fitness: {}".format(average_fitness), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=120, centery=80)
    window.blit(init_text, init_text_pos)

    init_text = font.render("Best Cells:", 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=85, centery=100)
    window.blit(init_text, init_text_pos)

    init_text = font.render("{}".format(best_cells), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=320, centery=120)
    window.blit(init_text, init_text_pos)

    init_text = font.render("Average Output:", 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=110, centery=140)
    window.blit(init_text, init_text_pos)

    init_text = font.render("x:", 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=40, centery=160)
    window.blit(init_text, init_text_pos)

    init_text = font.render("y:", 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=40, centery=180)
    window.blit(init_text, init_text_pos)

    init_text = font.render("{}".format(round(average_output[0], 3)), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=80, centery=160)
    window.blit(init_text, init_text_pos)

    init_text = font.render("{}".format(round(average_output[1], 3)), 1, (255, 255, 255))
    init_text_pos = init_text.get_rect(centerx=80, centery=180)
    window.blit(init_text, init_text_pos)


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
    while len(childs) != constants.population_limit - len(cells):
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

    # print("[*] Cut Population")
    # population = population[:len(population)/2]  # /2

    # save cell.feeding for display
    best_cells = []
    for i in range(10):
        best_cells.append(population[i].feeding)

    population = mutate_population(population)

    cells = crossover_population(cells, population, grid)

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


def main():
    pygame.init()

    window = pygame.display.set_mode((constants.pixel_size * constants.width,
                                      constants.pixel_size * constants.height))

    background = pygame.Surface(window.get_size())
    background = background.convert()
    background.fill((40, 40, 40))

    pygame.display.set_caption('Creature Simulation')

    window.blit(background, (0, 0))
    pygame.display.flip()

    graph = Graph()
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

    while run:
        window.fill((40, 40, 40))
        grid.update(window)
        time += 1

        # Next Stage
        if generation == constants.generation_per_stage:
            generation, stage = next_stage(cells, stage)

        # Next Generation
        if len(cells) <= constants.population_limit / 2:
            print("[*] Next Generation")
            cells, best_cells, cells_to_save = next_gen(cells, grid, cells_to_save)
            graph.update(time, average_fitness, best_cells[0])
            dead_cells = []
            grid.random_grid()
            cells = reset_cells(cells, grid)
            generation += 1
            print("[*] Launch Generation")

        display_info(window, average_fitness, best_cells, generation, len(cells), len(dead_cells), average_output)

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
                run = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    save(cells_to_save, "quit")
                    run = False
                elif event.key == K_e:
                    save(cells, "e")
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Click gauche ajoute/supprime de la nourriture
                    if grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] != 1:
                        grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] = 1
                    else:
                        grid.grid[(mouse_xy[0])/constants.pixel_size][mouse_xy[1]/constants.pixel_size] = 0

        pygame.time.wait(0)
        pygame.display.flip()


if __name__ == "__main__":
    main()

# TODO: refacto
# TODO: ceux qui en on manger le plus dans un temp donnée