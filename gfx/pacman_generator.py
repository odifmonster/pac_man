#!/usr/bin/env python
import os
import math
import pygame, pygame.gfxdraw

def filled_sect(surface, cx, cy, radius, theta0, theta1, color, ndiv=50):
    dtheta = (theta1-theta0) / ndiv
    angles = [theta0 + dtheta*i for i in range(ndiv+1)]
    points = [(cx-radius/2, cy)] + [(cx+math.cos(theta)*radius,cy-math.sin(theta)*radius) for theta in angles]

    pygame.gfxdraw.filled_polygon(surface, points, color)

def main():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    PACMAN_SIZE = 20*2
    PACMAN_RAD = 0.8

    pygame.init()

    screen = pygame.display.set_mode((PACMAN_SIZE, PACMAN_SIZE))

    thetas = [(0, 2*math.pi), (math.pi/6, 11*math.pi/6), (math.pi/3, 5*math.pi/3)]

    running = True
    nframes = 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0,0))

        theta = thetas[(nframes // 100) % 3]

        filled_sect(screen,
                    PACMAN_SIZE/2, PACMAN_SIZE/2, PACMAN_SIZE/2 * PACMAN_RAD,
                    theta[0], theta[1],
                    (255,255,0))
        
        pygame.display.flip()

        if nframes % 100 == 0:
            fname = f'pacman-{(nframes // 100) % 3}.png'
            pygame.image.save(screen, os.path.join(SCRIPT_DIR, fname))

        nframes += 1

        if nframes >= 300:
            running = False

if __name__ == '__main__':
    main()