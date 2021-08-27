#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from random import seed, random
from copy import deepcopy

###############################
### Change these parameters ###
###############################

# General parameters
NUM_TIMESTEPS = 500
POPULATION_SIZE = 5000
NUM_RESISTANCE_TYPES = 3

# Recovery generally or by treatment (green line in powerpoint)
PROBABILITY_GENERAL_RECOVERY = 0.01
PROBABILITY_TREATMENT_RECOVERY = 0.2
# Mutation to higher resistance due to treatment (blue line in powerpoint)
PROBABILITY_MUTATION = 0.02
PROBABILITY_MOVE_UP_TREATMENT = 0.2
# Death (orange line in powerpoint)
PROBABILITY_DEATH = 0.01
# Spreading (grey line in powerpoint)
PROBABILITY_SPREAD = 1
NUM_SPREAD_TO = 2


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
        """Give the infection a specified resistance"""
        self.resistances[resistance] = True

    def is_resistant(self, resistance):
        """Return whether the infection has a specified resistance"""
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
        resistances_string = self.get_resistances_string()
        if resistances_string == "#":
            return "infected"
        return "infected with resistances: {}".format(resistances_string)


class Treatment:
    def __init__(self, drug=None):
        """Initialise a treatment within the model"""
        self.drug = drug

    def treats_infection(self, infection):
        """Return whether the treatment works on the infection given any
        resistances the infection may have"""
        return not infection.is_resistant(self.drug)

    def __repr__(self):
        if self.drug is not None:
            return "treated with drug: {}".format(self.drug)
        return "untreated"


class Person:
    def __init__(self, infection=None, treatment=None, isolated=False, immune=False):
        """Initialise a person as having various properties within the model"""
        self.infection = infection
        self.treatment = treatment

        self.isolated = isolated
        self.immune = immune
        self.alive = True

    def recover_from_infection(self):
        """Recover the person, returning them to their default state; totally
        uninfected with no resistances, but now immune to the infection -
        irrespective of any resistances it has"""
        self.__init__(immune=True)

    def mutate_infection(self):
        """Make the infection become resistant to the treatment with a given
        probability of occurring"""
        if self.infection is not None and self.current_treatment is not None:
            self.infection.make_resistant(self.current_treatment)

    def cure_infection(self):
        """Cure the infection with an treatment - if the infection is
        resistant to it, do nothing, otherwise, kill the infection and all
        other resistances it included"""
        if self.current_treatment is not None and not self.infection.is_resistant(self.current_treatment):
            self.recover_from_infection()

    def spread_infection(self, other):
        """Give the current infection to another person, as long as they can
        receive it, don't already have a more resistant infection, and neither
        are isolated"""
        susceptible = not other.immune and other.alive
        directional = self.infection.get_tier() > other.infection.get_tier()
        contactable = not self.isolated and not other.isolated
        if susceptible and directional and contactable:
            other.infection = deepcopy(self.infection)

    def isolate(self):
        """Put the person in isolation"""
        self.isolated = True

    def deisolate(self):
        """Take the person out of isolation"""
        self.isolated = False

    def die(self):
        """Make the person no longer alive"""
        self.alive = False

    def __repr__(self):
        """Provide a string representation for the person"""
        if not self.alive:
            return "Dead person"
        elif self.immune:
            return "Immune person"
        elif self.infection is not None:
            return "Person {} and {}".format(self.infection, self.treatment)
        return "Uninfected person"


class Model:
    def __init__(self, population=None):
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population

        # We also have some other lists to move people into to speed up
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

            # For each person in the population
            for person in self.population:

                # Recovery generally or by treatment
                # (green line in powerpoint)

                # Mutation to higher resistance due to treatment
                # (blue line in powerpoint)

                # Moving up in treatment class

                # Isolate if in high enough treatment class

                # Deaths due to infection
                # (orange line in powerpoint)

                pass

            # Spread within population
            # (grey line in powerpoint)


    def __repr__(self):
        return "Model"


def decision(probability):
    """Get a boolean value with a given probability"""
    return random() < probability


if __name__ == "__main__":
    # Seed the random number generator
    if RANDOM_SEED is not None:
        seed(RANDOM_SEED)

    # Create a population with some initially infected people
    population = [Person() for _ in range(POPULATION_SIZE - 10)]
    for _ in range(10):
        population.append(Person(infection=Infection()))

    # Create and run the model
    m = Model(population=population)
    m.run()
