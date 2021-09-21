#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
PROBABILITY_MOVE_UP_TREATMENT = 0.8
TIMESTEPS_MOVE_UP_LAG_TIME = 5
ISOLATION_THRESHOLD = 2
# Death (orange line in powerpoint)
PROBABILITY_DEATH = 0.01
# Spreading (grey line in powerpoint)
PROBABILITY_SPREAD = 1
NUM_SPREAD_TO = 1

# Whether our product is used in the simulation
# This changes how people are put into isolation. Normally, this is done when
# they are being treated for a resistance (i.e. expected to have it), but this
# does it based on whether they have it as an instantaneous test
PRODUCT_IN_USE = True
PROBABILIY_PRODUCT_DETECT = 0.5
PRODUCT_DETECTION_LEVEL = ISOLATION_THRESHOLD


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
RESISTANCE_NAMES = [str(i+1) for i in range(NUM_RESISTANCE_TYPES)]


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
    def __init__(self, drug=RESISTANCE_NAMES[0], time_treated=None):
        """Initialise a treatment within the model"""
        self.drug = drug
        if time_treated is not None:
            self.time_treated = time_treated
        else:
            self.time_treated = 0

    def next_treatment(self):
        """Move up the treatment to the next strongest drug, and reset the
        amout of time that it has been used to zero"""
        drug_index = RESISTANCE_NAMES.index(self.drug)
        if drug_index < NUM_RESISTANCE_TYPES - 1:
            self.drug = RESISTANCE_NAMES[drug_index + 1]
            self.time_treated = 0

    def treats_infection(self, infection):
        """Return whether the treatment works on the infection given any
        resistances the infection may have"""
        return not infection.is_resistant(self.drug)

    def __repr__(self):
        if self.drug is not None:
            return "treated with drug {} for {} timesteps".format(
                                                self.drug, self.time_treated)
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
        """Initialise the model as having a population of people"""
        if population is None:
            self.population = [Person() for _ in range(POPULATION_SIZE)]
        else:
            self.population = population

        # Abstract away all the data handling into another class to avoid
        # cluttering up the model logic
        self.data_handler = DataHandler()

    def run(self):
        """Simulate a number of timesteps within the model"""

        # Make a new data handler for each simulation
        self.data_handler.__init__()

        # Repeat the simulation for a set number of timesteps
        for _ in range(NUM_TIMESTEPS):

            # For each person in the population
            for person in self.population:

                # Record the data throughout the model
                self.data_handler.record_person(person)

                # If the person is infected (we realistically would know this
                # by whether they are symptomatic)
                if person.infection is not None and person.alive:

                    # Move up in treatment class if needed
                    if person.treatment is None:
                        # If the person is infected but are not being treated
                        # with **anything**, start them on the lowest tier
                        # treatment (we can know that the person is infected,
                        # but not which tier they are on, without diagnostic
                        # tools, as we can see they are sick)
                        person.treatment = Treatment()
                    else:
                        # If the person has been treated for a number of
                        # consecutive days with the, a certain probability is
                        # exceeded, move them up a treatment tier
                        time_cond = person.treatment.time_treated > TIMESTEPS_MOVE_UP_LAG_TIME
                        rand_cond = decision(PROBABILITY_MOVE_UP_TREATMENT)
                        if time_cond and rand_cond:
                            person.increase_treatment()

                        if PRODUCT_IN_USE and decision(PROBABILIY_PRODUCT_DETECT):
                            # If the product is in use, and it detects the
                            # infection (which occurs a certain probability of
                            # the time) immediately isolate this with the
                            # resistance

                            # The product detects exclusively when at one level
                            # of resistance and no higher, but since the disease
                            # will develop resistance incrementally due to the
                            # tiered antibiotics, this should acheive all above
                            if person.infection.resistances[str(PRODUCT_DETECTION_LEVEL)]:
                                person.isolate()

                            # If the person is known to have a resistance that
                            # is higher than their treatment, increase their
                            # treatment
                            if person.treatment.drug < str(PRODUCT_DETECTION_LEVEL):
                                person.treatment.drug = str(PRODUCT_DETECTION_LEVEL)

                            # More verbose/slightly different implementation
                            """
                            for v in range(PRODUCT_DETECTION_LEVEL, NUM_RESISTANCE_TYPES):
                                if person.infection.resistances[str(v)]:
                                    person.isolate()
                                    break
                            """

                        if int(person.treatment.drug) >= ISOLATION_THRESHOLD:
                            # Isolate if in high enough treatment class (which
                            # is not the same as infection class - this will
                            # likely lag behind)
                            person.isolate()

                        # Increment the number of times a person has been
                        # treated with the drug
                        person.treatment.time_treated += 1


                    # Recovery generally or by treatment if currently infected
                    # (green line in powerpoint)
                    general_recovery = decision(PROBABILITY_GENERAL_RECOVERY)
                    treatment_recovery = (person.correct_treatment() and
                                        decision(PROBABILITY_TREATMENT_RECOVERY))
                    if general_recovery or treatment_recovery:
                        person.recover_from_infection()

                    # Mutation to higher resistance due to treatment
                    # (blue line in powerpoint)
                    if decision(PROBABILITY_MUTATION):
                        person.mutate_infection()

                    # Deaths due to infection
                    # (orange line in powerpoint)
                    if decision(PROBABILITY_DEATH):
                        person.die()

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

            # Update data recorded in this timestep, and output any according
            # to parameters indicating output format
            self.data_handler.process_timestep_data()

    def __repr__(self):
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
        self.ys_data = [[] for _ in range(4 + NUM_RESISTANCE_TYPES)]
        self.labels = (
            ["Infected"]
            + list(map(lambda x: "Resistance " + x, RESISTANCE_NAMES))
            + ["Dead", "Immune", "Uninfected"]
        )

        # Include isolations separately as they are a non-disjoint category
        self.non_disjoint = [[]]
        self.non_disjoint_labels = ["Isolated"]

        self.timestep = -1
        self._new_timestep_vars()

    def _new_timestep_vars(self):
        """Make some helper variables"""
        self.num_infected_stages = [0] * (NUM_RESISTANCE_TYPES + 1)
        self.num_dead = 0
        self.num_immune = 0
        self.num_uninfected = 0
        self.num_isolated = 0
        self.timestep += 1

    def record_person(self, person):
        """Record data about a person in the helper variables, so a whole
        statistic can be formed by running this function on every person in
        the population"""
        if person.immune:
            self.num_immune += 1
        elif not person.alive:
            self.num_dead += 1
        elif person.infection is None:
            self.num_uninfected += 1
        else:
            self.num_infected_stages[person.infection.get_tier() + 1] += 1

        # Non-disjoint categories
        if person.isolated:
            self.num_isolated += 1

    def _preprocess_disjoint_labels(self):
        """Preprocess the data and the labelling for some graph types"""
        # When as a line graph, we can draw lines for categories which
        # are not disjoint, as they needn't sum to a fixed value as with
        # the stacked plot. This means we sum up infections to include
        # all resistances above them (i.e. infection = i + r1 + r2 + r3,
        # resistance #1 = r1 + r2 + r3, resistance #2 = r2 + r3, etc.)
        # Furthemore, categories such as isolated which are just totally
        # disjoint can also be included
        if GRAPH_TYPE == "line":
            datas = []
            for i in range(NUM_RESISTANCE_TYPES + 1):
                datas.append(
                    [sum(x) for x in zip(*self.ys_data[i:-3])]
                )
            datas.extend(self.ys_data[-3:])
            datas.extend(self.non_disjoint)
            final_labels = self.labels + self.non_disjoint_labels
            return datas, final_labels
        return self.ys_data, self.labels

    def draw_full_graph(self):
        """Draw a graph of all of the data in the graph"""
        datas, final_labels = self._preprocess_disjoint_labels()
        DataRenderer.draw_full_graph(self.time, datas, final_labels)

    def _print_current_data(self):
        """Print the values of the current state of the simulation"""
        # TODO: Automate this from the disjoint and non-disjoint labels?
        print("uninfected: {}, immune: {}, dead: {}, infected: {}, isolated: {}".format(
            str(self.num_uninfected).ljust(OUTPUT_PADDING),
            str(self.num_immune).ljust(OUTPUT_PADDING),
            str(self.num_dead).ljust(OUTPUT_PADDING),
            "[" + ", ".join(map(
                lambda x: str(x).ljust(OUTPUT_PADDING),
                self.num_infected_stages
            )) + "]",
            str(self.num_isolated)
        ))

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
        for j, v in enumerate(self.num_infected_stages):
            self.ys_data[j].append(v)
        self.ys_data[-3].append(self.num_dead)
        self.ys_data[-2].append(self.num_immune)
        self.ys_data[-1].append(self.num_uninfected)
        self.non_disjoint[0].append(self.num_isolated)
        self.time.append(self.timestep)

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

    # Create a population with some initially infected people
    population = [Person() for _ in range(POPULATION_SIZE - 10)]
    for _ in range(10):
        population.append(Person(infection=Infection()))

    # Create and run the model
    m = Model(population=population)
    m.run()

    if not ANIMATE_GRAPH:
        # Finally show the full simulation graph
        m.data_handler.draw_full_graph()

    # Don't immediately close when the simulation is done
    input("Press any key to exit: ")
