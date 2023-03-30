import os


# Specfiy whether integrator should be run. If not, 
# simulation-data will be loaded from the save-file 
# `./out/states.txt` (if it exists).
RUN_INTEGRATOR = True

# Specfiy whether or not to run in "christmas mode".
CHRISTMAS_MODE = False

# Define nr. of integration steps.
STEPS = 10000 if not CHRISTMAS_MODE else 1000

# Define path to save-file.
PATH_TO_SAVEFILE = os.path.join("..", "out", "states.txt")

# Define dimensions of PyGame display.
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = DISPLAY_WIDTH
DISPLAY_DIMENSIONS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# Define coordinate origin.
ORIGIN = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)

# Define length of displayed "tails".
TAIL_LENGTH = 200 if not CHRISTMAS_MODE else 135

# Define width of displayed lines.
LINE_WIDTH = 2

# Define value of gravitational acceleration g.
GRAVITATIONAL_ACCELERATION = 0.5

# Specify whether frame nr. should be shown in upper left corner.
SHOW_FRAME_NR = False

# Specify initial conditions.
# - either "random"
# - or a list of the form  [phi_1, phi_2, omega_1, omega_2],
#   where phi labels the initial position angle of the two bodies,
#   and omega their initial angular velocity.
#   NOTE: It's been a few years since I wrote this, 
#         maybe it's the angular momenta instead of angular velocities...
INITIAL_CONDITIONS = "random"
