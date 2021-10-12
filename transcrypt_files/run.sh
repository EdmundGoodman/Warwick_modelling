#!/bin/bash


python -m transcrypt -b -m -n model.py
python -m http.server
