#! /usr/bin/python
# -*- coding: utf-8 -*-
try:
    import pygame
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)
    

class Foods(object):
    def __init__(self, window, all_sprites, food_sprites):
        self.window = window
        self.all_sprites = all_sprites
        self.food_sprites = food_sprites

    def generate(self):
        for i in range(constants.number_of_food):
                x = random.randint(0, constants.width * constants.pixel_size)
                y = random.randint(0, constants.height * constants.pixel_size)
                food = Food(self.window, self.all_sprites, (x, y))
                self.food_sprites.add(food)

    def update(self, window):
        for i in range(3):
            if random.random() < constants.chance_add_random_food:
                x = random.randint(0, constants.width - 1)
                y = random.randint(0, constants.height - 1)
                food = Food(self.window, self.all_sprites, (x, y))
                self.food_sprites.add(food)


class Food(pygame.sprite.Sprite):
    def __init__(self, window, all_sprites, pos):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.x = pos[0]
        self.y = pos[1]

        self.image = pygame.Surface((constants.pixel_size, constants.pixel_size))
        self.image.fill([0, 100, 100])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
