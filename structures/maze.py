#!/usr/bin/env python

from enum import Enum
from typing import Sequence
#import os, sys
from pygame import Rect

#SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(SCRIPT_DIR))

from structures.position import *

class Tile(Enum):
    """Enum for holding tile types and equivalent strings"""

    EMPTY, DOT, EDGE, OOB, GHOST_WALL = '-', 'o', 'E', 'X', 'G'

    def __repr__(self) -> str:
        return self.value
    
    def __str__(self) -> str:
        return self.__repr__()

class Maze:

    # static constants
    BOUNDARY_TILES = (Tile.EDGE, Tile.OOB, Tile.GHOST_WALL)

    def __init__(self, nrows: int = 31, ncols: int = 28) -> None:
        self.tiles = [[Tile.EMPTY for _ in range(ncols)] for _ in range(nrows)]
        self.nrows = nrows
        self.ncols = ncols
    
    def __repr__(self) -> str:
        return '\n'.join([''.join([str(t) for t in row]) for row in self.tiles])
    
    def get_tile(self, pos: ListCoord) -> Tile:
        if pos.getr() == 14 and (pos.getc() < 6 or pos.getc() >= self.ncols-6):
            pos.wrap(self.ncols, self.nrows)
        
        if not pos.is_in_bounds(self.nrows, self.ncols):
            return Tile.OOB
        
        return self.tiles[pos.getr()][pos.getc()]
    
    def set_tile(self, pos: ListCoord, ttype: Tile) -> None:
        self.tiles[pos.y][pos.x] = ttype
    
    def get_tile_rects(self, pos: ListCoord, tsize: int) -> list[Rect]:
        
        if not pos.is_in_bounds(self.nrows, self.ncols):
            raise IndexError('Cannot get drawable points for out-of-bounds maze tile.')
        
        if self.get_tile(pos) != Tile.EDGE:
            return []
        
        moves = [Direction.E, Direction.NE, Direction.N, Direction.NW,
                 Direction.W, Direction.SW, Direction.S, Direction.SE]
        rects = []
        float_pos = FloatCoord(x=pos.x*tsize, y=pos.y*tsize)

        for move in moves:
            adj = pos.get_adj(move)

            if self.get_tile(adj) not in Maze.BOUNDARY_TILES:
                tl = float_pos.midpoint_to(FloatCoord(x=adj.x*tsize, y=adj.y*tsize))
                rects.append(Rect(tl.x, tl.y, tsize, tsize))
        
        tile_rect = Rect(float_pos.x, float_pos.y, tsize, tsize)

        return [rect.clip(tile_rect) for rect in rects]

    # ================== MAZE INITIALIZATION ==================
    
    def add_block(self, block: Block, ttype: Tile, ignore_type: Sequence[Tile] = []) -> None:

        start, end = block

        if not isinstance(start, ListCoord):
            start = ListCoord(x=start[0], y=start[1])
        if not isinstance(end, ListCoord):
            end = ListCoord(x=end[0], y=end[1])
        
        start.wrap(self.ncols, self.nrows)
        end.wrap(self.ncols, self.nrows)
        
        for r in range(start.y, end.y+1):
            for c in range(start.x, end.x+1):
                pos = ListCoord(x=c, y=r)

                if self.get_tile(pos) not in ignore_type:
                    self.set_tile(ListCoord(x=c,y=r), ttype)
    
    def add_blocks(self, blocks: list[Block], ttype: Tile) -> None:

        for block in blocks:
            self.add_block(block, ttype)
    
    def init(self):
        """Set up all walls/edges in maze separately from constructor method."""

        self.add_block(((0,0),(-1,-1)), Tile.EDGE) # outer box
        self.add_block(((1,1),(-2,-2)), Tile.EMPTY)

        self.add_blocks([((0,9),(5,-12)), ((-6,9),(-1,-12))], Tile.EDGE) # addtional outer edge shaping
        self.add_blocks([((0,10),(4,12)), ((0,-15),(4,-13)), ((-5,10),(-1,12)), ((-5,-15),(-1,-13))],
                        Tile.OOB)
        self.add_blocks([((0,14),(5,14)), ((-6,14),(-1,14))], Tile.EMPTY)

        top_walls = [
            ((2,2),(5,4)), ((-6,2),(-3,4)), ((7,2),(11,4)), ((-12,2),(-8,4)),
            ((self.ncols//2-1,0),(self.ncols//2,4)), ((2,6),(5,7)), ((-6,6),(-3,7)),
            ((7,6),(8,self.nrows//2-2)), ((-9,6),(-8,self.nrows//2-2)),
            ((self.ncols//2-4,6),(self.ncols//2+3,7)),
            ((7,9),(11,10)), ((-12,9),(-8,10)), ((self.ncols//2-1,6),(self.ncols//2,10))
        ]
        self.add_blocks(top_walls, Tile.EDGE) # add walls to top half of maze

        # add ghost house
        self.add_block(((self.ncols//2-4,self.nrows//2-3),(self.ncols//2+3,self.nrows//2+1)), Tile.EDGE)
        self.add_block(((self.ncols//2-3,self.nrows//2-2),(self.ncols//2+2,self.nrows//2)), Tile.OOB)
        self.add_block(((self.ncols//2-1,self.nrows//2-3),(self.ncols//2,self.nrows//2-3)), Tile.GHOST_WALL)

        bottom_walls = [
            ((7,self.nrows//2),(8,self.nrows//2+4)), ((-9,self.nrows//2),(-8,self.nrows//2+4)),
            ((self.ncols//2-4,self.nrows//2+3),(self.ncols//2+3,self.nrows//2+4)),
            ((self.ncols//2-1,self.nrows//2+3),(self.ncols//2,self.nrows//2+7)),
            ((2,-10),(5,-9)), ((4,-10),(5,-6)), ((-6,-10),(-3,-9)), ((-6,-10),(-5,-6)),
            ((0,-7),(2,-6)), ((-3,-7),(-1,-6)), ((7,-10),(11,-9)), ((-12,-10),(-8,-9)),
            ((2,-4),(self.ncols//2-3,-3)), ((self.ncols//2+2,-4),(-3,-3)),
            ((self.ncols//2-4,-7),(self.ncols//2+3,-6)),
            ((7,-7),(8,-3)), ((-9,-7),(-8,-3)), ((self.ncols//2-1,-7),(self.ncols//2,-3))
        ]
        self.add_blocks(bottom_walls, Tile.EDGE)

        self.add_block(((0,0),(-1,8)), Tile.DOT, ignore_type=Maze.BOUNDARY_TILES)
        self.add_block(((0,-11),(-1,-1)), Tile.DOT, ignore_type=Maze.BOUNDARY_TILES)
        self.add_blocks([((6,8),(6,-12)), ((-7,8),(-7,-12))], Tile.DOT)

def main():
    print('You are runnning maze.py as a python script')

    maze = Maze()
    maze.init()
    print(maze)

if __name__ == '__main__':
    main()