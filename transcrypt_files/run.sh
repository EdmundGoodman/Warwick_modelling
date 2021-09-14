#!/bin/bash


python -m transcrypt -b -m -n model_v2_in.py
python -m http.server
