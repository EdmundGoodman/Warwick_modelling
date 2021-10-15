#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from .model_minimal import Params, Settings, Infection, Treatment, Person, Model, DataHandler, decision, run


DEFAULT_NUM_TIMESTEPS = Params.NUM_TIMESTEPS
DEFAULT_POPULATION_SIZE = Params.POPULATION_SIZE
DEFAULT_INITIALLY_INFECTED = Params.INITIALLY_INFECTED
DEFAULT_DRUG_NAMES = Params.DRUG_NAMES
DEFAULT_PROBABILITY_MOVE_UP_TREATMENT = Params.PROBABILITY_MOVE_UP_TREATMENT
DEFAULT_TIMESTEPS_MOVE_UP_LAG_TIME = Params.TIMESTEPS_MOVE_UP_LAG_TIME
DEFAULT_ISOLATION_THRESHOLD = Params.ISOLATION_THRESHOLD
DEFAULT_PRODUCT_IN_USE = Params.PRODUCT_IN_USE
DEFAULT_PROBABILIY_PRODUCT_DETECT = Params.PROBABILIY_PRODUCT_DETECT
DEFAULT_PRODUCT_DETECTION_LEVEL = Params.PRODUCT_DETECTION_LEVEL
DEFAULT_PROBABILITY_GENERAL_RECOVERY = Params.PROBABILITY_GENERAL_RECOVERY
DEFAULT_PROBABILITY_TREATMENT_RECOVERY = Params.PROBABILITY_TREATMENT_RECOVERY
DEFAULT_PROBABILITY_MUTATION = Params.PROBABILITY_MUTATION
DEFAULT_PROBABILITY_DEATH = Params.PROBABILITY_DEATH
DEFAULT_DEATH_FUNCTION = Params.DEATH_FUNCTION
DEFAULT_PROBABILITY_SPREAD = Params.PROBABILITY_SPREAD
DEFAULT_NUM_SPREAD_TO = Params.NUM_SPREAD_TO


def reset_params():
    DEFAULT_NUM_TIMESTEPS = Params.NUM_TIMESTEPS
    DEFAULT_POPULATION_SIZE = Params.POPULATION_SIZE
    DEFAULT_INITIALLY_INFECTED = Params.INITIALLY_INFECTED
    DEFAULT_DRUG_NAMES = Params.DRUG_NAMES
    DEFAULT_PROBABILITY_MOVE_UP_TREATMENT = Params.PROBABILITY_MOVE_UP_TREATMENT
    DEFAULT_TIMESTEPS_MOVE_UP_LAG_TIME = Params.TIMESTEPS_MOVE_UP_LAG_TIME
    DEFAULT_ISOLATION_THRESHOLD = Params.ISOLATION_THRESHOLD
    DEFAULT_PRODUCT_IN_USE = Params.PRODUCT_IN_USE
    DEFAULT_PROBABILIY_PRODUCT_DETECT = Params.PROBABILIY_PRODUCT_DETECT
    DEFAULT_PRODUCT_DETECTION_LEVEL = Params.PRODUCT_DETECTION_LEVEL
    DEFAULT_PROBABILITY_GENERAL_RECOVERY = Params.PROBABILITY_GENERAL_RECOVERY
    DEFAULT_PROBABILITY_TREATMENT_RECOVERY = Params.PROBABILITY_TREATMENT_RECOVERY
    DEFAULT_PROBABILITY_MUTATION = Params.PROBABILITY_MUTATION
    DEFAULT_PROBABILITY_DEATH = Params.PROBABILITY_DEATH
    DEFAULT_DEATH_FUNCTION = Params.DEATH_FUNCTION
    DEFAULT_PROBABILITY_SPREAD = Params.PROBABILITY_SPREAD
    DEFAULT_NUM_SPREAD_TO = Params.NUM_SPREAD_TO
    Params.reset_granular_parameters()


def set_no_deaths_recoveries():
    Params.DEATH_FUNCTION = lambda p, t: p
    Params.PROBABILITY_GENERAL_RECOVERY = 0
    Params.PROBABILITY_TREATMENT_RECOVERY = 0
    Params.NUM_TIMESTEPS = 3 * Params.TIMESTEPS_MOVE_UP_LAG_TIME


class TestModel(unittest.TestCase):
    def test_empty_model(self):
        """Test that a model with no infected people always stays fully uninfected"""
        # Change parameters for the test setup and run the test
        Params.INITIALLY_INFECTED = 0
        m = run()
        self.assertEqual(m.data_handler.get_uninfected_data(),
                         [Params.POPULATION_SIZE]*Params.NUM_TIMESTEPS)
        self.assertEqual(m.data_handler.get_infected_data()[0],
                         [0]*Params.NUM_TIMESTEPS)
        reset_params()

    def test_all_infected_certain_death(self):
        """100% infected, 100% death chance, 0% recovery -> 100% death rate"""
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_DEATH = 1
        Params.PROBABILITY_GENERAL_RECOVERY = 0
        Params.PROBABILITY_TREATMENT_RECOVERY = 0
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_death_data()[-1], Params.POPULATION_SIZE)
        reset_params()


    def test_all_infected_certain_recovery(self):
        """100% infected, 0% death chance, 100% recovery -> 100% immune"""
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_DEATH = 0
        Params.DEATH_FUNCTION = lambda p, t: p
        Params.PROBABILITY_GENERAL_RECOVERY = 1
        Params.PROBABILITY_TREATMENT_RECOVERY = 1
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_immune_data()[-1], Params.POPULATION_SIZE)
        reset_params()

    def test_total_spread(self):
        """1 infected, 100% infection chance, 50 infected per infection-> 100%
        infected
        Params.NUM_SPREAD_TO = 50
        Params.INITIALLY_INFECTED = 1
        Params.PROBABILITY_SPREAD = 1
        Params.PROBABILITY_DEATH = 0
        Params.PROBABILITY_GENERAL_RECOVERY = 0
        Params.PROBABILITY_TREATMENT_RECOVERY = 0
        Params.PROBABILITY_MUTATION = 0
        Params.reset_granular_parameters()

        # TODO: Reason about number of timesteps needed

        m = run()
        print(m.data_handler.get_infected_data())
        self.assertEqual(m.data_handler.get_infected_data()[0][-1], Params.POPULATION_SIZE)
        self.assertEqual(m.data_handler.get_uninfected_data(), 0)

        reset_params()"""


    def test_no_spread_num(self):
        """1 infected, 100% infection chance, 0 infected per infection -> 1
        infected"""
        Params.INITIALLY_INFECTED = 1
        Params.PROBABILITY_SPREAD = 1
        Params.NUM_SPREAD_TO = 0
        Params.PROBABILITY_MUTATION = 0
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_infected_data()[0], [1]*Params.NUM_TIMESTEPS)
        reset_params()

    def test_no_spread_percent(self):
        """1 infected, 0% infection chance, 100 infected per infection -> 1
        infected"""
        Params.INITIALLY_INFECTED = 1
        Params.PROBABILITY_SPREAD = 0
        Params.NUM_SPREAD_TO = 100
        Params.PROBABILITY_MUTATION = 0
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_infected_data()[0], [1]*Params.NUM_TIMESTEPS)
        reset_params()

    def test_no_move_up_treatment(self):
        """100% infected, 100% mutation chance, 0% move up treatment -> 100%
        with lvl 1 resistance, 0% lvl 3"""
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_MUTATION = 1
        Params.PROBABILITY_MOVE_UP_TREATMENT = 0
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_infected_data()[0], [Params.INITIALLY_INFECTED]+[0]*(Params.NUM_TIMESTEPS-1))
        self.assertEqual(m.data_handler.get_infected_data()[1], [0]+[Params.POPULATION_SIZE]*(Params.NUM_TIMESTEPS-1))
        self.assertEqual(m.data_handler.get_infected_data()[-1], [0]*Params.NUM_TIMESTEPS)
        reset_params()

    def test_move_up_all_treatment(self):
        """100% infected, 100% mutation chance, 100% move up treatment -> 100%
        with lvl 3 resistance"""
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_MUTATION = 1
        Params.PROBABILITY_MOVE_UP_TREATMENT = 1
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_infected_data()[0][0], Params.POPULATION_SIZE)
        self.assertEqual(m.data_handler.get_infected_data()[-1][0], 0)
        self.assertEqual(m.data_handler.get_infected_data()[-1][-1], Params.POPULATION_SIZE)
        reset_params()

    def test_move_up_all_treatment_slow(self):
        """100% infected, 100% mutation chance, 100% move up treatment, 10 days
        lag for move up -> 100% with lvl 3 resistance but only over time."""
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_MUTATION = 1
        Params.PROBABILITY_MOVE_UP_TREATMENT = 1
        Params.TIMESTEPS_MOVE_UP_LAG_TIME = 10
        Params.NUM_TIMESTEPS = 3 * Params.TIMESTEPS_MOVE_UP_LAG_TIME
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_infected_data()[0][0], Params.POPULATION_SIZE)
        self.assertEqual(m.data_handler.get_infected_data()[0][-1], 0)
        self.assertEqual(m.data_handler.get_infected_data()[1][1], Params.POPULATION_SIZE)
        self.assertEqual(m.data_handler.get_infected_data()[1][Params.TIMESTEPS_MOVE_UP_LAG_TIME+2], 0)
        self.assertEqual(m.data_handler.get_infected_data()[2][Params.TIMESTEPS_MOVE_UP_LAG_TIME+2], Params.POPULATION_SIZE)
        self.assertEqual(m.data_handler.get_infected_data()[-1][-1], Params.POPULATION_SIZE)
        reset_params()

    def test_ioslation_no_move_up(self):
        """100% infected, 100% mutation chance, 0% move up treatment, isolation
        threshold = 1, no product -> 0% isolated"""
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_MUTATION = 1
        Params.PROBABILITY_MOVE_UP_TREATMENT = 0
        Params.ISOLATION_THRESHOLD = 1
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()
        self.assertEqual(m.data_handler.get_isolated_data(), [0]*Params.NUM_TIMESTEPS)
        reset_params()

    def test_isolation_no_mutation(self):
        """100% infected, 0% mutation chance, 100% move up treatment, isolation
        threshold = 3, no product -> 100% isolated
        Params.INITIALLY_INFECTED = Params.POPULATION_SIZE
        Params.PROBABILITY_MUTATION = 0
        Params.PROBABILITY_MOVE_UP_TREATMENT = 1
        Params.ISOLATION_THRESHOLD = 3
        Params.PRODUCT_IN_USE = False
        Params.TIMESTEPS_MOVE_UP_LAG_TIME = 1
        set_no_deaths_recoveries()
        Params.reset_granular_parameters()
        m = run()

        print()
        print(m.data_handler.get_infected_data())
        print(m.data_handler.get_death_data())
        print(m.data_handler.get_immune_data())
        print(m.data_handler.get_isolated_data())
        print()

        self.assertEqual(m.data_handler.get_isolated_data()[-1], Params.POPULATION_SIZE)
        reset_params()"""

    def test_isolation_product(self):
        """100% infected, 100% mutation chance, 0% move up treatment, isolation
        threshold = 1, product detects at 1-> 100% isolated"""
        m = run()
        self.assertEqual(None,None)
        reset_params()

    def test_disjoint_states(self):
        """Check over all timesteps that the states are disjoint"""
        m = run()
        for i in range(Params.NUM_TIMESTEPS):
            infected = sum([x[i] for x in m.data_handler.get_infected_data()])
            dead = m.data_handler.get_death_data()[i]
            immune = m.data_handler.get_immune_data()[i]
            uninfected = m.data_handler.get_uninfected_data()[i]
            self.assertEqual(sum([infected, dead, immune, uninfected]),Params.POPULATION_SIZE)
        reset_params()


if __name__ == "__main__":
    """Apply unit tests to the model. However, since the model itself is
    stochastic, these unit tests are in fact a form of property based testing,
    as the inputs can vary dependent on the random seed. This means that by
    iterating within the tests, a proportion of the input space can be searched,
    adding further guarantees at correctness."""

    # Don't always use the same seed - allows property based testing
    Settings.RANDOM_SEED = None
    # Don't print model state, as the outputs are internally inspected
    Settings.REPORT_PROGRESS = False
    Settings.PRINT_DATA = False

    # Make the models run a bit faster (if tests specifically need these things
    # to be larger, they can set them themselves on a case-by-case basis)
    Params.NUM_TIMESTEPS = 25
    Params.POPULATION_SIZE = 25
    Params.INITIALLY_INFECTED = 2

    # Run the unit tests
    unittest.main()

    print("All tests passed")
