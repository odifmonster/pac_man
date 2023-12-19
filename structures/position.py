#!/usr/bin/env python

from typing import Union, TypeAlias
from enum import Enum
import math

CoordVal: TypeAlias = Union[int, float]

class Direction(Enum):
    """Enum for the four relative directions to avoid hard-coding."""

    N, W, S, E = 0, 1, 2, 3
    NW, NE, SE, SW = 4, 5, 6, 7

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
            match dir:
                case Direction.N:
                    self.x, self.y = 0, -1
                case Direction.S:
                    self.x, self.y = 0, 1
                case Direction.E:
                    self.x, self.y = 1, 0
                case Direction.W:
                    self.x, self.y = -1, 0
                case Direction.NE:
                    self.x, self.y = 1, -1
                case Direction.NW:
                    self.x, self.y = -1, -1
                case Direction.SE:
                    self.x, self.y = 1, 1
                case Direction.SW:
                    self.x, self.y = -1, 1
                case _:
                    raise ValueError('Unrecognized direction.')
        else:
            raise ValueError('Coord constructor cannot be called on all NoneTypes.')
    
    def get_tuple(self) -> tuple:
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
    
    def add(self, coord):
        return ListCoord(self.x+coord.x, self.y+int(coord.y))
    
    def get_adj(self, dir: Direction):
        """Get the adjacent coordinate in the given direction."""

        return self.add(Coord(dir=dir))
    
    def is_in_bounds(self, nrows: int, ncols: int) -> bool:
        """Return whether this list coordinate is within the bounds of the given rows and cols."""

        return self.x >= 0 and self.y >= 0 and self.x < ncols and self.y < nrows
    
    def getr(self):
        return self.y
    
    def getc(self):
        return self.x

class FloatCoord(Coord):
    """Class for coordinates that refer to relative grid positions in the display rather than a list."""

    def __init__(self,
                 x: CoordVal = None, y: CoordVal = None,
                 v: tuple[CoordVal, CoordVal] = None,
                 dir: Direction = None,
                 coord: Coord = None) -> None:
        
        if not coord is None:
            self.x = coord.x
            self.y = coord.y
        else:
            super().__init__(x, y, v, dir)

    def get_direction(self) -> Direction:
        """Get the Direction that this coordinate points in."""

        if self.x == 0 and self.y == -1: return Direction.N
        if self.x == -1 and self.y == 0: return Direction.W
        if self.x == 0 and self.y == 1: return Direction.S
        if self.x == 1 and self.y == 0: return Direction.E

        return None
    
    def __add__(self, coord):
        return FloatCoord(self.x+coord.x, self.y+coord.y)
    
    def __sub__(self, coord):
        return FloatCoord(self.x-coord.x, self.y-coord.y)
    
    def midpoint_to(self, coord):
        return FloatCoord((self.x+coord.x)/2, (self.y+coord.y)/2)

CoordLike: TypeAlias = Union[Coord, list[CoordVal, CoordVal], tuple[CoordVal, CoordVal]]
Block: TypeAlias = Union[tuple[CoordLike, CoordLike], list[CoordLike, CoordLike]]

ZERO = FloatCoord(0, 0)

def main():
    test = ListCoord(4,5)
    print(test.get_adj(Direction.N), test.get_adj(Direction.E), test.get_adj(Direction.NE))

if __name__ == '__main__':
    main()