#!/usr/bin/env python
import os
import math
import pygame, pygame.gfxdraw

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
GHOST_DIRS = ['blinky', 'pinky', 'inky', 'clyde']

GHOST_SIZE = 20*2
SIZE_FACT = 0.9
GHOST_COLORS = [(255,0,0), (255,192,255), (255,176,64), (0,224,255)]

def ghost_waves(ndiv=50):
    xoffset = GHOST_SIZE*(1-SIZE_FACT)/2+1
    dx = GHOST_SIZE*SIZE_FACT-2

    waveh = GHOST_SIZE*(2*SIZE_FACT-1)/4
    yoffset = GHOST_SIZE*3/4+waveh/2

    t_vals = [i/ndiv for i in range(ndiv+1)]
    x = [xoffset] + [xoffset+dx*t for t in t_vals] + [xoffset+dx]
    y0 = [yoffset-(waveh/2)*math.cos(6*math.pi*t) for t in t_vals]
    y1 = [yoffset-(waveh/2)*math.cos(6*math.pi*t+math.pi) for t in t_vals]

    return x, [GHOST_SIZE/2] + y0 + [GHOST_SIZE/2] , [GHOST_SIZE/2] + y1 + [GHOST_SIZE/2]

def ghost_eyes(wfact, hfact, pfact, xoff, yoff):
    eyew, eyeh = (GHOST_SIZE/4)*wfact, (GHOST_SIZE/4)*hfact
    pw, ph = eyew*pfact, eyeh*pfact

    exl = [GHOST_SIZE*(2-SIZE_FACT)/4-eyew/2] * 4
    exl[1] += GHOST_SIZE*xoff/3+1
    exl[3] -= GHOST_SIZE*xoff/4+1
    exr = [GHOST_SIZE*(2+SIZE_FACT)/4-eyew/2] * 4
    exr[1] += GHOST_SIZE*xoff/4+1
    exr[3] -= GHOST_SIZE*xoff/3+1

    ey = [GHOST_SIZE/2-eyeh/2] * 4
    ey[0] -= GHOST_SIZE*yoff/4
    ey[2] += GHOST_SIZE*yoff/10

    pxl = [exl[0]+eyew/2-pw/2, exl[1]+eyew-pw, exl[2]+eyew/2-pw/2, exl[3]]
    pxr = [exr[0]+eyew/2-pw/2, exr[1]+eyew-pw, exr[2]+eyew/2-pw/2, exr[3]]

    py = [ey[0], ey[1]+eyeh/2-ph/2, ey[2]+eyeh-ph, ey[3]+eyeh/2-ph/2]

    return (list(zip(exl, ey, [eyew]*4, [eyeh]*4)),
            list(zip(exr, ey, [eyew]*4, [eyeh]*4)), 
            list(zip(pxl, py, [pw]*4, [ph]*4)),
            list(zip(pxr, py, [pw]*4, [ph]*4)))

def main():

    pygame.init()

    screen = pygame.display.set_mode((GHOST_SIZE, GHOST_SIZE))

    px, py0, py1 = ghost_waves()
    wave0 = list(zip(px,py0))
    wave1 = list(zip(px,py1))

    lt_eye, rt_eye, lt_pl, rt_pl = ghost_eyes(0.9, 1.2, 0.6, 0.2, 0.6)

    running = True
    nframes = 0
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0,0,0,0))

        color_ind = nframes // (2400) % 4
        pygame.draw.circle(screen, GHOST_COLORS[color_ind],
                           (GHOST_SIZE/2, GHOST_SIZE/2), (GHOST_SIZE/2)*SIZE_FACT-1,
                           draw_top_right=True, draw_top_left=True)
        
        if (nframes // 300) % 2 == 0:
            pygame.gfxdraw.filled_polygon(screen, wave0, GHOST_COLORS[color_ind])
        else:
            pygame.gfxdraw.filled_polygon(screen, wave1, GHOST_COLORS[color_ind])
        
        eye_ind = nframes // (600) % 4
        pygame.draw.ellipse(screen, (255,255,255), lt_eye[eye_ind])
        pygame.draw.ellipse(screen, (255,255,255), rt_eye[eye_ind])
        pygame.draw.ellipse(screen, (0,0,255), lt_pl[eye_ind])
        pygame.draw.ellipse(screen, (0,0,255), rt_pl[eye_ind])
        
        pygame.display.flip()

        if nframes % 300 == 0:
            angle = ((9-eye_ind) % 4)*90
            wave = (nframes // 300) % 2
            ghost_dir = GHOST_DIRS[color_ind]
            fname = f'a{angle:03}_w{wave}.png'
            pygame.image.save(screen, os.path.join(SCRIPT_DIR, ghost_dir, fname))

        nframes += 1

if __name__ == '__main__':
    main()