#!/usr/bin/env python

import pygame

import Maze, Agent
import position

pygame.init()

def main():
    TILE_SIZE = 18

    maze = Maze.Maze()
    maze.initialize()

    pacman = Agent.Player(
        position.IntCoord(maze.size.r-9, maze.size.c//2-1),
        position.FloatCoord(-1,0),
        0.17,
        'gfx'
    )

    blinky = Agent.Enemy(
        position.IntCoord(14, maze.size.c//2-1),
        position.FloatCoord(0,-1),
        0.17
    )
    
    screen = pygame.display.set_mode((maze.size.c*TILE_SIZE,maze.size.r*TILE_SIZE))
    clock = pygame.time.Clock()

    nframes = 0
    frame_rate = 40
    running = True
    while running:
        
        screen.fill((0,0,0))

        for r in range(maze.size.r):
            for c in range(maze.size.c):
                tile_rect = pygame.Rect((c*TILE_SIZE, r*TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pos = position.IntCoord(r, c)
                
                pygame.draw.rect(screen, (0,0,0), tile_rect)
                lines = maze.get_tile_lines(pos, TILE_SIZE)

                line_color = (0,0,255)
                if maze.get_tile(pos) == Maze.TileType.GHOST:
                    line_color = (255,128,255)

                for line in lines:
                    pygame.draw.line(screen, line_color, line[0].get_tuple(), line[1].get_tuple())
                
                if maze.get_dot(pos) == Maze.DotType.NORMAL:
                    pygame.draw.circle(screen, (255,255,255), (c*TILE_SIZE,r*TILE_SIZE), 2)
        
        pacman_img = pacman.get_image(nframes)
        screen.blit(pacman_img, (pacman.pos.x*TILE_SIZE, pacman.pos.y*TILE_SIZE))

        blinky_cx = (blinky.pos.x+blinky.size/2)*TILE_SIZE
        blinky_cy = (blinky.pos.y+blinky.size/2)*TILE_SIZE
        pygame.draw.circle(screen, (255,0,0), (blinky_cx, blinky_cy), TILE_SIZE*0.7)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    pacman.next_speed = position.FloatCoord(0,-1)
                elif keys[pygame.K_DOWN]:
                    pacman.next_speed = position.FloatCoord(0,1)
                elif keys[pygame.K_LEFT]:
                    pacman.next_speed = position.FloatCoord(-1,0)
                elif keys[pygame.K_RIGHT]:
                    pacman.next_speed = position.FloatCoord(1,0)

        pacman.update_pos(maze)
        blinky.update_pos(maze, pacman, nframes, frame_rate)

        clock.tick_busy_loop(frame_rate)
        nframes += 1

if __name__ == '__main__':
    main()