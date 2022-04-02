# CA4024 - Complex Computational Models: Assignment 1

## Assignment Details

The main objective of this assignment is to define an ABM (Agent Based Model) of any natural/human phenomenon. These phenomana could be the spread of a virus, the evacuation behaviour of a building under panic, ant behaviour, etc.

The assignment involves clear documentation of the model (purpose, rules, tracking of outputs, etc.) and the code must be well-structured and documented. The model must have the ability to output the result as time-based graphs and must also allow users to change initial parameters of the model.

## Repository Structure

This assignment will be modelling the effect of tiredness on drivers.

The repository is structured as follows:

* [Screenshots](Screenshots/): This is a directory containing the screenshots of running the simulation under different parameters.
* [ABM_traffic_simulator.py](ABM_traffic_simulator.py): This is the python script containing the ABM model and the driver class.
* [functions.py](functions.py): This is a python script that holds any functions used by the ABM_traffic_simulator.py file that does not need to be directly stored in that file.
* [pycxsimulator.py](pycxsimulator.py): This is a python script (available [here](https://github.com/hsayama/PyCX/blob/master/pycxsimulator.py)) that is required in order to visualise the ABM. 