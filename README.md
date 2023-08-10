# Presentation of the subject

## Context of the repository

This repository was created as part of an internship at TalTech University.

## Content

This repository deals with cluster head election and vehicle position and direction prediction and the extraction of data from SUMO.

# Information

## Attention

On GitHub it only has the python function files. Not the data.

The sumo data is too big to be exported to GitHub in the normal way (I need to compress it) and in any case I intend to use other data in the future.

So my functions are designed to adapt to all types of intersection.

## Things to do before launching the programme

• First you need to install Python 2.7 or higher, and install SUMO

• Secondly, you need to use two functions available in the /sumo/tools file
And use the following lines of code:

'python osmWebWizard.py'

For more information, see [osmWebWizard Documentation](https://sumo.dlr.de/docs/Tutorials/OSMWebWizard.html)

'python randomTrips . py -n osm . net . xml -r osm_pt . roub . xml -e 4801140'

For more information, see [randomTrips Documentation](https://sumo.dlr.de/docs/Tools/Trip.html)

• Now go to your Home directory, and copy the created folder (named with the current time) under /data/one_run/m

## Files in the folder

• main.ipynb

The experiments notebook

• Initialisation.py

Useful file for initialising and extracting data on SUMO

• CH.py

File used for the election and maintenance of the cluster head

• PredictPos.py

File used to predict the future position and intersection with traffic light

• ModifyFile.py

File used to analyse results and plot graphs