#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from random import choice, randint, sample, random, seed
from itertools import combinations




###############################
### Change these parameters ###
###############################

NUM_ANTIBIOTICS = 3
POPULATION_SIZE = 5000
PROBABILITY_RESISTANCE_CHANGE= 0.2
PROPORTION_TREATED_PER_ROUND = 0.2
PROBABILITY_SPREAD = 0.1
NUM_TIMESTEPS = 20

#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))
ANTIBIOTIC_NAMES = [i+1 for i in range(NUM_ANTIBIOTICS)]
ANTIBIOTIC_COMBINATIONS = []
for i in reversed(range(len(ANTIBIOTIC_NAMES)+1)):
    ANTIBIOTIC_COMBINATIONS.extend([",".join(map(str,j))
                            for j in combinations(ANTIBIOTIC_NAMES,i)])
ANTIBIOTIC_COMBINATIONS.append("#")




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

        # Store data about percentage resistance of each combination of
        # resistances throughout the model run
        self.x_data = []
        self.ys_data = [[] for _ in range(2 ** NUM_ANTIBIOTICS + 1)]

    def run(self):
        """Simulate a number of timesteps within the model"""

        self.x_data = range(NUM_TIMESTEPS)
        for i in range(NUM_TIMESTEPS):

            # Report how far through the run when a multiple of a set percentage
            # of steps are completed
            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10) )

            # Record the data for the timestep
            infection_percentages = self.get_infection_percentages().values()
            for i,data_point in enumerate(infection_percentages):
                self.ys_data[i].append(data_point)

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

        print("Done!")

    def get_infection_percentages(self):
        """Get the percentage infected with each type of bacteria"""
        infections = {name:0 for name in ANTIBIOTIC_COMBINATIONS}
        for person in self.population:
            infections[self.infection_list_to_names(person)] += 1

        return {infection: (float(number) / POPULATION_SIZE) * 100
                                    for infection,number in infections.items()}

    def infection_list_to_names(self, person):
        """Turn a persons infection list into the name of those infections"""
        name = ",".join([str(i+1) for i,v in enumerate(person.infections) if v])
        if name == "":
            return "#"
        return name

    def __repr__(self):
        """Return a string encoding the percentage of people infected by
        each anti-biotice resistant bacteria"""
        infection_strings = ""
        for k,v in self.get_infection_percentages():
            infection_strings += "{}% {}".format(v, k)
        return ",".join(infection_strings)



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
    plt.stackplot(m.x_data, *m.ys_data, labels=ANTIBIOTIC_COMBINATIONS)
    plt.legend(loc='upper right')
    plt.xlabel("Time / timesteps")
    plt.ylabel("Infections / %")
    plt.show()
