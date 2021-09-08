#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################
### Change these parameters ###
###############################

NUM_TIMESTEPS = 500
POPULATION_SIZE = 5000


#################################################
### Internal parameters and derived constants ###
#################################################

RANDOM_SEED = 0

REPORT_PROGRESS = True
REPORT_PERCENTAGE = 5
PRINT_DATA = True
ANIMATE_GRAPH = False
GRAPH_TYPE = "line"  # line, stackplot (default)
OUTPUT_PADDING = len(str(POPULATION_SIZE))

REPORT_MOD_NUM = int(NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))


#####################################
### Library imports for the model ###
#####################################

from copy import deepcopy
from random import seed, random, sample
import matplotlib.pyplot as plt

# Only import the niche drawnow library if it is needed, to allow use even if
# someone cannot install it, just with fewer features
if ANIMATE_GRAPH:
    from drawnow import drawnow


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


###############################################
### Data handler and renderer for the model ###
###############################################

class DataHandler:
    def __init__(self):
        """Initialise the data handler for the model as storing data
        in an appropriate structure"""
        self.time = []
        # [infected, resistance #1,.. , resistance #2, dead, immune, uninfected]
        self.ys_data = [[] for _ in range(0)] # TODO
        self.labels = []

        # Include isolations separately as they are a non-disjoint category
        self.non_disjoint = [[]]
        self.non_disjoint_labels = []

        self.timestep = -1
        self._new_timestep_vars()

    def _new_timestep_vars(self):
        """Make some helper variables"""
        # TODO
        self.timestep += 1

    def record_person(self, person):
        """Record data about a person in the helper variables, so a whole
        statistic can be formed by running this function on every person in
        the population"""
        # TODO

        # Non-disjoint categories
        # TODO

    def _preprocess_disjoint_labels(self):
        """Preprocess the data and the labelling for some graph types"""
        if GRAPH_TYPE == "line":
            # TODO
            pass
        return self.ys_data, self.labels

    def draw_full_graph(self):
        """Draw a graph of all of the data in the graph"""
        datas, final_labels = self._preprocess_disjoint_labels()
        DataRenderer.draw_full_graph(self.time, datas, final_labels)

    def _print_current_data(self):
        """Print the values of the current state of the simulation"""
        # TODO
        print()

    def _report_model_state(self):
        """Report the model's state through any mechanism set in parameters"""
        if self.timestep % REPORT_MOD_NUM == 0:
            if REPORT_PROGRESS and not PRINT_DATA:
                print("{}% complete".format(int(
                    self.timestep / int(NUM_TIMESTEPS / 10) * 10
                )))

            if PRINT_DATA:
                if REPORT_PROGRESS:
                    # Display it on the same line for ease of reading
                    print("{}% complete".format(str(int(
                        self.timestep / int(NUM_TIMESTEPS / 10) * 10
                    )).ljust(2)), end=" - ")
                self._print_current_data()

        if ANIMATE_GRAPH:
            datas, final_labels = self._preprocess_disjoint_labels()
            DataRenderer.animate_current_graph(self.time, datas, final_labels)

    def process_timestep_data(self):
        """Store the current timestep's data into the appropriate data
        structures"""
        # TODO

        # Report the model's state through any mechanism set in parameters
        self._report_model_state()

        # Reset the helper variables
        self._new_timestep_vars()


class DataRenderer:
    @staticmethod
    def _draw_graph(time, ys_data, labels):
        """Actually draw the graph via matplotlib"""
        if GRAPH_TYPE == "line":
            # line graph
            for i in range(len(ys_data)):
                plt.plot(time, ys_data[i], label=labels[i])
        else:
            # stackplot as default
            plt.stackplot(time, *ys_data, labels=labels)

    @staticmethod
    def _graph_settings():
        """Add settings for the graph, e.g. axis labels and legend"""
        plt.title('Resistance simulation')
        plt.legend(loc='upper right')
        plt.xlabel("Time / timesteps")
        plt.ylabel("# People")

    @staticmethod
    def draw_full_graph(time, ys_data, labels):
        """Draw and show the graph with all the data and legend once"""
        DataRenderer._draw_graph(time, ys_data, labels)
        DataRenderer._graph_settings()
        plt.show()

    @staticmethod
    def animate_current_graph(time, ys_data, labels):
        """Draw a graph up to the current state of the simulation"""
        drawnow(lambda: DataRenderer._draw_graph(time, ys_data, labels))


if __name__ == "__main__":
    # Seed the random number generator
    if RANDOM_SEED is not None:
        seed(RANDOM_SEED)

    # Enable interactivity in matplotlib figures
    plt.ion()

    # Create and run the model
    m = Model()
    m.run()

    if not ANIMATE_GRAPH:
        # Finally show the full simulation graph
        m.data_handler.draw_full_graph()

    # Don't immediately close when the simulation is done
    input("Press any key to exit: ")
