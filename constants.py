#! /usr/bin/python
# -*- coding: utf-8 -*-
import random

width = 120
height = 120
pixel_size = 6

population_limit = 50

generation_per_stage = 1000

chance_food = 0.08
chance_add_random_food = 0.7

mutate_chance = 1

sensor_limit = 5

choice = lambda x: x[int(random.random() * len(x))]

n_inputs = 2
n_hidden = 3
n_outputs = 2
