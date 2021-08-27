#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from random import seed, random


###############################
### Change these parameters ###
###############################

NUM_TIMESTEPS = 500
POPULATION_SIZE = 5000


#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))

#######################################
### Objects and logic for the model ###
#######################################


class Infection:
    def __init__(self, present=False, resistances=None):
        self.present = present
        if resistances is not None:
            self.resistances = resistances
        else:
            self.resistances = []

    def __repr__(self):
        if self.present:
            return "Infection resistant to: {}".format(",".join(resistances))
        else:
            return "No infection"


class Treatment:
    def __init__(self, drug=None):
        self.drug = drug

    def __repr__(self):
        return "Treating with drug: {}".format(self.drug)


class Person:
    def __init__(self):
        self.isolated = False
        self.infection = Infection()
        self.treatment = Treatment()

    def __repr__(self):
        return "Person"


class Model:
    def __init__(self, population=None):
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population

        # We also have some other lists to move people into to speed up
        # processing
        self.dead = []

    def run(self):
        """Simulate a number of timesteps within the model"""
        for i in range(NUM_TIMESTEPS):

            # Report how far through the run when a multiple of a set percentage
            # of steps are completed
            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10))

            # For each person in the population
            for person in self.population:

                # Recovery generally or by treatement
                # (green line in first slide of powerpoint)

                # Mutation due to treatment
                # (blue line in first slide of powerpoint)

                # Moving up in treatment class

                # Deaths due to infection
                # (orange line in first slide of powerpoint)

    def __repr__(self):
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
