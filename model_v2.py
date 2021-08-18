#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from random import seed, random
from copy import deepcopy


###############################
### Change these parameters ###
###############################

NUM_TIMESTEPS = 500
POPULATION_SIZE = 5000
NUM_RESISTANCE_TYPES = 3
PROBABILITY_MUTATION = 0.02

PROBABILITY_GENERAL_RECOVERY = 0.01


#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))
RESISTANCE_NAMES = [str(i+1) for i in range(NUM_RESISTANCE_TYPES)]


#######################################
### Objects and logic for the model ###
#######################################

class Infection:
    def __init__(self, resistances=None):
        """Initialise an infection within the model"""
        if resistances is not None:
            self.resistances = resistances
        else:
            self.resistances = {name: False for name in RESISTANCE_NAMES}

    def make_resistant(self, resistance):
        """Return whether the infection has a specified resistance"""
        self.resistances[resistance] = True

    def is_resistant(self, resistance):
        """Give the infection a specified resistance"""
        return self.resistances[resistance]

    def get_tier(self):
        """Return how resistant the infection is - higher is more resistant"""
        for i in reversed(range(NUM_RESISTANCE_TYPES)):
            # RESISTANCE_NAMES is assumed to be ordered from first to last
            # resort treatment resistances
            if self.resistances[RESISTANCE_NAMES[i]] == True:
                return i
        return -1

    def get_resistances_string(self):
        """Get a canonical name for the present resistances"""
        string = ",".join([k for k, v in self.resistances.items() if v])
        if string == "":
            return "#"
        return string

    def __repr__(self):
        """Provide a string representation for the infection"""
        return "infection with resistances: {}".format(
            self.get_resistances_string())


class Person:
    def __init__(self, initial_infection=None, immune=False):
        """Initialise a person within the model"""
        self.infection = initial_infection
        self.immune = immune
        self.current_treatment = None
        self.alive = True

    def mutate_infection(self):
        """Make the infection become resistant to the treatment with a given
        probability of occurring"""
        if self.infection is not None and self.current_treatment is not None:
            self.infection.make_resistant(self.current_treatment)

    def recover_from_infection(self):
        """Recover the person, returning them to their default state; totally
        uninfected with no resistances, but now immune to the infection -
        irrespective of any resistances it has"""
        self.__init__(immune=True)

    def treat_infection(self, treatment_name):
        """Treat the infection with an treatment - if the infection is
        resistant to it, do nothing, otherwise, kill the infection and all
        other resistances it included"""
        self.current_treatment = treatment_name
        # TODO: Make this not always work
        if not self.infection.is_resistant(treatment_name):
            self.recover_from_infection()

    def spread_infection(self, other):
        """Give the current infection to another person"""
        if not other.immune and self.infection.get_tier() > other.infection.get_tier():
            other.infection = deepcopy(self.infection)

    def die(self):
        """Make the person no longer alive"""
        self.alive = False

    def __repr__(self):
        """Provide a string representation for the person"""
        if self.immune:
            return "Immune person"
        elif self.infection is not None:
            return "Person {}".format(self.infection)
        return "Uninfected person"


class Model:
    def __init__(self, population=None, initial_infected=True):
        """Start the model with a population of defualt people, or a custom
        population provided as a parameter"""
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population
            # Give a member of the population a simple infection with no
            # resistances to any treatments
            if initial_infected:
                self.population[0].infection = Infection()

        # Store a separate list of dead people to avoid continual checking
        # for if a person is dead before operations
        self.dead = []

    def run(self):
        """Simulate a number of timesteps within the model"""
        for i in range(NUM_TIMESTEPS):

            # Report how far through the run when a multiple of a set percentage
            # of steps are completed
            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10))

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
