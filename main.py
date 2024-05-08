# Welcome to HyperAir!
# If you haven't already, read the README please!
# This file is just to ensure that we don't mess up and get errors for stuff.

import os
from pathlib import Path
import time
from collpy import *
import random

os.system('clear')
print("Welcome to HyperAir!")
print("Beginning loading process...")
print("")
print("Checking directories...")
time.sleep(1)
print("CWD: ", os.getcwd())

# Change directory
os.chdir(Path(__file__).parent.absolute())
print("Parent: ", Path(__file__).parent.absolute())

print("CWD: ", os.getcwd())
print("")

loadbar = Load_bar(name="Loading Data... ", length=60, style='#')

val = 100

delay = random.randint(2, 6) / 100
for i in loadbar.iter(val): # or string or val
    e = i
    time.sleep(delay)

print("Done!")  

import flightsim
