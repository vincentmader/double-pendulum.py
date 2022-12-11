import os

import numpy as np
from numpy import pi as PI

import config as cfg
from integrate import main as integrate
from display import main as display


def initial_conditions():
    if cfg.CHRISTMAS_MODE:
        return [PI * .75, PI * .75, 0, 0]
    else:
        return [PI, .8 * PI, 0, 0]


def main(
    run_integrator=True,
):
    # Define path to savefile.
    filename = "states.txt"
    savepath = os.path.join(cfg.PATH_TO_OUT, filename)

    # Set parameters of physical system.
    L, m = 1, 1

    # Define initial conditions.
    y0 = initial_conditions()

    # Run integrator, or load from file.
    if run_integrator:
        ys = integrate(y0, m, L)
        np.savetxt(savepath, ys)
    else:
        ys = np.loadtxt(savepath)

    # Display simulation using pygame.
    display(ys, L, fading_tails=True,)


if __name__ == "__main__":
    main()
