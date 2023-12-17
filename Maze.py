#!/usr/bin/env python

from enum import Enum

import position

class TileType(Enum):
    OPEN = '-'
    EDGE = 'E'
    WALL = 'W'
    GHOST = 'G'

    def __repr__(self) -> str:
        return self.value
    
    def __str__(self) -> str:
        return self.__repr__()

class DotType(Enum):
    EMPTY = '-'
    NORMAL = 'D'
    BLINK = 'B'

class Maze:

    def __init__(self, rows: int = 32, cols: int = 29) -> None:
        self.size = position.IntCoord(rows, cols)
        self.list_rep = [[TileType.OPEN for _ in range(cols)] for _ in range(rows)]
        self.dots = [[DotType.EMPTY for _ in range(cols)] for _ in range(rows)]
    
    def __repr__(self) -> str:
        return '\n'.join([''.join([str(t) for t in s]) for s in self.list_rep])
    
    def get_tile(self, pos: position.IntCoord) -> TileType:
        return self.list_rep[pos.r][pos.c]
    
    def get_dot(self, pos: position.IntCoord) -> DotType:
        return self.dots[pos.r][pos.c]
    
    def set_dot(self, pos: position.IntCoord, dot: DotType) -> None:
        self.dots[pos.r][pos.c] = dot
    
    def get_tile_lines(self, pos: position.IntCoord, t_size: int) -> list[position.Block]:
        if self.get_tile(pos) == TileType.OPEN:
            return []
        
        lines = []
        if pos.r < self.size.r-1 and self.list_rep[pos.r+1][pos.c] == TileType.OPEN:
            start = position.FloatCoord(x=pos.c*t_size,y=(pos.r+1)*t_size-1)
            end = position.FloatCoord(x=(pos.c+1)*t_size-1,y=(pos.r+1)*t_size-1)
            lines.append((start, end))
        if pos.r > 0 and self.list_rep[pos.r-1][pos.c] == TileType.OPEN:
            start = position.FloatCoord(x=pos.c*t_size,y=pos.r*t_size)
            end = position.FloatCoord(x=(pos.c+1)*t_size-1,y=pos.r*t_size)
            lines.append((start, end))
        if pos.c < self.size.c-1 and self.list_rep[pos.r][pos.c+1] == TileType.OPEN:
            start = position.FloatCoord(x=(pos.c+1)*t_size-1,y=pos.r*t_size)
            end = position.FloatCoord(x=(pos.c+1)*t_size-1,y=(pos.r+1)*t_size-1)
            lines.append((start, end))
        if pos.c > 0 and self.list_rep[pos.r][pos.c-1] == TileType.OPEN:
            start = position.FloatCoord(x=pos.c*t_size,y=pos.r*t_size)
            end = position.FloatCoord(x=pos.c*t_size,y=(pos.r+1)*t_size-1)
            lines.append((start, end))
        
        return lines
    
    def add_block(self, block: position.Block, btype: TileType) -> None:

        start, end = block

        if not isinstance(start, position.IntCoord) or not isinstance(end, position.IntCoord):
            start = position.IntCoord(start[0], start[1])
            end = position.IntCoord(end[0], end[1])
        
        start.wrap(self.size.r, self.size.c)
        end.wrap(self.size.r, self.size.c)

        for r in range(start.r, end.r+1):
            for c in range(start.c, end.c+1):
                self.list_rep[r][c] = btype
    
    def add_blocks(self, block_list: list[position.Block], btype: TileType) -> None:

        for block in block_list:
            self.add_block(block, btype)
    
    def initialize(self):
        edge_list = [
            ((0,0),(0,-1)),
            ((0,0),(10,0)), ((10,0),(13,5)),
            ((16,0),(19,5)), ((19,0),(-1,0)),
            ((-1,0),(-1,-1)), ((16,-6), (19,-1)), ((19,-1),(-1,-1)),
            ((0,-1),(10,-1)), ((10,-6),(13,-1)), 
            ((13,self.size.c//2-3),(13,self.size.c//2+3)),
            ((13,self.size.c//2-3),(16,self.size.c//2-3)),
            ((16,self.size.c//2-3),(16,self.size.c//2+3)),
            ((13,self.size.c//2+3),(16,self.size.c//2+3))
        ]
        self.add_blocks(edge_list, TileType.EDGE)

        self.add_block(((13,self.size.c//2-3),(16,self.size.c//2+3)), TileType.EDGE)
        self.add_block(((14,self.size.c//2-2),(15,self.size.c//2+2)), TileType.GHOST)
        self.add_block(((13,self.size.c//2-1),(13,self.size.c//2+1)), TileType.GHOST)

        wall_list = [
            ((3,3),(4,5)), ((3,8),(4,11)), ((1,self.size.c//2),(4,self.size.c//2)),
            ((3,-6),(4,-4)), ((3,-12),(4,-9)), ((7,3),(7,5)), ((7,-6),(7,-4)),
            ((7,8),(13,8)), ((7,-9),(13,-9)), ((7,11),(7,-12)),
            ((10,8),(10,11)), ((10,-12),(10,-9)), ((7,self.size.c//2),(10,self.size.c//2)),
            ((16,8),(19,8)), ((16,-9),(19,-9)),
            ((19,self.size.c//2-3),(19,self.size.c//2+3)),((19,self.size.c//2),(22,self.size.c//2)),
            ((-4,3),(-4,self.size.c//2-3)), ((-7,8),(-4,8)), ((-4,self.size.c//2+3),(-4,-4)),
            ((-7,-9),(-4,-9)), ((-7,1),(-7,2)), ((-7,-3),(-7,-2)),
            ((-7,self.size.c//2-3),(-7, self.size.c//2+3)), ((-7,self.size.c//2),(-4,self.size.c//2)),
            ((-10,3),(-10,5)), ((-10,5),(-7,5)), ((-10,8),(-10,self.size.c//2-3)),
            ((-10,-6),(-10,-4)), ((-10,-6),(-7,-6)), ((-10,self.size.c//2+3),(-10,-9))
        ]
        self.add_blocks(wall_list, TileType.WALL)

        for r in range(1,self.size.r):
            for c in range(1,self.size.c):
                cur = position.IntCoord(r,c)
                up = cur.get_adj(position.Direction.UP)
                up_left = up.get_adj(position.Direction.LEFT)
                left = cur.get_adj(position.Direction.LEFT)

                dot_space = True
                for tile in (cur, up, up_left, left):
                    if self.get_tile(tile) != TileType.OPEN:
                        dot_space = False
                
                if dot_space:
                    self.dots[r][c] = DotType.NORMAL

def main():
    m = Maze()
    m.initialize()
    print(m)

if __name__ == '__main__':
    main()