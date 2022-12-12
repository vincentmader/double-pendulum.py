from tqdm import tqdm

import numpy as np
from numpy import cos, sin
from scipy.integrate import RK45

import config as cfg

# Set parameters for 4th order Runge-Kutta integration scheme.
t0, t_bound = 0, 10000
first_step, max_step = .05, .05


def main(y0, m, L):
    print("Running RK4 integrator...")
    g = cfg.GRAVITATIONAL_ACCELERATION

    # Define temporal derivative:  dy/dt = f(t, y)
    def f(t, y):
        th_1, th_2, p_1, p_2 = y[0], y[1], y[2], y[3]
        dth = th_1 - th_2
        dth_1 = 6/(m*L**2) * (2*p_1 - 3*cos(dth) * p_2) / (16 - 9*cos(dth)**2)
        dth_2 = 6/(m*L**2) * (8*p_2 - 3*cos(dth) * p_1) / (16 - 9*cos(dth)**2)
        dp_1 = -m * L**2 / 2 * (dth_1 * dth_2 * sin(dth) + 3*g/L*sin(th_1))
        dp_2 = -m * L**2 / 2 * (-dth_1 * dth_2 * sin(dth) + g/L*sin(th_2))
        return np.array([dth_1, dth_2, dp_1, dp_2])

    # Define Runge-Kutta integrator.
    integrator = RK45(
        f,
        t0,
        y0,
        t_bound,
        first_step=first_step,
        max_step=max_step
    )

    # Integrate.
    ys = []
    for _ in tqdm(range(cfg.STEPS)):
        _ = integrator.step()
        ys.append(integrator.y)

    return ys
