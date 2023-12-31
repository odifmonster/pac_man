#!/usr/bin/env python

from typing import Union, TypeAlias
from enum import Enum
import math

CoordVal: TypeAlias = Union[int, float]

class Direction(Enum):
    """Convenience class to have directions as separate types rather than hard-coded values."""

    E, NE, N, NW = 0, 1, 2, 3
    W, SW, S, SE = 4, 5, 6, 7

def get_dir_angle(dir: Direction) -> int:

    match dir:
        case Direction.E: return 0
        case Direction.NE: return 45
        case Direction.N: return 90
        case Direction.NW: return 135
        case Direction.W: return 180
        case Direction.SW: return 225
        case Direction.S: return 270
        case Direction.SE: return 315

def get_reverse(dir: Direction) -> Direction:
    
    dirs = list(Direction)
    dir_ind = dirs.index(dir)

    return dirs[(dir_ind+len(dirs)//2)%len(dirs)]

class Coord:
    """
    Generic class for coordinates and directional vectors including a couple convenience
    methods.
    
    Constructor method accepts either x+y values, a vector represented as a 2-length
    sequence, or a Direction indicating where the vector should point. Direction-based
    vectors always have abs(x) and abs(y) = 0 or 1.
    """

    def __init__(self, x: CoordVal = None, y: CoordVal = None,
                 v: tuple[CoordVal, CoordVal] = None,
                 dir: Direction = None) -> None:
        
        if not x is None and not y is None: # x+y args override all other present arguments
            self.x = x
            self.y = y
        elif not v is None: # v overrides subsequent args when no x+y passed
            self.x = v[0]
            self.y = v[1]
        elif not dir is None: # dir only used when no other args passed to constructor
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
        else: # raise error if Coord constructor called with invalid arguments
            raise ValueError('Too many NoneTypes passed to Coord constructor.')
    
    def __repr__(self) -> str:
        return f'(x: {self.x}, y: {self.y})'
    
    def __eq__(self, coord) -> bool:
        return self.x == coord.x and self.y == coord.y
    
    def __add__(self, coord):
        return type(self)(self.x+coord.x, self.y+coord.y)
    
    def __sub__(self, coord):
        return type(self)(self.x-coord.x, self.y-coord.y)
    
    def get_tuple(self) -> tuple:
        """Get vector components as 2-tuple of form (x,y)."""
        return (self.x, self.y)
    
    def dist_from(self, coord) -> float:
        """
        Arguments: coord (Coord) -- the Coord object to calculate the distance from
        Returns:         (float) -- the euclidean distance between this object and the coord argument
        """
        return math.sqrt((self.x-coord.x)**2+(self.y-coord.y)**2)
    
    def wrap(self, xmax: CoordVal, ymax: CoordVal,
             xmin: CoordVal = 0, ymin: CoordVal = 0, in_place: bool = True):
        """
        Arguments:
            xmax (CoordVal) -- maximum allowed x value (as float or int)
            ymax (CoordVal) -- maximum allowed y value
            xmin (CoordVal) -- (optional; default=0) minimum allowed x value
            ymin (CoordVal) -- (optional; default=0) minimum allowed y value
            in_place (bool) -- (optional; default=True) set this argument to false when you want
                               the function to return a new Coord object rather than change the
                               the current one.
        
        Returns:
            None when in_place is True. The Coord object will "wrap" its coordinates back around
            to be within the bounds set by xmin, xmax, ymin, and ymax (if necessary). When in_place
            is False, the function returns a new Coord object with the wrapped x and y values.
        """

        new_x = ((self.x-xmin) + (xmax-xmin)) % (xmax-xmin) + xmin
        new_y = ((self.y-ymin) + (ymax-ymin)) % (ymax-ymin) + ymin

        if not in_place:
            return type(self)(x=new_x, y=new_y)
        
        self.x = new_x
        self.y = new_y

class ListCoord(Coord):
    """
    Subclass of Coord for integer vector operations. Includes convenience functions for accessing
    elements from 2-D lists.
    """

    def __init__(self,
                 x: int = None, y: int = None,
                 v: tuple[int, int] = None,
                 dir: Direction = None,
                 coord: Coord = None) -> None:
        if not x is None and not y is None: super().__init__(int(x), int(y), v, dir)
        elif not coord is None and isinstance(coord, Coord): super().__init__(x=int(coord.x), y=int(coord.y))
        else: super().__init__(x, y, v, dir)
    
    def __add__(self, coord):
        return ListCoord(self.x+int(coord.x), self.y+int(coord.y))
    
    def get_adj(self, dir: Direction):
        """ Arguments: dir (Direction) -- the Direction of the adjacent tile
            Returns:   An adjacent ListCoord to this object in the specified direction
        """

        return self + ListCoord(dir=dir)
    
    def is_in_bounds(self, nrows: int, ncols: int) -> bool:
        """Return whether this list coordinate is within the bounds of nrows and ncols."""

        return self.x >= 0 and self.y >= 0 and self.x < ncols and self.y < nrows
    
    # Convenience functions to refer to x+y attributes as r(ow) and c(olumn)
    def getr(self):
        return self.y
    
    def getc(self):
        return self.x

class FloatCoord(Coord):
    """
    Subclass of Coord to represent floating point vector positions in the game. Probably just
    messy coding if we're being honest.
    """

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

        if self.x == 0 and self.y < 0: return Direction.N
        if self.x < 0 and self.y == 0: return Direction.W
        if self.x == 0 and self.y > 0: return Direction.S
        if self.x > 0 and self.y == 0: return Direction.E

        return None
    
    def __mul__(self, scale: float):
        return FloatCoord(self.x*scale, self.y*scale)
    
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