#! /usr/bin/python
# -*- coding: utf-8 -*-
import random

width = 160
height = 160
pixel_size = 6

population_limit = 60

generation_per_stage = 1000

chance_food = 0.08
chance_add_random_food = 0.6

mutate_chance = 0.1

sensor_limit = 8

choice = lambda x: x[int(random.random() * len(x))]

n_inputs = 2
n_hidden = 4
n_outputs = 2
