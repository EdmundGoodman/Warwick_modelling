#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import seed, random, sample
import matplotlib.pyplot as plt
import pandas as pd

###############################
### Change these parameters ###
###############################


class Params:
    # General model parameters
    NUM_TIMESTEPS = 100
    POPULATION_SIZE = 7500
    INITIALLY_INFECTED = 10

    # Ordered list of drugs used, their properties, and the properties of their
    # resistant pathogens
    DRUG_NAMES = ["Penicillin", "Carbapenemase", "Colistin"]

    PROBABILITY_MOVE_UP_TREATMENT = 0.2
    TIMESTEPS_MOVE_UP_LAG_TIME = 5
    ISOLATION_THRESHOLD = DRUG_NAMES.index("Colistin")

    PRODUCT_IN_USE = True
    PROBABILIY_PRODUCT_DETECT = 1
    PRODUCT_DETECTION_LEVEL = DRUG_NAMES.index("Carbapenemase")

    ############################################################
    # Use these if you want to set all drugs to the same thing #
    ############################################################

    PROBABILITY_GENERAL_RECOVERY = 0
    PROBABILITY_TREATMENT_RECOVERY = 0.3
    PROBABILITY_MUTATION = 0.25
    PROBABILITY_DEATH = 0.015
    # Add time infected into consideration for death chance
    DEATH_FUNCTION = lambda p, t: round(min(0.001*t + p, 1), 4)
    PROBABILITY_SPREAD = 0.25
    NUM_SPREAD_TO = 1

    @staticmethod
    def reset_granular_parameters():
        ###########################################################################
        # Set these explicitly for more granular control, or use the above to set #
        # them all as a group                                                     #
        ###########################################################################

        # Lookup table of drug properties by their names
        Params.DRUG_PROPERTIES = {}
        Params.DRUG_PROPERTIES["Penicillin"] = (
            Params.PROBABILITY_TREATMENT_RECOVERY,
        )
        Params.DRUG_PROPERTIES["Carbapenemase"] = (
            Params.PROBABILITY_TREATMENT_RECOVERY,
        )
        Params.DRUG_PROPERTIES["Colistin"] = (
            Params.PROBABILITY_TREATMENT_RECOVERY,
        )

        # Lookup table of resistance properties by their names
        Params.NUM_RESISTANCES = len(Params.DRUG_NAMES)
        Params.RESISTANCE_PROPERTIES = {}
        Params.RESISTANCE_PROPERTIES["None"] = (
            Params.PROBABILITY_GENERAL_RECOVERY, Params.PROBABILITY_MUTATION,
            Params.PROBABILITY_SPREAD, Params.NUM_SPREAD_TO,
            Params.PROBABILITY_DEATH, Params.DEATH_FUNCTION,
        )
        Params.RESISTANCE_PROPERTIES["Penicillin"] = (
            Params.PROBABILITY_GENERAL_RECOVERY, Params.PROBABILITY_MUTATION,
            Params.PROBABILITY_SPREAD, Params.NUM_SPREAD_TO,
            Params.PROBABILITY_DEATH, Params.DEATH_FUNCTION,
        )
        Params.RESISTANCE_PROPERTIES["Carbapenemase"] = (
            Params.PROBABILITY_GENERAL_RECOVERY, Params.PROBABILITY_MUTATION,
            Params.PROBABILITY_SPREAD, Params.NUM_SPREAD_TO,
            Params.PROBABILITY_DEATH, Params.DEATH_FUNCTION,
        )
        Params.RESISTANCE_PROPERTIES["Colistin"] = (
            Params.PROBABILITY_GENERAL_RECOVERY, Params.PROBABILITY_MUTATION,
            Params.PROBABILITY_SPREAD, Params.NUM_SPREAD_TO,
            Params.PROBABILITY_DEATH, Params.DEATH_FUNCTION,
        )


# Set the granular parameters from the generic ones
Params.reset_granular_parameters()


#########################
### Internal settings ###
#########################

class Settings:
    RANDOM_SEED = 0

    REPORT_PROGRESS = True
    REPORT_PERCENTAGE = 5
    REPORT_MOD_NUM = None  # Ensure scope
    if REPORT_PERCENTAGE is not None:
        REPORT_MOD_NUM = int(Params.NUM_TIMESTEPS / (100/REPORT_PERCENTAGE))
        # Don't try to report more than once per timestep
        if REPORT_MOD_NUM < 1:
            REPORT_MOD_NUM = 1
    PRINT_DATA = True
    OUTPUT_PADDING = len(str(Params.POPULATION_SIZE))

    DRAW_GRAPH = True
    GRAPH_TYPE = "line" # line, stackplot (default)
    EXPORT_TO_EXCEL = False
    DEFAULT_EXCEL_FILENAME = "out.xlsx"


#######################################
### Objects and logic for the model ###
#######################################

class Infection:
    def __init__(self, resistance=None, time_treated=0):
        """Initialise an infection within the model"""
        if resistance is None:
            resistance = "None"

        self.resistance = resistance
        self.general_recovery_probability = Params.RESISTANCE_PROPERTIES[resistance][0]
        self.mutation_probability = Params.RESISTANCE_PROPERTIES[resistance][1]
        self.spread_probability = Params.RESISTANCE_PROPERTIES[resistance][2]
        self.num_spread_to = Params.RESISTANCE_PROPERTIES[resistance][3]
        self.death_probability = Params.RESISTANCE_PROPERTIES[resistance][4]
        self.death_function = Params.RESISTANCE_PROPERTIES[resistance][5]

        self.time_treated = time_treated

    def make_resistant(self, resistance):
        """Give the infection a specified resistance"""
        self.__init__(resistance, self.time_treated)

    def is_resistant(self, resistance):
        """Return whether the infection has a specified resistance"""
        return self.get_tier() >= Infection.get_tier_from_resistance(resistance)

    def get_tier(self):
        """Return how resistant the infection is - higher is more resistant"""
        return Infection.get_tier_from_resistance(self.resistance)

    @staticmethod
    def get_tier_from_resistance(resistance):
        """Return an integer ordering of resistances - higher is more resistant"""
        if resistance == "None":
            return -1
        else:
            return Params.DRUG_NAMES.index(resistance)

    def duplicate(self):
        """Return a duplicate object of the current infection"""
        return Infection(self.resistance, self.time_treated)

    def __repr__(self):
        if self.resistance == "None":
            return "infected"
        else:
            return "infected with resistance up to: {}".format(self.resistance)


class Treatment:
    def __init__(self, drug=Params.DRUG_NAMES[0], time_treated=None):
        """Initialise a treatment within the model"""
        self.drug = drug
        self.treatment_recovery_probability = Params.DRUG_PROPERTIES[drug][0]

        if time_treated is not None:
            self.time_treated = time_treated
        else:
            self.time_treated = 0

    def next_treatment(self):
        """Move up the treatment to the next strongest drug, and reset the
        amount of time that it has been used to zero"""
        drug_index = Params.DRUG_NAMES.index(self.drug)
        if drug_index < Params.NUM_RESISTANCES - 1:
            self.__init__(Params.DRUG_NAMES[drug_index + 1], self.time_treated)

    def treats_infection(self, infection):
        """Return whether the treatment works on the infection given any
        resistances the infection may have"""
        return not infection.is_resistant(self.drug)

    def duplicate(self):
        """Return a duplicate object of the current treatment"""
        return Treatment(self.drug, self.time_treated)

    def __repr__(self):
        return "treated with drug {} for {} timesteps".format(self.drug, self.time_treated)


class Person:
    def __init__(self, infection=None, treatment=None, isolated=False, immune=False, time_infected=0, alive=True):
        """Initialise a person as having various properties within the model"""
        self.infection = infection
        self.treatment = treatment

        self.isolated = isolated
        self.immune = immune
        self.time_infected = time_infected
        self.alive = alive

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

    def try_spread_infection(self, population):
        """Give the current infection to another person, as long as they can
        receive it (susceptible), don't already have a more resistant infection
        (directional), and neither are isolated (contactable)"""
        if self.infection is not None and decision(self.infection.spread_probability):
            for receiver in sample(population, self.infection.num_spread_to):
                directional = (receiver.infection is None
                    or self.infection.get_tier() > receiver.infection.get_tier())
                susceptible = not receiver.immune and receiver.alive
                contactable = not self.isolated and not receiver.isolated
                if directional and susceptible and contactable:
                    receiver.infection = Infection(self.infection.resistance)

    def isolate(self):
        """Put the person in isolation"""
        self.isolated = True

    def die(self):
        """Make the person no longer alive"""
        self.__init__(alive=False)

    def duplicate(self):
        """Return a duplicate object of the current person, including
        duplicates of their infections and treatments"""
        return Person(
            None if self.infection is None else self.infection.duplicate(),
            None if self.treatment is None else self.treatment.duplicate(),
            self.isolated,
            self.immune,
            self.time_infected,
            self.alive,
        )

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
            # Make a default population as having a set number of initially
            # infected people
            num_intially_uninfected = Params.POPULATION_SIZE - Params.INITIALLY_INFECTED
            population = [Person() for _ in range(num_intially_uninfected)]
            for _ in range(Params.INITIALLY_INFECTED):
                population.append(Person(infection=Infection()))
        self.population = population

        # Abstract away all the data handling into another class to avoid
        # cluttering up the model logic
        self.data_handler = DataHandler()

    def run(self):
        """Simulate a number of timesteps within the model"""

        # Repeat the simulation for a set number of timesteps
        for _ in range(Params.NUM_TIMESTEPS):

            # For each person in the population
            for person in self.population:

                # Record the data throughout the model
                self.data_handler.record_person(person)

                # If the person is dead, they will not change state
                if not person.alive:
                    continue

                # If the person is infected, apply appropriate state changes
                if person.infection is not None:

                    """Handle increasing treatment"""
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
                        time_cond = person.treatment.time_treated > Params.TIMESTEPS_MOVE_UP_LAG_TIME
                        rand_cond = decision(Params.PROBABILITY_MOVE_UP_TREATMENT)
                        if time_cond and rand_cond:
                            person.increase_treatment()

                    """Handle isolation"""
                    # Isolate if in high enough treatment class (which
                    # is not the same as infection class - this will
                    # likely lag behind)
                    treatment_tier = Infection.get_tier_from_resistance(person.treatment.drug)
                    if treatment_tier >= Params.ISOLATION_THRESHOLD:
                        person.isolate()

                    """Handle use of the product"""
                    if person.infection.get_tier() >= Params.PRODUCT_DETECTION_LEVEL:
                        if Params.PRODUCT_IN_USE and decision(Params.PROBABILIY_PRODUCT_DETECT):
                            # Put people into isolation if our product detects
                            # them as being infected
                            person.isolate()

                            # If a person has the detected infection, put them on
                            # a treatment course for it, (i.e. only ever change
                            # it up to one above)
                            if Params.DRUG_NAMES.index(person.treatment.drug) <= Params.PRODUCT_DETECTION_LEVEL:
                                person.treatment = Treatment(Params.DRUG_NAMES[Params.PRODUCT_DETECTION_LEVEL+1])

                    """Handle Recovery generally or by treatment if currently infected"""
                    general_recovery = decision(person.infection.general_recovery_probability)
                    treatment_recovery = (person.correct_treatment() and
                                          decision(person.treatment.treatment_recovery_probability))
                    if general_recovery or treatment_recovery:
                        person.recover_from_infection()
                        # Don't do anything else, as infection/treatment will
                        # now be set to None
                        continue

                    """Handle Mutation to higher resistance due to treatment"""
                    if decision(person.infection.mutation_probability):
                        person.mutate_infection()

                    """Handle deaths due to infection"""
                    death_probability = person.infection.death_function(
                        person.infection.death_probability,
                        person.time_infected
                    )
                    if decision(death_probability):
                        person.die()
                        # Don't do anything else, as infection/treatment will
                        # now be set to None
                        continue

                    """Handle agent state about timesteps"""
                    # Increment the of timesteps a person has had the infection
                    person.time_infected += 1
                    # Increment the number of timesteps a person has been
                    # treated with the drug (treatment will always not be
                    # None by this point)
                    person.treatment.time_treated += 1

            """Handle infection spread through the population"""
            # We need a deepcopy operation, to prevent someone who has just
            # been spread to in this timestep spreading the thing they've
            # just received, so technically don't have yet
            updated_population = [p.duplicate() for p in self.population]
            for person in self.population:
                # `updated_population` is passed by reference, since it is
                # a list, so we can mutate it's state in different functions
                # and don't need to pass it back
                person.try_spread_infection(updated_population)
            self.population = updated_population[:]

            # updated_population data recorded in this timestep, and output any according
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
        self.ys_data = [[] for _ in range(4 + Params.NUM_RESISTANCES)]
        self.labels = (
            ["Infected"]
            + list(map(lambda x: "Resistance to " + x, Params.DRUG_NAMES))
            + ["Dead", "Immune", "Uninfected"]
        )

        # Include isolations separately as they are a non-disjoint category
        self.non_disjoint = [[]]
        self.non_disjoint_labels = ["Isolated"]

        self.timestep = -1
        self._new_timestep_vars()

    def get_infected_data(self):
        """Return the data about infections across all timesteps. Indices give
        0=no resistance, 1=resistance level 1, etc."""
        return self.ys_data[0:Params.NUM_RESISTANCES+1]

    def get_death_data(self):
        """Return the data about deaths across all timesteps"""
        return self.ys_data[-3]

    def get_immune_data(self):
        """Return the data about immune people across all timesteps"""
        return self.ys_data[-2]

    def get_uninfected_data(self):
        """Return the data about uninfected people across all timesteps"""
        return self.ys_data[-1]

    def get_isolated_data(self):
        """Return the data about isolated people across all timesteps"""
        return self.non_disjoint[0]

    def _new_timestep_vars(self):
        """Make some helper variables"""
        self.num_infected_stages = [0] * (Params.NUM_RESISTANCES + 1)
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

    def _preprocess_disjoint_labels(self):
        """Preprocess the data and the labelling for some graph types"""
        # When as a line graph, we can draw lines for categories which
        # are not disjoint, as they needn't sum to a fixed value as with
        # the stacked plot. This means we sum up infections to include
        # all resistances above them (i.e. infection = i + r1 + r2 + r3,
        # resistance #1 = r1 + r2 + r3, resistance #2 = r2 + r3, etc.)
        # Furthemore, categories such as isolated which are just totally
        # disjoint can also be included
        if Settings.GRAPH_TYPE == "line":
            datas = []
            for i in range(Params.NUM_RESISTANCES + 1):
                datas.append(
                    [sum(x) for x in zip(*self.ys_data[i:-3])]
                )
            datas.extend(self.ys_data[-3:])
            datas.extend(self.non_disjoint)
            final_labels = self.labels + self.non_disjoint_labels
            return datas, final_labels
        return self.ys_data, self.labels

    def _print_current_data(self):
        """Print the values of the current state of the simulation"""
        print("uninfected: {}, immune: {}, dead: {}, infected: {}, isolated: {}".format(
            str(self.num_uninfected).ljust(Settings.OUTPUT_PADDING),
            str(self.num_immune).ljust(Settings.OUTPUT_PADDING),
            str(self.num_dead).ljust(Settings.OUTPUT_PADDING),
            "[" + ", ".join(map(
                lambda x: str(x).ljust(Settings.OUTPUT_PADDING),
                self.num_infected_stages
            )) + "]",
            str(self.num_isolated)
        ))

    def _print_current_progress(self, end="\n", ljust=None):
        """Output the current progress of the model"""
        out = "{}% complete".format(str(int(self.timestep / int(Params.NUM_TIMESTEPS / 10) * 10)))
        if ljust is not None:
            out = out.ljust(ljust)
        print(out, end=end)

    def _report_model_state(self):
        """Report the model's state through any mechanism set in parameters"""
        if Settings.REPORT_MOD_NUM is None or self.timestep % Settings.REPORT_MOD_NUM == 0:
            # Print how far through the model run we are
            if Settings.REPORT_PROGRESS and not Settings.PRINT_DATA:
                self._print_current_progress()

            # Print both how far through, and the current state of the model
            if Settings.PRINT_DATA:
                if Settings.REPORT_PROGRESS:
                    # Display it on the same line for ease of reading
                    self._print_current_progress(end=" - ", ljust=2)
                self._print_current_data()

    def draw_full_graph(self):
        """Draw a graph of all of the data in the graph"""
        datas, final_labels = self._preprocess_disjoint_labels()
        DataRenderer.draw_full_graph(self.time, datas, final_labels)

    def export_to_excel(self, filename):
        """Export all the data to an excel file"""
        datas, final_labels = self._preprocess_disjoint_labels()
        DataRenderer.export_to_excel(filename, datas, final_labels)


class DataRenderer:
    @staticmethod
    def _draw_graph(time, ys_data, labels):
        """Actually draw the graph via matplotlib"""
        # matplotlib plots require: x_axis_data, y_axis_data(s), data labels

        if Settings.GRAPH_TYPE == "line":
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
        plt.figure()
        DataRenderer._draw_graph(time, ys_data, labels)
        DataRenderer._graph_settings()
        plt.show()

    @staticmethod
    def export_to_dataframe(ys_data, labels):
        """Turn the datahandler data into a dataframe"""
        df = pd.DataFrame()
        for i in range(len(ys_data)):
            df[labels[i]] = ys_data[i]
        return df

    @staticmethod
    def export_to_excel(filename, ys_data, labels):
        """Export the datahandler data into an excel sheet"""
        df = DataRenderer.export_to_dataframe(ys_data, labels)
        writer = pd.ExcelWriter(filename)
        df.to_excel(writer)
        writer.save()


def run():
    """Run the model with a given set of parameters"""
    # Seed the random number generator
    if Settings.RANDOM_SEED is not None:
        seed(Settings.RANDOM_SEED)

    # Create and run the model
    m = Model()
    m.run()
    return m


def run_and_output(excel_filename=None):
    """Wrapper on run, displaying and writing the output for the user"""
    # Run the model
    m = run()
    print()

    # Export the finished model to an excel file
    if Settings.EXPORT_TO_EXCEL:
        if excel_filename is None:
            excel_filename = Settings.DEFAULT_EXCEL_FILENAME
        m.data_handler.export_to_excel(excel_filename)

    # Finally show the full simulation graph
    if Settings.DRAW_GRAPH:
        m.data_handler.draw_full_graph()


if __name__ == "__main__":
    # Make the matplotlib graphs interactive
    plt.ion()

    # Run the model with and without the product
    print("With product:")
    run_and_output("withProduct.xlsx")  # Figure 1
    Params.PRODUCT_IN_USE = False
    print("Without product:")
    run_and_output("withoutProduct.xlsx")  # Figure 2

    # Don't immediately exit, otherwise the graphs won't show up - so wait
    # for the user to prompt the program to end
    if Settings.DRAW_GRAPH:
        input()
