#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys

try:
    import matplotlib.pyplot as plt
except ImportError, errmsg:
    print('Requires matplotlib')
    print(errmsg)
    sys.exit(1)


class Graph(object):
    def __init__(self):
        plt.style.use('ggplot')
        plt.xlabel('Time')
        plt.ylabel('Error')
        self.x = [0]
        self.y = [0]
        self.best = [0]
        self.axis_x = 0.01
        self.axis_y = 0.01
        plt.axis([0, self.axis_x, 0, self.axis_y])
        plt.ion()
        plt.show()

    def update(self, x, y):
        self.x.append(x)
        self.y.append(y)

        if self.axis_x < x:
            self.axis_x = x
        else:
            pass

        if self.axis_y < y:
            self.axis_y = y

        plt.axis([0, self.axis_x * 1.1, 0, self.axis_y * 1.1])
        plt.plot(self.x, self.y, color='black', label="average fitness")
        plt.draw()
