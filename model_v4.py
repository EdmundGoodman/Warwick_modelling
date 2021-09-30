#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################
### Library imports for the model ###
#####################################

from random import seed, random, sample
from copy import deepcopy

###############################
### Change these parameters ###
###############################

# General parameters
NUM_TIMESTEPS = 20
POPULATION_SIZE = 250

# Ordered list of drugs used, their properties, and the properties of their
# resistant pathogens
DRUG_NAMES = ["Penicillin", "Amoxycillin",
                    "Carbopenamase", "Wonder drug"]

# Lookup table of drug properties by their names
DRUG_PROPERTIES = {}
DRUG_PROPERTIES["Penicillin"] = (
    0.2                     # Drug treatment recovery probability
)
DRUG_PROPERTIES["Amoxycillin"] = (0.2)
DRUG_PROPERTIES["Carbopenamase"] = (0.2)
DRUG_PROPERTIES["Wonder drug"] = (0.2)

# Lookup table of resistance properties by their names
NUM_RESISTANCES = len(DRUG_NAMES)
death_function = lambda p, t: round(min(0.0005*t + p, 1), 4)
RESISTANCE_PROPERTIES = {}
RESISTANCE_PROPERTIES["None"] = (
    0.01,                   # General recovery probability
    0.02,                   # Mutation probability
    # TODO: Make this more robust
    0.8,                    # Spread probability
    1,                      # Number of people spread to
    0.01,                   # Death probability
    death_function,         # Death function
)
RESISTANCE_PROPERTIES["Penicillin"] = (0.01, 0.02, 0.8, 1, 0.01, death_function)
RESISTANCE_PROPERTIES["Amoxycillin"] = (0.01, 0.02, 0.8, 1, 0.01, death_function)
RESISTANCE_PROPERTIES["Carbopenamase"] = (0.01, 0.02, 0.8, 1, 0.01, death_function)
RESISTANCE_PROPERTIES["Wonder drug"] = (0.01, 0.02, 0.8, 1, 0.01, death_function)


PROBABILITY_MOVE_UP_TREATMENT = 0.8
TIMESTEPS_MOVE_UP_LAG_TIME = 5
ISOLATION_THRESHOLD = "Carbopenamase"

PRODUCT_IN_USE = True
PROBABILIY_PRODUCT_DETECT = 1
PRODUCT_DETECTION_LEVEL = "Carbopenamase"

#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))
if REPORT_MOD_NUM < 1:
    REPORT_MOD_NUM = 1  # Don't try to report more than once per timestep

#######################################
### Objects and logic for the model ###
#######################################


class Infection:
    def __init__(self, resistance=None, time_treated=0):
        """Initialise an infection within the model"""
        if resistance is None:
            resistance="None"

        self.resistance = resistance
        self.general_recovery_probability = RESISTANCE_PROPERTIES[resistance][0]
        self.mutation_probability = RESISTANCE_PROPERTIES[resistance][1]
        self.spread_probability = RESISTANCE_PROPERTIES[resistance][2]
        self.num_spread_to = RESISTANCE_PROPERTIES[resistance][3]
        self.death_probability = RESISTANCE_PROPERTIES[resistance][4]

        self.time_treated = time_treated

    def make_resistant(self, resistance):
        """Give the infection a specified resistance"""
        self.__init__(resistance, self.time_treated)

    def is_resistant(self, resistance):
        """Return whether the infection has a specified resistance"""
        return self.get_tier() >= DRUG_NAMES.index(resistance)

    def get_tier(self):
        """Return how resistant the infection is - higher is more resistant"""
        return DRUG_NAMES.index(self.resistance)

    def __repr__(self):
        if self.resistance == "None":
            return "infected"
        else:
            return "infected with resistance up to: {}".format(self.resistance)


class Treatment:
    def __init__(self, drug=DRUG_NAMES[0], time_treated=None):
        """Initialise a treatment within the model"""
        self.drug = drug
        self.treatment_recovery_probability = DRUG_PROPERTIES[drug][0]

        if time_treated is not None:
            self.time_treated = time_treated
        else:
            self.time_treated = 0

    def next_treatment(self):
        """Move up the treatment to the next strongest drug, and reset the
        amount of time that it has been used to zero"""
        drug_index = DRUG_NAMES.index(self.drug)
        if drug_index < NUM_RESISTANCES - 1:
            self.__init__(DRUG_NAMES[drug_index + 1], self.time_treated)

    def treats_infection(self, infection):
        """Return whether the treatment works on the infection given any
        resistances the infection may have"""
        return not infection.is_resistant(self.drug)

    def __repr__(self):
        return "treated with drug {} for {} timesteps".format(
                self.drug, self.time_treated)


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
        if self.infection is not None and self.treatment is not None:
            self.infection.make_resistant(self.treatment.drug)

    def increase_treatment(self):
        """Move up the treatment by one"""
        if self.treatment is not None:
            self.treatment.next_treatment()

    def correct_treatment(self):
        """Return whether the current treatment is sufficient to overcome
        any resistances of the infection"""
        if self.treatment is not None:
            return self.treatment.treats_infection(self.infection)
        return False

    def spread_infection(self, other):
        print("unimplemented")

    def isolate(self):
        """Put the person in isolation"""
        self.isolated = True

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
            if self.treatment is not None:
                return "Person {} and {}".format(self.infection, self.treatment)
            else:
                return "Person {} and untreated".format(self.infection)
        return "Uninfected person"


class Model:
    def __init__(self, population=None):
        """Initialise the model as having a population of people"""
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population

    def run(self):
        """Simulate a number of timesteps within the model"""

        # Repeat the simulation for a set number of timesteps
        for _ in range(NUM_TIMESTEPS):

            # For each person in the population
            for person in self.population:
                print(person)


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
