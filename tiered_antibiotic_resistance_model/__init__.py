#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
if hasattr(sys, '_called_from_test'):
    # Only import the minimal model for testing (no need for big matplotlib/pandas imports)
    from .model_minimal import Params, Settings, Infection, Treatment, Person, Model, DataHandler, decision, run
else:
    # Import everything if general import is done
    from .model import Params, Settings, Infection, Treatment, Person, Model, DataHandler, DataRenderer, decision, run, run_and_output
    from .model_minimal import Params, Settings, Infection, Treatment, Person, Model, DataHandler, decision, run
