#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from random import seed, random


###############################
### Change these parameters ###
###############################

NUM_TIMESTEPS = 500

#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))

#######################################
### Objects and logic for the model ###
#######################################

class Person:
    def __init__(self):
        """Initialise a person within the model"""
        pass

    def __repr__(self):
        return "Person"

class Model:
    def __init__(self, population=None):
        """Start the model with a population of defualt people, or a custom
        population provided as a parameter"""
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population

    def run(self):
        """Simulate a number of timesteps within the model"""
        for i in range(NUM_TIMESTEPS):

            # Report how far through the run when a multiple of a set percentage
            # of steps are completed
            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10) )

    def __repr__(self):
        """Return a string encoding the percentage of people infected by
        each anti-biotic resistant bacteria"""
        return "Model"


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
