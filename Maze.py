#!/usr/bin/env python

from enum import Enum

from position import *

class Tile(Enum):
    """Enum for holding tile types and equivalent strings"""

    EMPTY, DOT, EDGE, OOB, GHOST_WALL = '-', 'o', 'E', 'X', 'G'

    def __repr__(self) -> str:
        return self.value
    
    def __str__(self) -> str:
        return self.__repr__()

class Maze:

    def __init__(self, nrows: int = 31, ncols: int = 28) -> None:
        self.tiles = [[Tile.EMPTY for _ in range(ncols)] for _ in range(nrows)]
        self.nrows = nrows
        self.ncols = ncols
    
    def __repr__(self) -> str:
        return '\n'.join([''.join([str(t) for t in row]) for row in self.tiles])
    
    def set_tile(self, pos: ListCoord, ttype: Tile):
        self.tiles[pos.y][pos.x] = ttype
    
    def add_block(self, block: Block, ttype: Tile) -> None:

        start, end = block

        if not isinstance(start, ListCoord):
            start = ListCoord(x=start[0], y=start[1])
        if not isinstance(end, ListCoord):
            end = ListCoord(x=end[0], y=end[1])
        
        start.wrap(self.ncols, self.nrows)
        end.wrap(self.ncols, self.nrows)
        
        for r in range(start.y, end.y+1):
            for c in range(start.x, end.x+1):
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
            ((2,-10),(5,-9)), ((4,-10),(5,-6)), ((-6,-10),(-3,-9)), ((-6,-10),(-5,-6))
        ]
        self.add_blocks(bottom_walls, Tile.EDGE)

def main():
    print('You are runnning maze.py as a python script')

    maze = Maze()
    maze.init()
    print(maze)

if __name__ == '__main__':
    main()