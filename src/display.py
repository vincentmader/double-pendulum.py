import sys
import time

from numpy import cos, sin
import pygame

import config as cfg


# Define colors for displaying with pygame.
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 128, 0), (0, 0, 255)


def format_frame_number(frame_num, nr_of_leading_zeros):
    formatted_frame_num = frame_num
    for i in range(nr_of_leading_zeros):
        if frame_num < 10**i:
            formatted_frame_num = f'0{formatted_frame_num}'

    return formatted_frame_num


def shift_coordinates(x, y):
    x = (0.24 * x + .5) * cfg.DISPLAY_WIDTH
    y = (-0.24 * y + .5) * cfg.DISPLAY_HEIGHT
    return x, y


def make_transparent(color, alpha):
    r, g, b = color[0], color[1], color[2]
    r, g, b = (int(alpha * r), int(alpha * g), int(alpha * b))
    return r, g, b


def draw_frame(display, color):
    lines = [
        ((0, 0), (0, cfg.DISPLAY_HEIGHT)),
        ((0, cfg.DISPLAY_HEIGHT), cfg.DISPLAY_DIMENSIONS),
        (cfg.DISPLAY_DIMENSIONS, (cfg.DISPLAY_WIDTH, 0)),
        ((cfg.DISPLAY_WIDTH, 0), (0, 0)),
    ]
    for line in lines:
        pygame.draw.line(
            display, color, line[0], line[1], 5
        )


def draw_tail(ys, frame_num, L, display, fading_tails=True):
    frames_back = min(frame_num - 1, cfg.TAIL_LENGTH)
    for idx in range(frame_num - frames_back, frame_num):
        y_previous = ys[idx - 1]
        y_current = ys[idx]

        th_1, th_2 = y_current[0], y_current[1]
        x_1c, y_1c = L * sin(th_1), -L * cos(th_1)
        x_2c, y_2c = x_1c + L * sin(th_2), y_1c - L * cos(th_2)
        x_1c, y_1c = shift_coordinates(x_1c, y_1c)
        x_2c, y_2c = shift_coordinates(x_2c, y_2c)

        th_1, th_2 = y_previous[0], y_previous[1]
        x_1p, y_1p = L * sin(th_1), -L * cos(th_1)
        x_2p, y_2p = x_1p + L * sin(th_2), y_1p - L * cos(th_2)
        x_1p, y_1p = shift_coordinates(x_1p, y_1p)
        x_2p, y_2p = shift_coordinates(x_2p, y_2p)

        if fading_tails:
            tail_idx = frame_num - idx
            alpha = 1 - tail_idx / cfg.TAIL_LENGTH
        else:
            alpha = 1

        red = make_transparent(RED, alpha)
        green = make_transparent(GREEN, alpha)

        pygame.draw.line(display, red, (x_2p, y_2p), (x_2c, y_2c), 5)
        if not cfg.CHRISTMAS_MODE:
            pygame.draw.line(display, green, (x_1p, y_1p), (x_1c, y_1c), 5)


def main(ys, L, fading_tails=True):
    pygame.init()

    # Define display.
    display = pygame.display.set_mode(cfg.DISPLAY_DIMENSIONS, 0, 32)

    # Define fonts.
    pygame.font.init()
    myfont = pygame.font.SysFont('Hack Nerd', 60)
    title_font = pygame.font.SysFont('Hack Nerd', 100)

    frame_num = 0
    while True:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display christmas message.
        if cfg.CHRISTMAS_MODE and frame_num == 368:  # <3
            text = f'Merry Christmas!'
            textsurface = title_font.render(f'{text}', False, (255, 0, 0))
            position = (.16*cfg.DISPLAY_WIDTH, .16*cfg.DISPLAY_HEIGHT)
            display.blit(textsurface, position)
            pygame.display.update()
            continue

        # Stop animation after last entry in simulation output data.
        try:
            y = ys[frame_num]
        except IndexError:
            continue

        # Clear screen.
        display.fill(BLACK)

        # Get pendulum coordinates for given frame.
        th_1, th_2 = y[0], y[1]
        x_1, y_1 = L * sin(th_1), -L * cos(th_1)
        x_2, y_2 = x_1 + L * sin(th_2), y_1 - L * cos(th_2)
        x_1, y_1 = shift_coordinates(x_1, y_1)
        x_2, y_2 = shift_coordinates(x_2, y_2)

        # Draw tails, pendulum bodies, and pendulum rods.
        fading_tails = False if cfg.CHRISTMAS_MODE else True
        draw_tail(
            ys,
            frame_num,
            L,
            display,
            fading_tails=fading_tails
        )
        pygame.draw.circle(display, WHITE, cfg.ORIGIN, 10)
        pygame.draw.circle(display, WHITE, (x_1, y_1), 10)
        pygame.draw.circle(display, WHITE, (x_2, y_2), 10)
        pygame.draw.line(display, WHITE, cfg.ORIGIN, (x_1, y_1), cfg.LINE_WIDTH)
        pygame.draw.line(display, WHITE, (x_1, y_1), (x_2, y_2), cfg.LINE_WIDTH)

        # Show frame number in top left.
        if cfg.SHOW_FRAME_NR and not cfg.CHRISTMAS_MODE:
            formatted_frame_num = format_frame_number(
                frame_num, len(str(len(ys)))
            )
            text = f'{formatted_frame_num}'
            textsurface = myfont.render(f'{text}', False, (255, 255, 255))
            display.blit(textsurface, (20, 20))
            text = f' /  {len(ys)}'
            textsurface = myfont.render(f'{text}', False, (255, 255, 255))
            display.blit(textsurface, (150, 20))

        draw_frame(display, WHITE)

        # Update, wait shortly, update frame number.
        pygame.display.update()
        time.sleep(0.01)
        frame_num += 1
