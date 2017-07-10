#! /usr/bin/python
# -*- coding: utf-8 -*-
import random

width = 200
height = 200
pixel_size = 5

population_limit = 100

generation_per_stage = 1000

number_of_food = 500
chance_food = 0.05
chance_add_random_food = 0.9

mutate_chance = 0.1

sensor_limit = 10

choice = lambda x: x[int(random.random() * len(x))]

n_inputs = 2
n_hidden = 4
n_outputs = 4
