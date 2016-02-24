#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Times(object):
    def __init__(self):
        self.rebours = {}
        self.chronos = {}

    def __getitem__(self, name, chrono=False):
        """Renvoi se qui est demander rebour ou chrono"""
        if not chrono:
            return self.rebours[name]
        else:
            return self.chronos[name]

    def add_rebour(self, name):
        """Instancie un rebour et l'ajoute a la liste des rebours 'actif' """
        self.rebours[name] = Rebour(name)

    def add_chrono(self, name):
        """Instancie un chrono et l'ajoute a la liste des chronos 'actif' """
        self.chronos[name] = Chrono(name)

    def update(self):
        """met à jour les chronos et les rebours"""
        for rebour in self.rebours:
            if self.rebours[rebour].is_started:
                self.rebours[rebour].update()

        for chrono in self.chronos:
            if self.chronos[chrono].is_started:
                self.chronos[chrono].update()


class Rebour(object):
    def __init__(self, name):
        self. name = name
        self.Time = None
        self.is_started = False
        self.isFinish = None

    def __getitem__(self):
        return self.isFinish

    def start(self, init_value):
        """Lance le rebour"""
        #print('[*] Rebour Start ' + self.name)
        self.Time = init_value
        self.is_started = True
        self.isFinish = False

    def stop(self):
        """Arrete le rebour"""
        self.is_started = False
        self.isFinish = True

    def update(self):
        """Met à jour le rebour"""
        self.Time[2] -= 1
        if self.Time[2] < 0:
            self.Time[2] = 99
            self.Time[1] -= 1
            if self.Time[1] < 0:
                self.Time[1] = 59
                self.Time[0] -= 1
                if self.Time[0] < 0:
                    self.Time = [0, 0, 0]
                    self.stop()


class Chrono(object):
    def __init__(self, name):
        self. name = name
        self.Time = None
        self.is_started = False

    def start(self):
        """Lance le chrono"""
        #print('[*] Chrono Start ' + self.name)
        self.is_started = True
        self.Time = [0, 0, 0]

    def reset(self):
        """Reset le chrono"""
        self.Time = [0, 0, 0]

    def stop(self):
        """Arrete le chrono"""
        self.is_started = False
        return self.Time

    def update(self):
        """Met à jour le chrono"""
        self.Time[2] += 1
        if self.Time[2] > 99:
            self.Time[2] = 0
            self.Time[1] += 1
            if self.Time[1] > 59:
                self.Time[1] = 0
                self.Time[0] += 1
                if self.Time[0] > 99:
                    self.Time = [0, 0, 0]
                    self.stop()
