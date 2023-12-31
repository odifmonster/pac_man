#!/usr/bin/env python
from enum import Enum
from typing import Sequence
from pygame import Rect

from structures.position import *

class Tile(Enum):

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
    
    def get_tile(self, pos: Coord) -> Tile:
        
        if not pos.has_int_vals():
            raise ValueError('Tile coordinates of maze must use integer values.')
        
        if pos.y == 14 and (pos.x < 6 or pos.x >= self.ncols-6):
            pos.wrap(self.ncols, self.nrows)

        if not pos.is_in_bounds(self.nrows, self.ncols):
            return Tile.OOB
        
        return self.tiles[pos.y][pos.x]
    
    def set_tile(self, pos: Coord, ttype: Tile) -> None:
        
        if not pos.has_int_vals() or not pos.is_in_bounds(self.nrows, self.ncols):
            raise ValueError('Invalid position coordinates passed to Maze.set_tile()')

        self.tiles[pos.y][pos.x] = ttype

    def get_tile_rects(self, pos: Coord, tsize: int) -> list[Rect]:
        
        if not pos.has_int_vals() or not pos.is_in_bounds(self.nrows, self.ncols):
            raise IndexError('Invalid position coordinates passed to Maze.get_tile_rects()')
        
        if self.get_tile(pos) != Tile.EDGE:
            return []
        
        moves = Direction.list_in_order()
        rects = []
        float_pos = Coord(x=pos.x*tsize, y=pos.y*tsize)

        for move in moves:
            adj = pos.get_adj(move)

            if self.get_tile(adj) not in Maze.BOUNDARY_TILES:
                tl = float_pos.midpoint_to(Coord(x=adj.x*tsize, y=adj.y*tsize))
                rects.append(Rect(tl.x, tl.y, tsize, tsize))
        
        tile_rect = Rect(float_pos.x, float_pos.y, tsize, tsize)

        return [rect.clip(tile_rect) for rect in rects]

    # ================== MAZE INITIALIZATION ==================

    def add_block(self, block: Block, ttype: Tile, ignore_type: Sequence[Tile] = []) -> None:

        lblock = list(block)

        for i, arg in enumerate(lblock):
            if not type(arg) is Vector:
                if type(arg) in (tuple, list) and len(arg) == 2:
                    lblock[i] = Coord(x=arg[0], y=arg[1])
                else:
                    raise TypeError('block argument for Maze.add_block() must be a Block (see structures.position.Block)')
                
        start, end = lblock
        
        start.wrap(self.ncols, self.nrows)
        end.wrap(self.ncols, self.nrows)
        
        for r in range(start.y, end.y+1):
            for c in range(start.x, end.x+1):
                pos = Coord(x=c, y=r)

                if self.get_tile(pos) not in ignore_type:
                    self.set_tile(Coord(x=c,y=r), ttype)
    
    def add_blocks(self, blocks: list[Block], ttype: Tile) -> None:

        for block in blocks:
            self.add_block(block, ttype)

    def init(self) -> None:
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