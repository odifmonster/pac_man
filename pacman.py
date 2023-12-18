#!/usr/bin/env python
import maze

def main():
    m = maze.Maze()
    m.init()

    print('It\'s pacman time! Here is the pacman maze:')
    print(m)

if __name__ == '__main__':
    main()