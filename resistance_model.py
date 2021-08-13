#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from random import choice, randint, sample, random, seed
from math import comb


###############################
### Change these parameters ###
###############################

RANDOM_SEED = 0
NUM_ANTIBIOTICS = 3
POPULATION_SIZE = 5000
PROBABILITY_RESISTANCE_CHANGE= 0.05
PROPORTION_TREATED_PER_ROUND = 0.2
PROBABILITY_SPREAD = 0.1


class Person:
    def __init__(self):
        """Everybody starts uninfected in the model"""
        self.infections = [False] * NUM_ANTIBIOTICS

    def mutate_infections(self):
        """Flip whether the person is resistant to each antibiotic with a
        very low probability"""
        for i in range(NUM_ANTIBIOTICS):
            if decision(PROBABILITY_RESISTANCE_CHANGE):
                self.infections[i] = not(self.infections[i])

    def treat_infection(self, infection_index):
        """Treat the infection (remove it) with a given treatment"""
        self.infections[infection_index] = False

    def spread_infection(self, other):
        """Give any present infections from the current object to the other
        object"""
        other.infections = [bool(x+y) for x,y in zip(
                                            self.infections, other.infections)]


class Model:
    def __init__(self, population=None):
        """Start the model with a population of uninfected people, or a custom
        population provided as a parameter"""
        if population is None:
            self.population = [Person() for i in range(POPULATION_SIZE)]
        else:
            self.population = population

    def run(self, num_timesteps=200):
        """Simulate a number of timesteps within the model"""

        # Store data about percentage resistance throughout the model run
        self.x_data = range(num_timesteps)
        self.ys_data = [[] for i in range(NUM_ANTIBIOTICS+1)]

        for i in range(num_timesteps):
            # Record the data for the timestep
            infection_percentages = list(self.get_infection_percentages())
            for i,data_point in enumerate(infection_percentages):
                self.ys_data[i].append(data_point)
            self.ys_data[-1].append(100-sum(infection_percentages))

            # Mutate the infections for every person in the population
            for person in self.population:
                person.mutate_infections()

            # Randomly select some people to treat with random drugs
            to_treat = sample(self.population,
                            int(POPULATION_SIZE*PROPORTION_TREATED_PER_ROUND))

            # Treat each of these people with a random drug
            for person in to_treat:
                person.treat_infection(randint(0, NUM_ANTIBIOTICS - 1))

            # Randomly spread
            if decision(PROBABILITY_SPREAD):
                spreader = choice(self.population)
                receiver = choice(list(set(self.population)
                                                            - set([spreader])))
                spreader.spread_infection(receiver)

    def get_infection_percentages(self):
        """Get the percentage infected with each type of bacteria"""
        infections = [0]*NUM_ANTIBIOTICS
        for person in self.population:
            infections = [x + y for x, y in zip(infections, person.infections)]
        return map(lambda x: 100*float(x)/POPULATION_SIZE, infections)

    def __repr__(self):
        """Return a string encoding the percentage of people infected by
        each anti-biotice resistant bacteria"""
        return "Infections: {}".format([str(p)+"%" for p in
                                            self.get_infection_percentages()])



def decision(probability):
    """Get a boolean value with a given probability"""
    return random() < probability



if __name__ == "__main__":
    # Seed the random number generator
    if RANDOM_SEED is not None:
        seed(RANDOM_SEED)

    # Create and run the model
    m = Model()
    m.run()

    # Create a stacked area plot of the infection data
    # https://www.python-graph-gallery.com/stacked-area-plot/
    plt.stackplot(m.x_data, *m.ys_data, labels=['A','B','C','#'])
    plt.legend(loc='upper right')
    plt.xlabel("Time / timesteps")
    plt.ylabel("Infections / %")
    plt.show()
