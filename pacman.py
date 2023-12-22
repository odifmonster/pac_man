#!/usr/bin/env python
import os
import pygame, simpleaudio as sa, math
from enum import Enum

from structures import maze as mz, position as pos, agent

# ================== GLOBAL CONSTANTS ==================
DEBUG = False
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class GhostMode(Enum):
    CHASE, SCATTER = 0, 1

class Game:

    def __init__(self) -> None:

        # game constants
        self.GAME_FONT_PATH = os.path.join(os.path.expanduser('~'), 'Library', 'Fonts', 'ARCADECLASSIC.TTF')
        self.TILE_SIZE = 20
        self.DOT_COLOR = (255, 255, 255)

        # other game values
        self.initialized = False
        self.MODES = list(GhostMode)
        self.mode_ind = 1
        self.mode_changes = [7, 27, 34, 54, 59, 79, 84, math.inf]
        self.next_mode_change = 0

        # game objects
        self.maze, self.pacman = None, None
        self.blinky, self.pinky, self.inky = None, None, None

        # pygame
        self.score_rows = 3
        self.screen, self.clock = None, None
        self.nframes, self.frame_rate = 0, 60
        self.running, self.playing = False, False
        self.start_frame = 1

        # other gfx
        self.game_font_lg, self.game_over = None, None
        self.game_font_md, self.score_label, self.score = None, None, None
        self.maze_img = None
        self.pm_img = None
        self.bk_img, self.pk_img, self.nk_img = None, None, None
        self.death_start, self.death_end = -1, -1

        # sfx
        self.start_sound, self.play_start = None, None
        self.waka, self.play_waka = None, None
        self.death, self.play_death = None, None
        self.sirens, self.play_siren = None, None
        self.siren_changes = [7, 34, 59, 84, math.inf]
        self.next_siren_change = 0
    
    def _init_game_objects(self) -> None:

        self.maze = mz.Maze()
        self.maze.init()

        self.pacman = agent.Player(os.path.join(SCRIPT_DIR, 'gfx', 'pacman'),
                                   (self.maze.ncols//2-1,self.maze.nrows-8),
                                   speed_vec=(1,0),
                                   speed_norm=0.15)
        self.pacman.pos.x += 0.5

        self.blinky = agent.Enemy(os.path.join(SCRIPT_DIR, 'gfx', 'blinky'),
                                  (self.maze.ncols//2-1,11),
                                  speed_vec=(1,0),
                                  speed_norm=0.15)
        self.blinky.pos.x += 0.5
        self.blinky.at_home = False
        self.blinky.waiting = False
        self.blinky.passable_tiles = [mz.Tile.EMPTY, mz.Tile.DOT]

        self.pinky = agent.Enemy(os.path.join(SCRIPT_DIR, 'gfx', 'pinky'),
                                 (self.maze.ncols//2-1,14),
                                 speed_vec=(0,-1),
                                 speed_norm=0.15)
        self.pinky.pos.x += 0.5
        self.pinky.waiting = False

        self.inky = agent.Enemy(os.path.join(SCRIPT_DIR, 'gfx', 'inky'),
                                (self.maze.ncols//2-2,14),
                                speed_vec=(0,-1),
                                speed_norm=0.15)
        self.inky.pos.x -= 0.5
        self.inky.pos.y -= 0.5
        self.inky.target = pos.ListCoord(0, self.maze.nrows-1)
    
    def _init_gfx(self) -> None:

        self.screen = pygame.display.set_mode((self.maze.ncols*self.TILE_SIZE,
                                               (self.maze.nrows+self.score_rows)*self.TILE_SIZE))
        self.clock = pygame.time.Clock()

        self.game_font_lg = pygame.font.Font(self.GAME_FONT_PATH, self.TILE_SIZE*2)
        self.game_font_md = pygame.font.Font(self.GAME_FONT_PATH, self.TILE_SIZE)
        self.game_over = self.game_font_lg.render('GAME OVER', False, (255,255,255))
        self.score_label = self.game_font_md.render('SCORE', False, (255,255,255))

        self.maze_img = pygame.image.load(os.path.join(SCRIPT_DIR, 'gfx', 'maze_sqr.png'))
        self.pm_img = self.pacman.mimages[-1]
        self.bk_img = self.blinky.images[0][0]
        self.pk_img = self.pinky.images[1][0]
        self.nk_img = self.inky.images[3][0]
    
    def _init_sfx(self) -> None:

        self.start_sound = sa.WaveObject.from_wave_file(os.path.join(SCRIPT_DIR, 'sfx', 'start_up.wav'))
        self.waka = sa.WaveObject.from_wave_file(os.path.join(SCRIPT_DIR, 'sfx', 'waka.wav'))
        self.death = sa.WaveObject.from_wave_file(os.path.join(SCRIPT_DIR, 'sfx', 'death.wav'))
        self.sirens = [sa.WaveObject.from_wave_file(os.path.join(SCRIPT_DIR, 'sfx', f'siren_{i+1}.wav'))
                       for i in range(5)]
        
        self.play_start = sa.PlayObject(0)
        self.play_waka = sa.PlayObject(0)
        self.play_death = sa.PlayObject(0)
        self.play_siren = sa.PlayObject(0)
    
    def init(self) -> None:

        pygame.init()

        self._init_game_objects()
        self._init_gfx()
        self._init_sfx()

        self.running = True
        self.playing = True
        self.initialized = True
    
    def get_mode(self) -> GhostMode:
        return self.MODES[self.mode_ind]
    
    def update_agent_imgs(self) -> None:

        if not self.initialized:
            RuntimeError('Game not yet initialized, draw methods unavailable.')

        if self.playing:
            self.pm_img = pygame.transform.rotate(self.pacman.get_move_image(self.nframes),
                                                  pos.get_dir_angle(self.pacman.speed_vec.get_direction()))
            self.bk_img = self.blinky.get_image(self.nframes, self.start_frame)
            self.pk_img = self.pinky.get_image(self.nframes, self.start_frame)
            self.nk_img = self.inky.get_image(self.nframes, self.start_frame)
        elif not self.playing and self.death_end == -1:
            self.bk_img = pygame.Surface((1,1))
            self.pk_img = pygame.Surface((1,1))
            self.nk_img = pygame.Surface((1,1))
            self.pm_img = self.pacman.get_death_image(self.nframes, self.death_start)

            if not self.pm_img:
                self.pm_img = pygame.Surface((1,1))
                self.death_end = self.nframes
            
            self.pm_img = pygame.transform.rotate(self.pm_img,
                                                  pos.get_dir_angle(self.pacman.speed_vec.get_direction()))
    
    def draw_game_objects(self) -> None:
        
        if not self.initialized:
            raise RuntimeError('Game not yet initialized, draw methods unavailable.')
        
        self.screen.fill((0,0,0))

        offset = pos.FloatCoord(x=0, y=self.score_rows*self.TILE_SIZE)
        
        self.score = self.game_font_md.render(str(self.pacman.score), False, (255,255,255))
        self.screen.blit(self.score_label, (1,1))
        self.screen.blit(self.score, (1, self.TILE_SIZE+1))

        self.screen.blit(self.maze_img, offset.get_tuple())

        for r in range(self.maze.nrows):
            for c in range(self.maze.ncols):

                if self.maze.get_tile(pos.ListCoord(x=c, y=r)) == mz.Tile.DOT:
                    pygame.draw.circle(self.screen, self.DOT_COLOR,
                                       ((c+0.5)*self.TILE_SIZE, (r+self.score_rows+0.5)*self.TILE_SIZE), 2)
    
        pm_pos = self.pacman.get_tl()*self.TILE_SIZE + offset
        self.screen.blit(self.pm_img, pm_pos.get_tuple())
        bk_pos = self.blinky.get_tl()*self.TILE_SIZE + offset
        self.screen.blit(self.bk_img, bk_pos.get_tuple())
        pk_pos = self.pinky.get_tl()*self.TILE_SIZE + offset
        self.screen.blit(self.pk_img, pk_pos.get_tuple())
        nk_pos = self.inky.get_tl()*self.TILE_SIZE + offset
        self.screen.blit(self.nk_img, nk_pos.get_tuple())
    
    def draw_game_over(self) -> None:

        x = (self.screen.get_width()-self.game_over.get_width())/2
        y = (self.screen.get_height()-self.game_over.get_height())/2
        self.screen.blit(self.game_over, (x,y))
    
    def handle_events(self) -> None:

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_UP]:
                        self.pacman.next_speed = pos.FloatCoord(dir=pos.Direction.N)
                    if keys[pygame.K_DOWN]:
                        self.pacman.next_speed = pos.FloatCoord(dir=pos.Direction.S)
                    if keys[pygame.K_LEFT]:
                        self.pacman.next_speed = pos.FloatCoord(dir=pos.Direction.W)
                    if keys[pygame.K_RIGHT]:
                        self.pacman.next_speed = pos.FloatCoord(dir=pos.Direction.E)
    
    def start_death_sequence(self) -> None:

        if not self.initialized:
            raise RuntimeError('Game not yet initialized, method start_death_sequence unavailable.')

        pygame.time.delay(500)

        self.pacman.eating = False
        self.pacman.chomp_rate = 8
        self.death_start = self.nframes
        self.playing = False
        self.play_death = self.death.play()

# ================== MAIN FUNCTION ==================
def main():
        
    game = Game()
    game.init()
    game.play_start = game.start_sound.play()

    while game.running:

        game.update_agent_imgs()
        game.draw_game_objects()

        if not game.playing and game.death_end != -1:
            game.draw_game_over()

        game.clock.tick(game.frame_rate)
        game.nframes += 1
        pygame.display.flip()

        if game.play_start.is_playing():
            game.play_start.wait_done()

        # SFX
        if game.playing and not game.play_siren.is_playing():
            game.play_siren = game.sirens[game.next_siren_change].play()
        if game.next_siren_change < len(game.siren_changes) \
            and game.nframes >= game.siren_changes[game.next_siren_change]*game.frame_rate:
            game.play_siren.stop()
            game.next_siren_change += 1
            game.play_siren = game.sirens[game.next_siren_change].play()
        if game.pacman.eating and not game.play_waka.is_playing():
            game.play_waka = game.waka.play()
        elif not game.pacman.eating and game.play_waka.is_playing():
            game.play_waka.stop()

        # GAME LOGIC
        if game.playing:
            game.pacman.update_pos(game.maze)

            if game.get_mode() == GhostMode.CHASE:
                game.blinky.target = game.pacman.list_pos
                game.pinky.target = pos.ListCoord(coord=game.pacman.pos+game.pacman.speed_vec*4)
            else:
                game.blinky.target = pos.ListCoord(game.maze.ncols-1, -1)
                game.pinky.target = pos.ListCoord(0, -1)

            game.blinky.update_speed(game.maze)
            game.blinky.move(game.maze)
            game.pinky.update_speed(game.maze)
            game.pinky.move(game.maze)

            if game.next_mode_change < len(game.mode_changes) \
                and game.nframes >= game.frame_rate*game.mode_changes[game.next_mode_change]:
                game.mode_ind = (game.mode_ind+1) % 2
                game.next_mode_change += 1
            if game.blinky.pos.dist_from(game.pacman.pos) <= 0.5 \
                or game.pinky.pos.dist_from(game.pacman.pos) <= 0.5:
                game.start_death_sequence()

        game.handle_events()

if __name__ == '__main__':
    main()