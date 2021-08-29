#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from drawnow import drawnow

from random import seed, random, sample
from copy import deepcopy

###############################
### Change these parameters ###
###############################

# General parameters
NUM_TIMESTEPS = 50
POPULATION_SIZE = 5000
NUM_RESISTANCE_TYPES = 3

# Recovery generally or by treatment (green line in powerpoint)
PROBABILITY_GENERAL_RECOVERY = 0.01
PROBABILITY_TREATMENT_RECOVERY = 0.2
# Mutation to higher resistance due to treatment (blue line in powerpoint)
PROBABILITY_MUTATION = 0.02
PROBABILITY_MOVE_UP_TREATMENT = 0.2
ISOLATION_THRESHOLD = 2
# Death (orange line in powerpoint)
PROBABILITY_DEATH = 0.01
# Spreading (grey line in powerpoint)
PROBABILITY_SPREAD = 1
NUM_SPREAD_TO = 1


#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0
REPORT_PERCENTAGE = 5
ANIMATE_GRAPH = True
PRINT_DATA = False

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))
RESISTANCE_NAMES = [str(i+1) for i in range(NUM_RESISTANCE_TYPES)]
ISOLATION_THRESHOLD_DRUG = str(ISOLATION_THRESHOLD)


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
    def __init__(self, drug=RESISTANCE_NAMES[0]):
        """Initialise a treatment within the model"""
        self.drug = drug

    def next_treatment(self):
        """Move up the treatment to the next strongest drug"""
        drug_index = RESISTANCE_NAMES.index(self.drug)
        if drug_index < NUM_RESISTANCE_TYPES - 1:
            self.drug = RESISTANCE_NAMES[drug_index + 1]

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
        if self.infection is not None and self.treatment is not None:
            self.infection.make_resistant(self.treatment)

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
        """Give the current infection to another person, as long as they can
        receive it, don't already have a more resistant infection, and neither
        are isolated"""
        # Cannot spread if not already infected
        if self.infection is None:
            return None

        directional = (other.infection is None
                    or self.infection.get_tier() > other.infection.get_tier())
        susceptible = not other.immune and other.alive
        contactable = not self.isolated and not other.isolated
        if directional and susceptible and contactable:
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

        """# We also have some other lists to move people into to speed up
        # Store a separate list of dead people to avoid continual checking
        # for if a person is dead before operations
        self.dead = []
        self.immune = []"""

        # Store data throughout the simulation
        # [Uninfected, infected, resistance #1,... , resistance #2, immune]
        self.time = []
        self.ys_data = [[] for _ in range(3 + NUM_RESISTANCE_TYPES)]
        self.labels = (
            ["Uninfected", "Infected"]
            + list(map(lambda x: "Resistance " + x, RESISTANCE_NAMES))
            + ["Immune"]
        )


    def run(self):
        """Simulate a number of timesteps within the model"""

        for i in range(NUM_TIMESTEPS):

            # Report how far through the run when a multiple of a set percentage
            # of steps are completed
            if i % REPORT_MOD_NUM == 0:
                print("{}% complete".format(i / int(NUM_TIMESTEPS / 10) * 10))

            # Make some helper variables
            num_uninfected = 0
            num_immune = 0
            num_infected_stages = [0] * (NUM_RESISTANCE_TYPES + 1)

            # For each person in the population
            for person in self.population:

                #Record the data throughout the model
                if person.immune:
                    num_immune += 1
                elif person.infection is None:
                    num_uninfected += 1
                else:
                    num_infected_stages[person.infection.get_tier() + 1] += 1

                # If the person is infected (we realistically would know this
                # by whether they are symptomatic)
                if person.infection is not None:

                    # Move up in treatment class if needed
                    if person.treatment is None:
                        # If the person is infected but are not being treated
                        # with **anything**, start them on the lowest tier
                        # treatment
                         person.treatment = Treatment()
                    else:
                        # Sometimes move the person up to emulate them being
                        # treated increasingly aggressively if they have not
                        # recovered
                        # TODO: Make this dependent on diagnostic tools etc.
                        if decision(PROBABILITY_MOVE_UP_TREATMENT):
                            person.increase_treatment()

                        if person.treatment.drug >= ISOLATION_THRESHOLD_DRUG:
                            # Isolate if in high enough treatment class
                            person.isolate()

                    # Recovery generally or by treatment if currently infected
                    # (green line in powerpoint)
                    general_recovery = decision(PROBABILITY_GENERAL_RECOVERY)
                    treatment_recovery = (person.correct_treatment() and
                                    decision(PROBABILITY_TREATMENT_RECOVERY))
                    if general_recovery or treatment_recovery:
                        person.recover_from_infection()
                        """# Move them into the immune list to avoid extra processing
                        person_position = self.population.index(person)
                        self.immune.append(self.population.pop(person_position))
                        continue"""


                    # Mutation to higher resistance due to treatment
                    # (blue line in powerpoint)
                    if decision(PROBABILITY_MUTATION):
                        person.mutate_infection()

                    # Deaths due to infection
                    # (orange line in powerpoint)
                    if decision(PROBABILITY_DEATH):
                        person.die()
                        """# Move them into the dead list to avoid extra processing
                        person_position = self.population.index(person)
                        self.dead.append(self.population.pop(person_position))"""


            # Spread the infection strains throughout the population
            # We need a deepcopy operation, to prevent someone who has just
            # been spread to in this timestep spreading the thing they've
            # just received, so technically don't have yet
            # (grey line in powerpoint)
            updated_population = deepcopy(self.population)
            for person in self.population:
                if person.infection is not None and decision(PROBABILITY_SPREAD):
                    for receiver in sample(updated_population, NUM_SPREAD_TO):
                        person.spread_infection(receiver)
            self.population = updated_population[:]

            # Print the data
            if PRINT_DATA and i % REPORT_MOD_NUM == 0:
                print(num_immune, num_uninfected, num_infected_stages)

            # Add the data to the record of what's happened
            self.ys_data[0].append(num_uninfected)
            for j,v in enumerate(num_infected_stages):
                self.ys_data[j+1].append(v)
            self.ys_data[-1].append(num_immune)
            self.time.append(i)
            if ANIMATE_GRAPH:
                # Draw a stacked plot of what's going on
                drawnow( lambda: plt.stackplot(self.time, *self.ys_data, labels=m.labels) )

        if ANIMATE_GRAPH:
            # Add a legend and axis labels (cannot be done during animation)
            plt.legend(loc='upper right')
            plt.xlabel("Time / timesteps")
            plt.ylabel("Infections / %")


    def __repr__(self):
        return "Model"


def decision(probability):
    """Get a boolean value with a given probability"""
    return random() < probability


if __name__ == "__main__":
    # Seed the random number generator
    if RANDOM_SEED is not None:
        seed(RANDOM_SEED)

    # Enable interactivity in matplotlib figures
    plt.ion()

    # Create a population with some initially infected people
    population = [Person() for _ in range(POPULATION_SIZE - 10)]
    for _ in range(10):
        population.append(Person(infection=Infection()))

    # Create and run the model
    m = Model(population=population)
    m.run()

    if not ANIMATE_GRAPH:
        # Finally show the full simulation graph
        print(m.ys_data)
        plt.stackplot(m.time, *m.ys_data, labels=m.labels)
        plt.legend(loc='upper right')
        plt.xlabel("Time / timesteps")
        plt.ylabel("Infections / %")
        plt.show()

    # Don't immediately close when the simulation is done
    input("Press enter to exit: ")
