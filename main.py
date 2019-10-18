# -*- coding: utf-8 -*-
	
from panel import Panel
from tank import Tank
from house import House
from scenario import Scenario
from configobj import ConfigObj, flatten_errors
from validate import Validator
import pprint
from os.path import join, dirname,exists

sim_dir="/storage/emulated/0/solarsim/"
curr_dir=dirname(__file__)

with open(join(curr_dir,"inputs.txt"), "r") as infile:
    lines=infile.readlines()
input_spec=join(curr_dir, "configspec.txt")
config=ConfigObj(lines, raise_errors=True,
	                configspec=input_spec,
	                stringify=True)
val = Validator() 
results = config.validate(val) 
if results == True: 
    print 'Inputs validation succeeded.'
else:
    errors=flatten_errors(config, results)
    for section_list, key, _ in errors:
        if key is not None:
            msg='The "%s" key in the section "%s" failed validation'
            print msg%(key, ', '.join(section_list))
        else:
            print 'The following section was missing %s '.join(section_list)
    raise ValueError("Invalid input data")
print "Simulation inputs :"
pp = pprint.PrettyPrinter(indent=4)
in_data={}
in_data.update(config)
pp.pprint(in_data)


panel=Panel(**config["Panels"])
tank =Tank(**config["Tank"])
print tank
house=House(**config["House"])
scenario=Scenario(house, panel, tank)
scenario.loop(**config["Scenario"])

scenario.post(sim_dir)
house.post(sim_dir)

