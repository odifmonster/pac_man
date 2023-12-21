#!/usr/bin/env python
import os
from pygame.image import load
import math

from structures.maze import *
from structures.position import *

class Agent:

    def __init__(self, list_pos: CoordLike, speed_vec: CoordLike = (0,0), speed_norm: float = 1):

        if isinstance(list_pos, ListCoord):
            self.list_pos = list_pos
        elif type(list_pos) in (tuple, list):
            self.list_pos = ListCoord(list_pos[0], list_pos[1])
        else:
            raise TypeError('Invalid position argument passed to Agent constructor.')
        
        self.pos = FloatCoord(coord=self.list_pos)
        
        if isinstance(speed_vec, Coord):
            self.speed_vec = FloatCoord(coord=speed_vec)
        elif type(speed_vec) in (tuple, list):
            self.speed_vec = FloatCoord(speed_vec[0], speed_vec[1])
        else:
            raise TypeError('Invalid speed argument passed to Agent constructor.')
        
        self.speed_norm = speed_norm

        self.passable_tiles = list(Tile)
    
    def move(self, maze: Maze, speed_vec: FloatCoord, speed_norm: float) -> None:

        self.pos += (speed_vec*speed_norm)
        self.pos.wrap(maze.ncols+0.5, maze.nrows, -0.5, 0)

        speed_dir = speed_vec.get_direction()
        if speed_dir == Direction.N:
            self.list_pos.y = math.ceil(self.pos.y)
            self.pos.x = self.list_pos.x
        if speed_dir == Direction.S:
            self.list_pos.y = math.floor(self.pos.y)
            self.pos.x = self.list_pos.x
        if speed_dir == Direction.E:
            self.list_pos.x = math.floor(self.pos.x)
            self.pos.y = self.list_pos.y
        if speed_dir == Direction.W:
            self.list_pos.x = math.ceil(self.pos.x)
            self.pos.y = self.list_pos.y
    
    def can_move(self, maze: Maze, speed: FloatCoord):

        return maze.get_tile(self.list_pos.get_adj(speed.get_direction())) in self.passable_tiles

    def get_center(self):

        return self.pos + FloatCoord(0.5, 0.5)
    
    def get_tl(self):

        return self.pos - FloatCoord(0.5, 0.5)

class Player(Agent):

    def __init__(self,
                 list_pos: CoordLike,
                 speed_vec: CoordLike = (0,0),
                 speed_norm: float = 1,
                 chomp_rate: int = 3):
        
        super().__init__(list_pos, speed_vec, speed_norm)

        self.chomp_rate = chomp_rate
        self.eating = False
        self.last_dot = ListCoord(0,0)

        self.images = sorted([f for f in os.listdir('gfx') if 'pacman' in f and '.png' in f])
        self.images = [load(os.path.join('gfx', img)) for img in self.images]

        self.next_speed = None
        self.is_moving = False

        self.passable_tiles = [Tile.EMPTY, Tile.DOT]
    
    def move(self, maze: Maze) -> None:
        super().move(maze, self.speed_vec, self.speed_norm)

        if maze.get_tile(self.list_pos) == Tile.DOT:
            maze.set_tile(self.list_pos, Tile.EMPTY)
            self.last_dot.x, self.last_dot.y = self.list_pos.x, self.list_pos.y
            self.eating = True
        elif self.list_pos != self.last_dot or not self.is_moving:
            self.eating = False
    
    def update_pos(self, maze: Maze) -> None:

        if not self.next_speed is None and self.can_move(maze, self.next_speed):
            self.speed_vec = self.next_speed
            self.next_speed = None
            self.is_moving = True
            self.move(maze)
        elif self.can_move(maze, self.speed_vec):
            self.move(maze)
            self.is_moving = True
        else:
            self.is_moving = False
    
    def get_image(self, nframes):

        if not self.is_moving: return self.images[-1]

        return self.images[(nframes // self.chomp_rate) % len(self.images)]

class Enemy(Agent):

    def __init__(self, 
                 gfx_path: os.PathLike,
                 list_pos: CoordLike, 
                 speed_vec: CoordLike = (0, 0), 
                 speed_norm: float = 1,
                 speed_reduction: float = 0.6,
                 wave_rate: int = 6):
        
        super().__init__(list_pos, speed_vec, speed_norm)

        self.slow_norm = speed_norm*speed_reduction
        self.passable_tiles = [Tile.EMPTY, Tile.DOT]

        self.gfx_path = gfx_path
        imgs = sorted(os.listdir(gfx_path))
        self.images = [(os.path.join(gfx_path, imgs[2*i]), os.path.join(gfx_path, imgs[2*i+1])) 
                       for i in range(len(imgs)//2)]
        self.images = [(load(w0), load(w1)) for w0, w1 in self.images]
        self.wave_rate = wave_rate

    def move(self, maze: Maze) -> None:

        if self.list_pos.y == 14 and (self.list_pos.x < 6 or self.list_pos.x >= maze.ncols-6):
            super().move(maze, self.speed_vec, self.slow_norm)
        else:
            super().move(maze, self.speed_vec, self.speed_norm)
    
    def get_turns(self, maze: Maze):

        return [d for d in list(Direction)[::2] if self.can_move(maze, FloatCoord(dir=d))]
    
    def update_speed(self, maze: Maze, player: Player):

        turns = self.get_turns(maze)
        if not self.can_move(maze, self.speed_vec) or len(turns) > 2:

            mindist = maze.nrows+maze.ncols+1
            best_turn = self.speed_vec
            for turn in turns:

                if turn != get_reverse(self.speed_vec.get_direction()):
                    curdist = self.list_pos.get_adj(turn).dist_from(player.list_pos)

                    if curdist < mindist:
                        mindist = curdist
                        best_turn = turn
            
            self.speed_vec = FloatCoord(dir=best_turn)
    
    def get_image(self, nframes, start_frame):

        if nframes < start_frame:
            return self.images[0][0]

        angle_ind = get_dir_angle(self.speed_vec.get_direction()) // 90
        angle_pair = self.images[angle_ind]
        wave = (nframes // self.wave_rate) % len(angle_pair)
        
        return angle_pair[wave]
