# Welcome to HyperAir!
# If you haven't already, read the README please!
# This file is just to ensure that we don't mess up and get errors for stuff.

import os
from pathlib import Path
import time
from collpy import *
import random

<<<<<<< HEAD
os.system('clear')
print("Welcome to HyperAir!")
print("Beginning loading process...")
print("")
print("Checking directories...")
time.sleep(1)
print("CWD: ", os.getcwd())
=======
import sys
pyver = sys.version_info.major
if pyver < 3:
    print("Oh no! You currently have Python", pyver, ". Please upgrade to Python 3 or above.")
elif pyver >= 3:
    print("Python", pyver, " found, continuing...")


print("CWD", os.getcwd())
>>>>>>> 26e21a0 (Added a simple house (not in game, but the code is there and it works) and made some changes to the python version-checker and also added better crash physics.)

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
