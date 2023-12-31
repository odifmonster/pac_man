#!/usr/bin/env python
from enum import Enum, auto

import pygame
from structures import agent, maze as m, position as pos

class AppMode(Enum):
    MENU = auto()
    START_UP = auto()
    PLAY = auto()
    END = auto()

class GameMode(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHT = auto()
    DEATH = auto()

class Game:
    """
    A class to handle game logic and store information about the game state.
    """

    def __init__(self) -> None:
        # TODO: Implement constructor
        self.mode = GameMode.SCATTER

        self.maze = m.Maze()

        self.player = agent.Player()
        self.blinky, self.pinky, self.inky, self.clyde = agent.Enemy(), agent.Enemy(), agent.Enemy(), agent.Enemy()
    
    def ghosts(self) -> list[agent.Enemy]:

        return [self.blinky, self.pinky, self.inky, self.clyde]
    
    def update_objects(self, events: list[pygame.event.Event], keys: pygame.key.ScancodeWrapper) -> None:
        # TODO: Implement update method
        pass

    def reset(self) -> None:
        # TODO: Implement reset method
        pass

class Graphics:
    """A class for handling game graphics."""

    def __init__(self) -> None:
        # TODO: Implement
        pass

    def draw_menu(self, screen: pygame.Surface) -> None:
        # TODO: Implement
        pass

    def draw_objects(self, screen: pygame.Surface) -> None:
        # TODO: Implement
        pass

class Sounds:
    """A class for handling game sound effects."""

    def __init__(self) -> None:
        # TODO: Implement
        pass

    def play_menu(self) -> None:
        # TODO: Implement
        pass

    def play_startup(self) -> None:
        # TODO: Implement
        pass

    def update_game_sounds(self) -> None:
        # TODO: Implement
        pass

def main() -> None:
    print('Running the main function...')

    pygame.init()
    screen = pygame.display.set_mode((200,200))
    mode = AppMode.MENU

    game = Game()
    gfx = Graphics()
    sfx = Sounds()

    running = True
    while running:

        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        match mode:
            case AppMode.MENU:
                # TODO: Implement menu
                gfx.draw_menu(screen)
                sfx.play_menu()
            case AppMode.START_UP:
                # TODO: Implement start-up
                gfx.draw_objects(screen)
                sfx.play_startup()
            case AppMode.PLAY:
                # TODO: Implement game-play
                game.update_objects(events, keys)
                gfx.draw_objects(screen)
                sfx.update_game_sounds()
            case AppMode.END:
                # TODO: Implement game over
                print('This is game over mode.')
        
        pygame.display.flip()
        
        for e in events:
            if e.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()