#!/usr/bin/env python
from typing import TypeAlias, Union
from enum import Enum
import math

class Direction(Enum):
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

class IntCoord:

    def __init__(self, r: int, c: int) -> None:
        self.r = r
        self.c = c
    
    def get_tuple(self) -> tuple[int, int]:
        return (self.r, self.c)
    
    def wrap(self, max_r, max_c) -> None:
        if self.r < 0:
            self.r += max_r
        if self.c < 0:
            self.c += max_c
    
    def get_adj(self, dir: Direction):
        if dir == Direction.UP:
            return IntCoord(self.r-1, self.c)
        if dir == Direction.DOWN:
            return IntCoord(self.r+1, self.c)
        if dir == Direction.LEFT:
            return IntCoord(self.r, self.c-1)
        if dir == Direction.RIGHT:
            return IntCoord(self.r, self.c+1)
    
    def dist_from(self, coord) -> float:
        return math.sqrt((self.r-coord.r)**2 + (self.c-coord.c)**2)

class FloatCoord:

    def __init__(self, x= 0.0, y= 0.0, dir = None) -> None:
        if not dir is None:
            if dir == Direction.UP:
                self.x, self.y = 0, -1
            elif dir == Direction.DOWN:
                self.x, self.y = 0, 1
            elif dir == Direction.LEFT:
                self.x, self.y = -1, 0
            else:
                self.x, self.y = 1, 0
        else:
            self.x = x
            self.y = y
    
    def get_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def get_direction(self) -> Direction:
        if self.x == 0 and self.y > 0:
            return Direction.DOWN
        if self.x == 0 and self.y < 0:
            return Direction.UP
        if self.x > 0 and self.y == 0:
            return Direction.RIGHT
        if self.x < 0 and self.y == 0:
            return Direction.LEFT
    
    def __repr__(self) -> str:
        return f'(x: {self.x}, y: {self.y})'
    
Coord: TypeAlias = Union[IntCoord, FloatCoord, tuple[int,int], tuple[float,float]]
Block: TypeAlias = Union[list[Coord, Coord], tuple[Coord, Coord]]
