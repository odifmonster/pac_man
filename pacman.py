#!/usr/bin/env python
import os
import pygame, simpleaudio as sa

from structures import maze as mz, position as pos, agent

# ================== GLOBAL CONSTANTS ==================
DEBUG = True
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TILE_SIZE = 20
DOT_COLOR = (255,255,255)

# ================== GLOBAL VARIABLES ==================
maze, pacman, blinky = None, None, None

# ================== HELPER FUNCTIONS ==================
def init_game_objects():
    global maze, pacman, blinky
    maze = mz.Maze()
    maze.init()

    pacman = agent.Player((maze.ncols//2-1,maze.nrows-8), (1,0), 0.15)
    pacman.pos.x += 0.5

    blinky = agent.Enemy(os.path.join(SCRIPT_DIR, 'gfx', 'blinky'), (maze.ncols//2-1,11), (1,0), 0.15)
    blinky.pos.x += 0.5

# ================== MAIN FUNCTION ==================
def main():

    init_game_objects()

    pygame.init()
    screen = pygame.display.set_mode((maze.ncols*TILE_SIZE, maze.nrows*TILE_SIZE))
    clock = pygame.time.Clock()
    frame_rate = 60

    maze_img = pygame.image.load(os.path.join(SCRIPT_DIR, 'gfx','maze_sqr.png'))

    waka = sa.WaveObject.from_wave_file(os.path.join(SCRIPT_DIR, 'sfx', 'waka.wav'))
    play_waka = waka.play()
    play_waka.stop()

    running = True
    nframes = 0
    while running:

        # GRAPHICS
        screen.blit(maze_img, (0,0))

        for r in range(maze.nrows):
            for c in range(maze.ncols):
                
                if maze.get_tile(pos.ListCoord(x=c,y=r)) == mz.Tile.DOT:
                    pygame.draw.circle(screen, DOT_COLOR,
                                       ((c+0.5)*TILE_SIZE, (r+0.5)*TILE_SIZE), 2)
        
        pm_tl = pacman.get_tl()
        pm_img = pygame.transform.rotate(pacman.get_image(nframes),
                                         pos.get_dir_angle(pacman.speed_vec.get_direction()))
        screen.blit(pm_img, (pm_tl.x*TILE_SIZE, pm_tl.y*TILE_SIZE))

        bk_tl = blinky.get_tl()
        bk_img = blinky.get_image(nframes, frame_rate*2)
        screen.blit(bk_img, (bk_tl.x*TILE_SIZE, bk_tl.y*TILE_SIZE))

        pygame.display.flip()
        clock.tick(frame_rate)
        nframes += 1

        # SFX
        if pacman.eating and not play_waka.is_playing():
            play_waka = waka.play()
        elif not pacman.eating:
            play_waka.stop()

        # GAME LOGIC
        if nframes >= frame_rate*2:
            pacman.update_pos(maze)
            blinky.update_speed(maze, pacman)
            blinky.move(maze)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and nframes >= frame_rate*2:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP]:
                    pacman.next_speed = pos.FloatCoord(dir=pos.Direction.N)
                elif keys[pygame.K_RIGHT]:
                    pacman.next_speed = pos.FloatCoord(dir=pos.Direction.E)
                elif keys[pygame.K_DOWN]:
                    pacman.next_speed = pos.FloatCoord(dir=pos.Direction.S)
                elif keys[pygame.K_LEFT]:
                    pacman.next_speed = pos.FloatCoord(dir=pos.Direction.W)

if __name__ == '__main__':
    main()