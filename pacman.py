#!/usr/bin/env python
import os
import pygame

from structures import maze as mz, position as pos

# global constants
TILE_SIZE = 18
DOT_COLOR = (255,255,255)

def main():

    m = mz.Maze()
    m.init()

    pygame.init()

    screen = pygame.display.set_mode((m.ncols*TILE_SIZE, m.nrows*TILE_SIZE))

    maze_img = pygame.image.load(os.path.join('gfx','maze_sqr.png'))

    running = True
    while running:

        screen.blit(maze_img, (0,0))

        for r in range(m.nrows):
            for c in range(m.ncols):
                
                if m.get_tile(pos.ListCoord(x=c,y=r)) == mz.Tile.DOT:
                    pygame.draw.circle(screen, DOT_COLOR,
                                       ((c+0.5)*TILE_SIZE, (r+0.5)*TILE_SIZE), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()