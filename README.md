# COHEN2-final_year_project
Reposity for final year project

- code-generation.py code is taken from stephens-2d-eigenworm-data gitlab repository which loads data from two MATLAB files:
  - "20150814 All PNAS2011 data stitched.mat" file contains tracking data for 12 worms.
  - "EigenWorms.mat" file contains the eigenworms used in this analysis.
- "initial_graphs.py" code contains graphs for the first 6 eigenworms (Principal Components)
- "code_gen.py" code contains the EigenData class n from stephens-2d-eigenworm-data gitlab repository from test.py in order to generate the data.(taken from https://gitlab.com/tom-ranner/stephens-2d-eigenworm-data/-/blob/master/stephens-2011-data/test.py)
- "variance_graphs.py" includes calculations regarding the percentage of variance of the worm's posture reconstruction method and graphical representations of the overall variance.
- "sinwave_reconstruction" is the python script for the first approach, which is reconstructing a sine wave.
- "posture.py" python code for second approach and reconstructs the worm posture using as datasets the two matlab files and produces an animation of the reformed worm movement.
- "GeometricPhase.py" generates the geometric phase and includes calculations and visualisations of parameters such as the phase, phase velocity, phase acceleration and moving velocity.
