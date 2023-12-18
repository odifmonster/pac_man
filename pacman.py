#!/usr/bin/env python
import pygame

import maze, position

def main():
    TILE_SIZE = 18
    BG_COLOR = (0,0,0)
    EDGE_COLOR = (0,0,255)

    m = maze.Maze()
    m.init()

    pygame.init()

    screen = pygame.display.set_mode((m.ncols*TILE_SIZE, m.nrows*TILE_SIZE))

    running = True
    while running:

        screen.fill(BG_COLOR)

        for r in range(m.nrows):
            for c in range(m.ncols):
                tile_pos = position.ListCoord(v=(c,r))

                tile_points = m.get_tile_points(tile_pos)

                if tile_points:
                    start, end1, end2 = tile_points
                    pygame.draw.line(screen, EDGE_COLOR,
                                     (start.x*TILE_SIZE, start.y*TILE_SIZE),
                                     (end1.x*TILE_SIZE, end1.y*TILE_SIZE))
                    pygame.draw.line(screen, EDGE_COLOR,
                                     (start.x*TILE_SIZE, start.y*TILE_SIZE),
                                     (end2.x*TILE_SIZE, end2.y*TILE_SIZE))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()