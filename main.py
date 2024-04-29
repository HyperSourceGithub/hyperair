# Welcome to HyperAir!
# If you haven't already, read the README please!
# This file is just to ensure that we don't mess up and get errors for stuff.

import os
from pathlib import Path
import time

print("CWD", os.getcwd())

# Change directory
os.chdir(Path(__file__).parent.absolute())
print("Parent", Path(__file__).parent.absolute())

print("CWD", os.getcwd())
time.sleep(2)


import flightsim
