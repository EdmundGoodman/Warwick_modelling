#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from itertools import combinations


###############################
### Change these parameters ###
###############################

NUM_ANTIBIOTICS = 3
POPULATION_SIZE = 1000000
PROBABILITY_RESISTANCE_CHANGE= 0.1
PROPORTION_TREATED_PER_ROUND = 0.2
PROBABILITY_SPREAD = 0.5
NUM_TIMESTEPS = 20

#################################################
### Internal parameters and derived constants ###
#################################################

REPORT_PERCENTAGE = 5
REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))

ANTIBIOTIC_NAMES = [i+1 for i in range(NUM_ANTIBIOTICS)]
# Form up all the combinations of antibiotics, e.g. #, a, b, c, ab, ac, bc, abc
# then make probabilities of them occuring based on the PROBABILITY_RESISTANCE_CHANGE
# parameter being taken as the likelihood of any single antibiotic being present,
# with abc being (x^3), ab being (x^2 - x^3), and a being (x^1 - x^2 - x^3)
# I think this is actually wrong, as we need to take into account binomial
# coefficients
ANTIBIOTIC_COMBINATIONS = {}
for i in reversed(range(len(ANTIBIOTIC_NAMES) + 1)):
    name_combinations = list(combinations(ANTIBIOTIC_NAMES,i))
    for j,names in enumerate(name_combinations):
        probability = PROBABILITY_RESISTANCE_CHANGE ** len(names)
        for k in range(len(names), NUM_ANTIBIOTICS):
            probability -= PROBABILITY_RESISTANCE_CHANGE ** (k + 1)
        ANTIBIOTIC_COMBINATIONS[",".join(map(str, names))] = round(
                                                probability,NUM_ANTIBIOTICS)
ANTIBIOTIC_COMBINATIONS["#"] = ANTIBIOTIC_COMBINATIONS[""]
del ANTIBIOTIC_COMBINATIONS[""]

class Model:
    def __init__(self):
        """Initialise the model as having some data structures"""
        self.x_data = []
        self.ys_data = [[] for _ in range(2 ** NUM_ANTIBIOTICS + 1)]
        self.num_with_infections = {}

    def run(self):
        """Simulate a number of timesteps within the model"""

        self.num_with_infections = {name:0 for name in ANTIBIOTIC_COMBINATIONS.keys()}
        self.num_with_infections["#"] = POPULATION_SIZE

        self.x_data = range(NUM_TIMESTEPS)
        for i in range(NUM_TIMESTEPS):

            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10) )

            



    def __repr__(self):
        """Return a string encoding the percentage of people infected by
        each anti-biotice resistant bacteria"""
        infection_strings = ""
        for k,v in self.num_with_infections:
            infection_strings += "{}% {}".format(v, k)
        return ",".join(infection_strings)



if __name__ == "__main__":

    # Create and run the model
    m = Model()
    #m.run()


    """
    # Create a stacked area plot of the infection data
    # https://www.python-graph-gallery.com/stacked-area-plot/
    plt.stackplot(m.x_data, *m.ys_data)
    plt.legend(loc='upper right')
    plt.xlabel("Time / timesteps")
    plt.ylabel("Infections / %")
    plt.show()
    """
