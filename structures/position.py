#!/usr/bin/env python

from enum import Enum
from typing import assert_never, Self, TypeAlias, Union
import math

class Direction(Enum):

    N, E, S, W = 0, 1, 2, 3
    NE, NW, SE, SW = 4, 5, 6, 7

    @classmethod
    def get_angle(cls, d: Self) -> int:

        match d:
            case cls.E: return 0
            case cls.NE: return 45
            case cls.N: return 90
            case cls.NW: return 135
            case cls.W: return 180
            case cls.SW: return 225
            case cls.S: return 270
            case cls.SE: return 315
            case _ as unreachable:
                assert_never(unreachable)
    
    @classmethod
    def get_reverse(cls, d: Self) -> Self:

        match d:
            case cls.E: return cls.W
            case cls.NE: return cls.SW
            case cls.N: return cls.S
            case cls.NW: return cls.SE
            case cls.W: return cls.E
            case cls.SW: return cls.NE
            case cls.S: return cls.N
            case cls.SE: return cls.NW
            case _ as unreachable:
                assert_never(unreachable)
    
    @classmethod
    def list_in_order(cls) -> list[Self]:

        return [cls.E, cls.NE, cls.N, cls.NW, cls.W, cls.SW, cls.S, cls.SE]

class Vector:

    def __init__(self, x: float = None, y: float = None,
                 v: tuple[float, float] = None,
                 d: Direction = None,
                 vec: Self = None) -> None:
        
        if not (x is None and y is None):
            try:
                self.x, self.y = float(x), float(y)
            except ValueError:
                raise TypeError('x and y args for Vector constructor must be castable to float.')
        elif not v is None:
            if not type(v) in (list, tuple):
                raise TypeError('v arg for Vector constructor must be a 2-length list or 2-tuple.')
            elif not len(v) == 2:
                raise ValueError('v arg for Vector constructor must be a 2-length list or 2-tuple.')
            else:
                try:
                    self.x, self.y = float(v[0]), float(v[1])
                except ValueError:
                    raise TypeError('elements of v arg for Vector constructor must be castable to floats.')
        elif not d is None:
            if not type(d) is Direction:
                raise TypeError('d arg for Vector constructor must be a Direction.')
            else:
                theta = 2 * math.pi * Direction.get_angle(d) / 360
                self.x, self.y = math.cos(theta), math.sin(theta)
                if self.x != 0: self.x /= abs(self.x)
                if self.y != 0: self.y /= abs(self.y)
        elif not vec is None:
            if not type(vec) is Self:
                raise TypeError('vec arg for Vector constructor must be a Vector.')
            else:
                self.x, self.y = vec.x, vec.y
        else:
            raise ValueError('Vector object cannot be instantiated with all NoneType arguments.')
    
    def __repr__(self) -> str:
        return f'({self.x:.1}, {self.y:.1})'
    
    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other: Self) -> Self:
        return type(self)(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other: Self) -> Self:
        return type(self)(self.x-other.x, self.y-other.y)
    
    def __mul__(self, coeff: float) -> Self:
        return type(self)(self.x*coeff, self.y*coeff)
    
    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def wrap(self, xmax: float, ymax: float,
             xmin: float = 0.0, ymin: float = 0.0,
             in_place: bool = True) -> None | Self:
        
        new_x = ((self.x-xmin) + (xmax-xmin)) % (xmax-xmin) + xmin
        new_y = ((self.y-ymin) + (ymax-ymin)) % (ymax-ymin) + ymin

        if not in_place:
            return type(self)(x=new_x, y=new_y)
        
        self.x, self.y = new_x, new_y
    
    def get_adj(self, d: Direction) -> Self:
        return self + type(self)(d=d)
    
    def get_direction(self) -> Direction:
        
        if self.x == 0 and self.y < 0: return Direction.N
        elif self.x > 0 and self.y == 0: return Direction.E
        elif self.x == 0 and self.y > 0: return Direction.S
        elif self.x < 0 and self.y == 0: return Direction.W
        else:
            raise ValueError('Cannot get direction of Vector pointing in non-cardinal Direction.')
    
    def is_in_bounds(self, nrows: int, ncols: int) -> bool:
        return self.x >= 0 and self.x <= ncols-1 and self.y >= 0 and self.y <= nrows-1
    
    def has_int_vals(self) -> bool:
        return int(self.x) == self.x and int(self.y) == self.y
    
    def dist_from(self, other: Self) -> float:
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
    
    def midpoint_to(self, other: Self) -> Self:
        return type(self)(0.5*(self.x+other.x), 0.5*(self.y+other.y))

Coord: TypeAlias = Vector
VectorLike: TypeAlias = Union[Vector, tuple[float, float], list[float, float]]
Block: TypeAlias = Union[tuple[VectorLike, VectorLike], list[VectorLike, VectorLike]]

ZERO = Vector(0,0)