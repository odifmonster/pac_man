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

    move_thetas = [(0, 2*math.pi), (math.pi/6, 11*math.pi/6), (math.pi/3, 5*math.pi/3)]
    death_thetas = [(math.pi/3+t*math.pi/15, 5*math.pi/3-t*math.pi/15) for t in range(10)]
    draw_ind = 0
    draw_type = ['m', 'd']

    running = True
    key_is_pressed = False
    nframes = 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0,0))

        if draw_ind == 0:
            theta = move_thetas[(nframes // 100) % 3]
        elif draw_ind == 1:
            theta = death_thetas[(nframes // 100) % 10]

        filled_sect(screen,
                    PACMAN_SIZE/2, PACMAN_SIZE/2, PACMAN_SIZE/2 * PACMAN_RAD,
                    theta[0], theta[1],
                    (255,255,0))
        
        pygame.display.flip()

        if nframes % 100 == 0:
            if draw_ind == 0:
                total = len(move_thetas)
            elif draw_ind == 1:
                total = len(death_thetas)
            fname = f'pacman-{draw_type[draw_ind]}{(nframes // 100) % total}.png'
            pygame.image.save(screen, os.path.join(SCRIPT_DIR, 'pacman', fname))

        nframes += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT] and not key_is_pressed:
                    draw_ind = (draw_ind+1) % 2
                    key_is_pressed = True
            elif event.type == pygame.KEYUP:
                key_is_pressed = False

if __name__ == '__main__':
    main()