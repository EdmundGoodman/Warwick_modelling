#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from random import choice, sample, random, seed
from itertools import combinations
from copy import deepcopy


###############################
### Change these parameters ###
###############################

NUM_TIMESTEPS = 100
NUM_RESISTANCE_TYPES = 3
POPULATION_SIZE = 5000
PROBABILITY_MUTATION = 0.05
PROBABILITY_GENERAL_RECOVERY = 0.01
PROBABILITY_SPREAD = 1
NUM_SPREAD_TO = 5


#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))
RESISTANCE_NAMES = [str(i+1) for i in range(NUM_RESISTANCE_TYPES)]
RESISTANCE_COMBINATIONS = []
for i in reversed(range(len(RESISTANCE_NAMES))):
    RESISTANCE_COMBINATIONS.extend([",".join(map(str,j))
                            for j in combinations(RESISTANCE_NAMES, i+1)])
RESISTANCE_COMBINATIONS.append("#")


#######################################
### Objects and logic for the model ###
#######################################

class Person:
    def __init__(self):
        """Everybody starts uninfected with no resistant strains in the model"""
        self.infected = False
        self.resistances = {resistance: False for resistance in RESISTANCE_NAMES}

    def mutate_infections(self):
        """Make a person resistant to each antibiotic with a very probability"""
        for resistance in RESISTANCE_NAMES:
            if decision(PROBABILITY_MUTATION):
                self.infected = True
                self.resistances[resistance] = True

    def recover_from_infection(self):
        """Recover the person, returning them to their default state: totally
        uninfected with no resistances"""
        self.__init__()

    def treat_infection(self, antibiotic_name):
        """Treat the infection with an antibiotic - if the infection is
        resistant to it, do nothing, otherwise, kill the infection and all
        other resistances it included"""
        if self.resistances[antibiotic_name] == False:
            self.recover_from_infection()

    def spread_infection(self, other):
        """Give any present resistant strains from the current object to the
        other object"""
        for resistance, present in self.resistances.items():
            if present:
                other.resistances[resistance] = True

    def get_resistances_name(self):
        """Get a canonical name for the present resistances"""
        string = ",".join([k for k, v in self.resistances.items() if v])
        if string == "":
            return "#"
        return string

    def __repr__(self):
        """Return a string representation of the class"""
        if self.infected:
            return "Infected with {}".format(self.get_resistances_name())
        return "Not infected"


class Model:
    def __init__(self, population=None):
        """Start the model with a population of uninfected people, or a custom
        population provided as a parameter"""
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population

        # Store data about percentage resistance of each combination of
        # resistances throughout the model run
        self.x_data = range(NUM_TIMESTEPS)
        self.ys_data = [[0] * NUM_TIMESTEPS for _ in range(2 ** NUM_RESISTANCE_TYPES)]

    def run(self):
        """Simulate a number of timesteps within the model"""
        for i in range(NUM_TIMESTEPS):

            # Report how far through the run when a multiple of a set percentage
            # of steps are completed
            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10) )

            # Record data about the proportions of strains prevalence within
            # the population
            infection_percentages = self.get_infection_percentages().values()
            for j,data_point in enumerate(infection_percentages):
                self.ys_data[j][i] = data_point

            # For each person in the population
            for person in self.population:
                # Allow for recovery from their infection
                if decision(PROBABILITY_GENERAL_RECOVERY):
                    person.recover_from_infection()

                # Allow for mutation to a resistant strain
                if decision(PROBABILITY_MUTATION):
                    person.mutate_infections()

                # Treat with a random antibiotic (which are named the same
                # as the strains which are resistant to them)
                if person.infected:
                    antibiotic = choice(RESISTANCE_NAMES)
                    person.treat_infection(antibiotic)

            # Spread the infection strains throughout the population
            # We need a deepcopy operation, to prevent someone who has just
            # been spread to in this timestep spreading that thing they've
            # just received, so technically don't have yet
            updated_population = deepcopy(self.population)
            for person in self.population:
                if person.infected and decision(PROBABILITY_SPREAD):
                    for receiver in sample(updated_population, NUM_SPREAD_TO):
                        person.spread_infection(receiver)
            self.population = updated_population[:]

        print("Done!")

    def get_infection_percentages(self):
        """Get the percentage infected with each type of bacteria"""
        infections = {name:0 for name in RESISTANCE_COMBINATIONS}
        for person in self.population:
            infections[person.get_resistances_name()] += 1
        return {infection: (float(number) / POPULATION_SIZE) * 100
                                    for infection,number in infections.items()}

    def __repr__(self):
        """Return a string encoding the percentage of people infected by
        each anti-biotic resistant bacteria"""
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
    plt.stackplot(m.x_data, *m.ys_data, labels=RESISTANCE_COMBINATIONS)
    plt.legend(loc='upper right')
    plt.xlabel("Time / timesteps")
    plt.ylabel("Infections / %")
    plt.show()
