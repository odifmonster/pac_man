#!/usr/bin/env python

from typing import Union, TypeAlias
from enum import Enum
import math

CoordVal: TypeAlias = Union[int, float]

class Direction(Enum):
    """Enum for the four relative directions to avoid hard-coding."""

    UP, LEFT, DOWN, RIGHT = 0, 1, 2, 3

class Coord:
    """Base class for coordinates and directional vectors."""

    def __init__(self, x: CoordVal = None, y: CoordVal = None,
                 v: tuple[CoordVal, CoordVal] = None,
                 dir: Direction = None) -> None:
        
        if not x is None and not y is None:
            self.x = x
            self.y = y
        elif not v is None:
            self.x = v[0]
            self.y = v[1]
        elif not dir is None:
            if dir == Direction.UP: self.x, self.y = 0, -1
            elif dir == Direction.LEFT: self.x, self.y = -1, 0
            elif dir == Direction.DOWN: self.x, self.y = 0, 1
            elif dir == Direction.RIGHT: self.x, self.y = 1, 0
        else:
            raise ValueError('Coord constructor cannot be called on all NoneTypes.')
    
    def get_tuple(self):
        """Get vector components as 2-tuple."""
        return (self.x, self.y)
    
    def dist_from(self, coord) -> float:
        """Get this Coord's Euclidean distance from another Coord."""
        return math.sqrt((self.x-coord.x)**2+(self.y-coord.y)**2)
    
    def wrap(self, xmax, ymax, buffer=0):
        """Allow overflow to wrap around given bounding area of coordinate."""
        if self.x < 0-buffer:
            self.x += xmax
        if self.y < 0-buffer:
            self.y += ymax
        if self.x >= xmax + buffer:
            self.x -= xmax
        if self.y >= ymax + buffer:
            self.y -= ymax
    
    def __repr__(self) -> str:
        return f'(x: {self.x}, y: {self.y})'

class ListCoord(Coord):

    def __init__(self, x: int = None, y: int = None, v: tuple[int, int] = None, dir: Direction = None) -> None:
        super().__init__(x, y, v, dir)
    
    def get_adj(self, dir: Direction):
        """Get the adjacent coordinate in the given direction."""

        if dir == Direction.UP: return ListCoord(self.x,self.y-1)
        if dir == Direction.LEFT: return ListCoord(self.x-1,self.y)
        if dir == Direction.DOWN: return ListCoord(self.x,self.y+1)
        if dir == Direction.RIGHT: return ListCoord(self.x+1,self.y)
    
    def is_in_bounds(self, nrows: int, ncols: int) -> bool:
        """Return whether this list coordinate is within the bounds of the given rows and cols."""

        return self.x >= 0 and self.y >= 0 and self.x < ncols and self.y < nrows

class FloatCoord(Coord):
    """Class for coordinates that refer to relative grid positions in the display rather than a list."""

    def __init__(self, x: CoordVal = None, y: CoordVal = None, v: tuple[CoordVal, CoordVal] = None, dir: Direction = None) -> None:
        super().__init__(x, y, v, dir)

    def get_direction(self) -> Direction:
        """Get the Direction that this coordinate points in."""

        if self.x == 0 and self.y == -1: return Direction.UP
        if self.x == -1 and self.y == 0: return Direction.LEFT
        if self.x == 0 and self.y == 1: return Direction.DOWN
        if self.x == 1 and self.y == 0: return Direction.RIGHT

        return None

CoordLike: TypeAlias = Union[Coord, list[CoordVal, CoordVal], tuple[CoordVal, CoordVal]]
Block: TypeAlias = Union[tuple[CoordLike, CoordLike], list[CoordLike, CoordLike]]