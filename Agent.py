#!/usr/bin/env python
import os
import math
import pygame

from Maze import Maze
pygame.init()

from Maze import *
import position

MOVE_MAT = [
    [1,0],
    [0,1]
]

class Agent:

    def __init__(self,
                 start_pos: position.IntCoord,
                 speed: position.FloatCoord,
                 speed_norm: float,
                 size: int = 2):
        
        self.maze_pos = start_pos
        self.pos = position.FloatCoord(x=start_pos.c,y=start_pos.r)
        self.size = size

        self.speed = speed
        self.speed_norm = speed_norm

        self.passable_tiles = [TileType.OPEN]
    
    def can_move(self, maze: Maze, speed: position.FloatCoord) -> bool:

        for r in range(self.maze_pos.r,self.maze_pos.r+self.size):
            for c in range(self.maze_pos.c,self.maze_pos.c+self.size):
                p = position.IntCoord(r, c)
                adj = p.get_adj(speed.get_direction())

                if adj.c >= 0 and adj.c < maze.size.c and maze.get_tile(adj) not in self.passable_tiles:
                    return False
        
        return True
    
    def move(self, maze: Maze) -> None:

        res = [0,0]
            
        for i in range(len(MOVE_MAT)):
            speed_tup = self.speed.get_tuple()

            for k in range(len(speed_tup)):
                res[i] += MOVE_MAT[i][k]*speed_tup[k]*self.speed_norm
            
        self.pos.x += res[0]
        self.pos.y += res[1]

        if self.speed.get_direction() == position.Direction.UP:
            self.maze_pos.r = math.ceil(self.pos.y)
            self.pos.x = self.maze_pos.c
        elif self.speed.get_direction() == position.Direction.DOWN:
            self.maze_pos.r = math.floor(self.pos.y)
            self.pos.x = self.maze_pos.c
        elif self.speed.get_direction() == position.Direction.LEFT:
            self.maze_pos.c = math.ceil(self.pos.x)
            self.pos.y = self.maze_pos.r
        elif self.speed.get_direction() == position.Direction.RIGHT:
            self.maze_pos.c = math.floor(self.pos.x)
            self.pos.y = self.maze_pos.r
        
        self.maze_pos.c = (self.maze_pos.c + maze.size.c) % maze.size.c
        self.pos.x = (self.pos.x + 1 + maze.size.c) % maze.size.c - 1
    
class Player(Agent):

    def __init__(self,
                 start_pos: position.IntCoord,
                 speed: position.FloatCoord,
                 speed_norm: float,
                 img_path: os.PathLike):
        
        super().__init__(start_pos, speed, speed_norm)

        self.next_speed: position.FloatCoord = None
        self.is_moving = True

        self.images = [pygame.image.load(os.path.join(img_path,file)) for file in os.listdir(img_path)
                        if 'pacman' in file and '.png' in file]
        self.frame_rate = 2
    
    def move(self, maze: Maze):

        super().move(maze)

        br = self.maze_pos.get_adj(position.Direction.DOWN).get_adj(position.Direction.RIGHT)
        if not br.c < 0 and not br.c >= maze.size.c:
            maze.set_dot(br, DotType.EMPTY)

        self.is_moving = True
    
    def update_pos(self, maze: Maze):

        if not self.next_speed is None:
            if self.can_move(maze, self.next_speed):
                self.speed = self.next_speed
                self.next_speed = None
                self.move(maze)
                return
            elif not self.can_move(maze, self.next_speed) and self.can_move(maze, self.speed):
                self.move(maze)
                return
        elif self.can_move(maze, self.speed):
            self.move(maze)
            return
        
        self.is_moving = False
    
    def get_image(self, nframes) -> list[pygame.Surface]:
        rotation = {
            position.Direction.UP: 90,
            position.Direction.LEFT: 180,
            position.Direction.DOWN: 270,
            position.Direction.RIGHT: 0,
        }

        if not self.is_moving:
            img_ind = 0
        else:
            img_ind = (nframes // self.frame_rate) % len(self.images)

        return pygame.transform.rotate(self.images[img_ind], rotation[self.speed.get_direction()])
    
class Enemy(Agent):

    def __init__(self,
                 start_pos: position.IntCoord,
                 speed: position.FloatCoord,
                 speed_norm: float):
        
        super().__init__(start_pos, speed, speed_norm)

        self.passable_tiles = [TileType.OPEN, TileType.GHOST]
        self.next_speed = None
        self.target_pos = start_pos
    
    def update_pos(self, maze: Maze, player: Player, nframes: int, frame_rate: int):

        if self.target_pos == self.maze_pos or not self.can_move(maze, self.speed):
            if nframes <= frame_rate*2:
                target = position.IntCoord(11, maze.size.c//2-1)
            else:
                target = player.maze_pos

            dirs = [position.Direction.UP,
                    position.Direction.RIGHT,
                    position.Direction.DOWN,
                    position.Direction.LEFT]
        
            mindist = maze.size.r+maze.size.c+1
            bestdir = self.speed.get_direction()

            for d in dirs:
                if self.can_move(maze, position.FloatCoord(dir=d)):
                    dist = self.maze_pos.get_adj(d).dist_from(target)

                    if dist < mindist:
                        mindist = dist
                        bestdir = d
        
            self.speed = position.FloatCoord(dir=bestdir)
            self.target_pos.r = self.maze_pos.r+self.speed.y
            self.target_pos.c = self.maze_pos.c+self.speed.x
            super().move(maze)

def main():
    m = Maze()
    m.initialize()

    up = position.FloatCoord(x=0,y=-1)
    down = position.FloatCoord(x=0,y=1)
    left = position.FloatCoord(x=-1,y=0)
    right = position.FloatCoord(x=1,y=0)

    test_agent = Agent(
        position.IntCoord(m.size.r-9, m.size.c//2-1),
        position.FloatCoord(x=-1,y=0),
        0.7,
        (255,255,0),
        'gfx'
    )

    print(test_agent.can_move(m, up))
    print(test_agent.can_move(m, down))
    print(test_agent.can_move(m, left))
    print(test_agent.can_move(m, right))

if __name__ == '__main__':
    main()