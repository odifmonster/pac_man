#!/usr/env/bin python

import sys, os
import pygame

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from structures.maze import *
from structures.position import *

TILE_SIZE = 20

BG_COLOR = (0,0,0)
EDGE_COLOR = (0,0,255)
GWALL_COLOR = (255,192,255)

DIRS = [Direction.E, Direction.NE, Direction.N, Direction.NW,
        Direction.W, Direction.SW, Direction.S, Direction.SE]

def get_tile_rects(maze: Maze, pos: ListCoord) -> list[pygame.Rect]:

    if not pos.is_in_bounds(maze.nrows, maze.ncols):
        raise IndexError('Cannot get drawable rects for out-of-bounds tile.')
    
    if maze.get_tile(pos) != Tile.EDGE:
        return []
    
    rects = []
    dsp_pos = FloatCoord(x=pos.x*TILE_SIZE, y=pos.y*TILE_SIZE)
    tile_rect = pygame.Rect(dsp_pos.x, dsp_pos.y, TILE_SIZE, TILE_SIZE)

    for dir in DIRS:
        adj = pos.get_adj(dir)

        if maze.get_tile(adj) not in Maze.BOUNDARY_TILES:
            tl = dsp_pos.midpoint_to(FloatCoord(x=adj.x*TILE_SIZE, y=adj.y*TILE_SIZE))
            rects.append(pygame.Rect(tl.x, tl.y, TILE_SIZE, TILE_SIZE).clip(tile_rect))
    
    return rects

def main():

    maze = Maze()
    maze.init()

    pygame.init()
    screen = pygame.display.set_mode((maze.ncols*TILE_SIZE, maze.nrows*TILE_SIZE))

    running = True
    nframes = 0
    while running:

        if nframes == 0:
            screen.fill(BG_COLOR)

            for r in range(maze.nrows):
                for c in range(maze.ncols):

                    tpos = ListCoord(x=c, y=r)

                    if maze.get_tile(tpos) == Tile.EDGE:
                        pygame.draw.rect(screen, EDGE_COLOR,
                                         (tpos.x*TILE_SIZE, tpos.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

                        trects = get_tile_rects(maze, tpos)

                        for rect in trects:
                            pygame.draw.rect(screen, BG_COLOR, rect)
                    elif maze.get_tile(tpos) == Tile.GHOST_WALL:
                        pygame.draw.rect(screen, GWALL_COLOR,
                                         (tpos.x*TILE_SIZE, (tpos.y+0.5)*TILE_SIZE+2,
                                          TILE_SIZE, TILE_SIZE/2-4))
            
            unfill = [[False for _ in range(screen.get_width())] for _ in range(screen.get_height())]

            for r in range(1,len(unfill)-1):
                for c in range(1,len(unfill[r])-1):

                    if screen.get_at((c, r)) == EDGE_COLOR:
                        all_blue = True
                        pixel = ListCoord(x=c, y=r)
                    
                        for dir in DIRS:
                            adj = pixel.get_adj(dir)

                            if not screen.get_at(adj.get_tuple()) == EDGE_COLOR \
                                and not unfill[adj.y][adj.x]:
                                all_blue = False
                    
                        if all_blue:
                            unfill[r][c] = True
                            screen.set_at(pixel.get_tuple(), BG_COLOR)
            
            if os.path.exists(os.path.join(SCRIPT_DIR, 'maze_sqr.png')):
                os.remove(os.path.join(SCRIPT_DIR, 'maze_sqr.png'))

            pygame.image.save(screen, os.path.join(SCRIPT_DIR, 'maze_sqr.png'))
        
        nframes += 1
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()