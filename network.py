#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
import random
import numpy


def sigmoid(x):
    # return math.tanh(x)
    return 1 / (1 + numpy.exp(- x))


def dsigmoid(y):
    return 1.0 - y**2


def rand(a, b):
    return (b - a) * random.random() + a


class Network(object):
    def __init__(self, inputs, hidden, outputs, random_weight=False, weight_in=[], weight_out=[]):
        # number of input, hidden...
        self.num_input = inputs + 1
        self.num_hidden = hidden
        self.num_output = outputs

        self.array_inputs = [1.0] * self.num_input
        self.array_hidden = [1.0] * self.num_hidden
        self.array_output = [1.0] * self.num_output

        self.weights_inputs = weight_in
        self.weights_outputs = weight_out

        if random_weight:
            self.generate_random_weights()

        self.change_input = [[0.0] * self.num_hidden for i in range(self.num_input)]
        self.change_output = [[0.0] * self.num_output for i in range(self.num_hidden)]

    def generate_random_weights(self):
        # weight
        self.weights_inputs = [[0.0] * self.num_hidden for i in range(self.num_input)]
        self.weights_outputs = [[0.0] * self.num_output for i in range(self.num_hidden)]

        # make it random
        for i in range(self.num_input):
            for j in range(self.num_hidden):
                self.weights_inputs[i][j] = rand(-1.0, 1)

        for j in range(self.num_hidden):
            for k in range(self.num_output):
                self.weights_outputs[j][k] = rand(-1.0, 1)

        for weight in range(len(self.weights_inputs[len(self.weights_inputs)-1])):
            self.weights_inputs[len(self.weights_inputs)-1][weight] = -1.0

    def update(self, inputs):
        # inputs = sensors_up, sensors_down.....
        if len(inputs) != self.num_input - 1:
            raise ValueError('Wrong number of inputs')

        for i in range(self.num_input - 1):
            self.array_inputs[i] = inputs[i]

        for j in range(self.num_hidden):
            sum = 0.0
            for i in range(self.num_input):
                sum += self.array_inputs[i] * self.weights_inputs[i][j]
            self.array_hidden[j] = sigmoid(sum)

        for k in range(self.num_output):
            sum = 0.0
            for j in range(self.num_hidden):
                sum += self.array_hidden[j] * self.weights_outputs[j][k]
            self.array_output[k] = sigmoid(sum)

    def back_propagate(self, targets, N=0.5, M=0.1):
        if len(targets) != self.num_output:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.num_output
        for k in range(self.num_output):  # pour chaque neuronnes de sortie
            error = targets[k] - self.array_output[k]  # cible moins sortie actuel
            output_deltas[k] = dsigmoid(self.array_output[k]) * error  # sortie x taux d'erreur

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.num_hidden
        for j in range(self.num_hidden):  # pour chaque neuronnes de la couche actuel
            error = 0.0
            for k in range(self.num_output):  # pour chaque neuronnes de la couche précédente
                error += output_deltas[k] * self.weights_outputs[j][k]  # sortie x taux d'erreur de ce neuronnes x weights correspondante
            hidden_deltas[j] = dsigmoid(self.array_hidden[j]) * error

        # update output weights
        for j in range(self.num_hidden):
            for k in range(self.num_output):
                change = output_deltas[k] * self.array_hidden[j]
                self.weights_outputs[j][k] = self.weights_outputs[j][k] + N * change + M * self.change_output[j][k]  # N ? M ?
                self.change_output[j][k] = change

        # update input weights
        for i in range(self.num_input):
            for j in range(self.num_hidden):
                change = hidden_deltas[j] * self.array_inputs[i]
                self.weights_inputs[i][j] = self.weights_inputs[i][j] + N * change + M * self.change_input[i][j]
                self.change_input[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error += 0.5 * (targets[k] - self.array_output[k]) ** 2
        return error

if __name__ == '__main__':
    wi = [[-0.021858447945422327, 0.15219448821928644, 0.06082195473891955, 0.08347288040659018], [0.1909121994812456, 0.16105687191039053, -0.18769546135253634, -0.014766294761266202], [0.1546242895212776, 0.12797293882949273, -0.0036336475923524902, 0.19020235957394455], [-0.12670289813821722, -0.16469072475937652, -0.18832445439002538, 0.0315962797173035], [-1.0, -1.0, -1.0, -1.0]]
    wo = [[-0.9560856525569337, 1.361885539452147, -0.46025552144298976, -1.9203233473106556], [-0.7744125106477409, 1.6341349615063914, 1.3810698098353176, 1.8758718034680735], [1.6863192074827609, -0.010694900162080412, -0.9888487949707563, 1.7803953355881577], [1.734576801155785, 1.6756635731090488, -0.44186306886283155, 1.2406913611755344]]
    wi = [[0.26777949697389036, 0.40576637840820373, 0.5561047626915733, 0.9816730819743473], [0.06295111101015927, 0.4803281330036596, 0.41922086503844636, 0.4069755859410127], [0.1920851487859575, 0.4401183663843169, 0.6417338141656637, 0.29451283631081926], [0.7695015057103675, 0.13194202511124686, 0.4126372777161512, 0.9426528527733363], [-1.0, -1.0, -1.0, -1.0]]
    wo = [[0.9960964261424552, 0.16616383413273628, 0.400849759641964, 1.0786720627410384], [0.27681258227100125, 1.734382340428455, 0.2374133321110985, 0.9292830818672713], [1.2305083837149202, 0.0025727197721989725, 0.21766866303329557, 0.09266162214256624], [1.911732428688653, 0.9937593684843562, 0.87978178789927, 0.9620244995489264]]

    net = Network(2, 3, 2, True)
    net.update([0.1, -0.2])
    print(net.weights_inputs)
    print(net.weights_outputs)
    for neuron in net.weights_outputs:
        print(neuron)
    print("output: ")
    for out in net.array_output:
        print(round(out), out)





