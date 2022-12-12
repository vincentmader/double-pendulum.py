import os

import numpy as np
from numpy import pi as PI

import config as cfg
from integrate import main as integrate
from display import main as display


def get_initial_state():
    if cfg.CHRISTMAS_MODE:
        return [PI * .75, PI * .75, 0, 0]
    elif cfg.INITIAL_CONDITIONS != "random":
        return [PI, .8 * PI, 0, 0]
    else:
        return [PI, np.random.rand(1, 1) * PI, 0, 0]


def main(
    run_integrator=cfg.RUN_INTEGRATOR
):
    # Set parameters of physical system.
    L, m = 1, 1

    # Define initial conditions.
    initial_state = get_initial_state()

    # Run integrator, or load from file.
    if run_integrator:
        states = integrate(initial_state, m, L)
        np.savetxt(cfg.PATH_TO_SAVEFILE, states)
    else:
        if os.path.exists(cfg.PATH_TO_SAVEFILE):
            states = np.loadtxt(cfg.PATH_TO_SAVEFILE)
        else:
            print("\nNo save-file found, exiting...")
            return

    # Display simulation using pygame.
    display(states, L, fading_tails=True,)


if __name__ == "__main__":
    main()
