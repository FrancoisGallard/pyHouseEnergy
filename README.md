# pyHouseEnergy
A simple python house thermal simulation, with eventually solar heating system.


Aims to provide simple time dependent simulation of heat fluxes in a house
User provides inputs in a config text file and runs main.py

The house configuration must be filled: surfaces and insulation properties, mechanical vent, hot water consumption.
A scenario is a time simulation, for a given outside temperature and a user selected inside temperature.
Solar panels (only peoviding heat, not photo voltaic) can be simulated, with a water heat tank.

The price of heating the house and overall energy cost is estimated.
The simulator outputs plots in pdf format thanks to matplotlib.

The models are very simple linear heat transfer equations.
This lacks validation and tests.
