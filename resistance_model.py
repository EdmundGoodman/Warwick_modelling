#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
random.seed(0)


NUM_ANTIBIOTICS = 3
POPULATION_SIZE = 50
RESISTANCE_CHANGE_PROB = 0.05



class Person:
    def __init__(self):
        """Everybody starts uninfected in the model"""
        self.infections = [False] * NUM_ANTIBIOTICS

    def mutate_infections(self):
        """Flip whether the person is resistant to each antibiotic with a
        very low probability"""
        for i in range(NUM_ANTIBIOTICS):
            if decision(RESISTANCE_CHANGE_PROB):
                self.infections[i] = not(self.infections[i])



class Model:
    def __init__(self, population=None):
        """Start the model with a population of uninfected people, or a custom
        population provided as a parameter"""
        if population is None:
            self.population = [Person() for i in range(POPULATION_SIZE)]
        else:
            self.population = population

    def run(self, num_timesteps=1000):
        """Simulate a number of timesteps within the model"""
        for i in range(num_timesteps):
            # Mutate the infections for every person in the population
            for person in self.population:
                person.mutate_infections()
            print(self)

    def __repr__(self):
        """Return a string encoding the percentage of people infected by
        each anti-biotice resistant bacteria"""
        infections = [0]*NUM_ANTIBIOTICS
        for person in self.population:
            infections = [x + y for x, y in zip(infections, person.infections)]
        percentages = map(lambda x: 100*float(x)/POPULATION_SIZE, infections)
        return "Infections: {}".format([str(p)+"%" for p in percentages])




def decision(probability):
    return random.random() < probability

if __name__ == "__main__":
    m = Model()
    m.run()
