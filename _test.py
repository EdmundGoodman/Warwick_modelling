#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from model_v4 import Params, Settings, Infection, Treatment, Person, Model, DataHandler, DataRenderer, decision, run

class TestModel(unittest.TestCase):

    def test_empty_model(self):
        """Test that a model with no infected people always stays fully uninfected"""
        Params.INITIALLY_INFECTED = 0
        m = run()
        # The number of uninfected people should always be the size of the population
        self.assertEqual(m.data_handler.get_uninfected_data(),
                                [Params.POPULATION_SIZE]*Params.NUM_TIMESTEPS)
        # The number of infected people should always be zero
        self.assertEqual(m.data_handler.get_infected_data()[0],
                                                    [0]*Params.NUM_TIMESTEPS)

    def test_instant_death(self):
        """Test that a model where infection causes instant death immediately
        'peters out', as dead people cannot spread"""
        Params.PROBABILITY_DEATH = 1
        m = run()

        # The final number of uninfected people should be the size of the
        # initially uninfected population
        self.assertEqual(m.data_handler.get_uninfected_data()[-1],
                            Params.POPULATION_SIZE - Params.INITIALLY_INFECTED)
        # The final number of infected people should be zero
        self.assertEqual(m.data_handler.get_infected_data()[0][-1], 0)
        # The final number of dead people should be the number of initially
        # infected people
        self.assertEqual(m.data_handler.get_death_data()[-1],
                                                    Params.INITIALLY_INFECTED)


if __name__ == "__main__":
    """Test the model"""

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
