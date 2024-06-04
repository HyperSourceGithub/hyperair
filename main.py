# Welcome to HyperAir!
# If you haven't already, read the README please!
# This file is just to ensure that we don't mess up and get errors for stuff.

try:
    import os
    from pathlib import Path
    import time
    from collpy import *
    import random
except ImportError as e:
    autoimport = input("Missing dependencies! Would you like to import them super-automagically? [Y/n]")
    if autoimport.lower() == "y":
        os.system("python3 -m pip install -r requirements.txt")
    elif autoimport.lower() == "n":
        print("Please run [python3 -m pip install -r requirements.txt] please.")
        exit()

os.system('clear')
print("Welcome to HyperAir!")
print("Beginning loading process...")
print("")
print("Checking directories...")
time.sleep(1)
print("CWD: ", os.getcwd())

import sys
pyver = sys.version_info.major
if pyver < 3:
    print("Oh no! You currently have Python", pyver, ". Please upgrade to Python 3 or above.")
elif pyver >= 3:
    print("Python", pyver, " found, continuing...")


print("CWD", os.getcwd())

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
