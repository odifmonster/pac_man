import turtle
import random
import math
class Wall_Point_2():
    """
    Class that describes a wall point, which is assigned an x value
    a y value, and a list of potential directions for the game's sprites
    to move in.
    """
    def __init__(self, x, y, directions):
        self.x = x
        self.y = y
        self.directions = directions
    def __str__(self):
        return '('+str(self.x)+ ',' + str(self.y)+')'
    def same_point(self, x, y):
        return self.x == x and self.y == y

    
class Wall_Point():
    """
    dated class please ignore
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up = False
        self.right = False
        self.left = False
        self.down = False
    def __str__(self):
        return '('+str(self.x)+ ',' + str(self.y)+')'
    def same_point(self, x, y):
        return self.x == x and self.y == y
all_directions = []
#valid_directions = {origin:['up','down','left','right']}

bg = turtle.Screen()
bg.bgcolor('black')
bg.setup(width=700, height = 800)
bg.tracer(0)


#ghost_colors = ['red', 'orange', 'pink', 'turquosie']

##for i in all_directions:
##    valid_directions[i] = ['up','down','left','right']


pacman = turtle.Turtle()
pacman.speed(0)
pacman.penup()
pacman.color('yellow')
pacman.shape('circle')
pacman.direction = 'stop'
pacman.qdirection = ''
pacman.shapesize (2,2)
pacman.setx(0)
pacman.sety(-100)
timer = 0

ghostlist= []
ghost = turtle.Turtle()
ghost.speed(0)
ghost.color('red')
ghost.shape('square')
ghost.penup()
direction_list = ['up', 'down', 'left', 'right']
ghost.direction = 'up'
ghost.setx(0)
ghost.sety(0)
ghostlist.append(ghost)

ghost2 = turtle.Turtle()
ghost2.speed(0)
ghost2.color('yellow')
ghost2.shape('square')
ghost2.penup()
direction_list = ['up', 'down', 'left', 'right']
ghost2.direction = 'up'
ghost2.setx(0)
ghost2.sety(0)

ghostlist.append(ghost2)

ghost3 = turtle.Turtle()
ghost3.speed(0)
ghost3.color('purple')
ghost3.shape('square')
ghost3.penup()
direction_list = ['up', 'down', 'left', 'right']
ghost3.direction = 'up'
ghost3.setx(0)
ghost3.sety(0)

ghostlist.append(ghost3)


walls = turtle.Turtle()
walls.speed(0)
walls.setx(330)
walls.sety(330)
walls.color('blue')
walls.shape('square')
walls.width(width = 20)
walls.right(90)
walls.forward(660)
walls.right(90)
walls.forward(660)
walls.right(90)
walls.forward(660)
walls.right(90)
walls.forward(660)

walls.penup()
walls.setx(0)
walls.sety(-150)
walls.pendown()
walls.right(90)
walls.forward(100)

walls.penup()
walls.setx(150)
walls.left(90)
walls.pendown()
walls.forward(100)

walls.penup()
walls.sety(-150)
walls.setx(-150)
walls.pendown()
walls.forward(300)
walls.penup()

walls.setx(250)
walls.sety(-150)
walls.left(90)
walls.pendown()
walls.forward(100)
walls.penup()

walls.forward(100)
walls.pendown()
walls.forward(200)
walls.penup()



walls.setx(-150)
walls.sety(-250)
walls.left(90)
walls.pendown()
walls.forward(100)
walls.penup()

walls.right(90)
walls.sety(-150)
walls.pendown()
walls.forward(100)
walls.penup()

walls.forward(100)
walls.pendown()
walls.forward(200)
walls.penup()
walls.backward(100)
walls.right(90)
walls.pendown()
walls.forward(100)
walls.penup()

walls.setx(250)
walls.sety(150)
walls.pendown()
walls.backward(100)
walls.penup()


walls.sety(250)
walls.pendown()
walls.backward(300)
walls.penup()
walls.forward(150)
walls.right(90)
walls.pendown()
walls.forward(100)
walls.penup()
walls.left(90)

walls.setx(-150)
walls.sety(50)
walls.pendown()
walls.forward(300)
walls.right(90)
walls.forward(100)
walls.right(90)
walls.forward(300)
walls.right(90)
walls.forward(100)
walls.penup()
walls.hideturtle()

inverse_directions = {'up':'down', 'right':'left', 'down':'up', 'left': 'right'}
ur = ['up', 'right']
ul = ['up', 'left']
dr = ['down', 'right']
drl = ['down', 'right', 'left']
alld = ['up', 'down', 'right', 'left']
dl = ['down', 'left']
url = ['up', 'right', 'left']
udl = ['up', 'down', 'left']
udr = ['up', 'down', 'right']

wps = []
bleft_corner = Wall_Point_2(-300, -300, ur)
wps.append(bleft_corner)
bright_corner = Wall_Point_2(300, -300, ul)
wps.append(bright_corner)
tright_corner = Wall_Point_2(300, 300, dl)
wps.append(tright_corner)
tleft_corner = Wall_Point_2(-300, 300, dr)
wps.append(tleft_corner)

r11= Wall_Point_2(-200, 300, drl)
wps.append(r11)
r12= Wall_Point_2(200, 300, drl)
wps.append(r12)

r21= Wall_Point_2(-200, 200, ur)
wps.append(r21)
r22= Wall_Point_2(200, 200, ul)
wps.append(r22)

r23= Wall_Point_2(-100, 200, dl)
wps.append(r23)
r24= Wall_Point_2(100, 200, dr)
wps.append(r24)

r31= Wall_Point_2(-200, 100, dr)
wps.append(r31)
r32= Wall_Point_2(200, 100, dl)
wps.append(r32)

r33= Wall_Point_2(-100, 100, url)
wps.append(r33)
r34= Wall_Point_2(100, 100, url)
wps.append(r34)

r41= Wall_Point_2(-300, 0, udr)
wps.append(r41)
r42= Wall_Point_2(300, 0, udl)
wps.append(r42)

r43= Wall_Point_2(-200, 0, udl)
wps.append(r43)
r44= Wall_Point_2(200, 0, udr)
wps.append(r44)

r51= Wall_Point_2(-200, -100, udr)
wps.append(r51)
r52= Wall_Point_2(200, -100, udl)
wps.append(r52)

r61= Wall_Point_2(-200, -200, url)
wps.append(r61)
r62= Wall_Point_2(200, -200, url)
wps.append(r62)

r63= Wall_Point_2(-300, -200, udr)
wps.append(r63)
r64= Wall_Point_2(300, -200, udl)
wps.append(r64)

r65= Wall_Point_2(-100, -200, dl)
wps.append(r65)
r66= Wall_Point_2(100, -200, dr)
wps.append(r66)

r71= Wall_Point_2(-100, -300, url)
wps.append(r71)
r72= Wall_Point_2(100, -300, url)
wps.append(r72)

rfinal = Wall_Point_2(0, -100, ['right', 'left'])
wps.append(rfinal)
point_list = []
for i in range(0, len(wps) - 1):
    t = turtle.Turtle()
    t.penup()
    t.setx(wps[i].x)
    t.sety(wps[i].y)
    t.shape('circle')
    t.color('orange')
    point_list.append(t)
    
def pac_Direction():
    """
    assesses whether or not the inputs given by the arrow keys
    can move pacman in an acceptible direction, and then sets pacman
    to move in that direction if found to be acceptable
    """
    global pac_timer
    global wps
    if pacman.qdirection == 'up'  and pac_timer < 30:
        for point in wps:
            if point.same_point(pacman.xcor(), pacman.ycor()) or pacman.direction == 'down':
                if 'up' in point.directions:
                    pacman.direction = 'up'
    elif pacman.qdirection == 'down' and pac_timer < 30:
        for point in wps:
            if point.same_point(pacman.xcor(), pacman.ycor()) or pacman.direction == 'up':
                if 'down' in point.directions:
                    pacman.direction = 'down'
    elif pacman.qdirection == 'right' and pac_timer < 30:
        for point in wps:
            if point.same_point(pacman.xcor(), pacman.ycor()) or pacman.direction == 'left':
                if 'right' in point.directions:
                    pacman.direction = 'right'
    elif pacman.qdirection == 'left' and pac_timer < 30:
        for point in wps:
            if point.same_point(pacman.xcor(), pacman.ycor()) or pacman.direction == 'right':
                if 'left' in point.directions:
                    pacman.direction = 'left'
    else:
        pacman.qdirection = pacman.direction
        pac_timer = 0


def move_Pac():
    """
    Controls the movement of pacman, will stop pacman's movement if it
    comes into contact with a wall
    """
    global wps
    global rfinal
    if pacman.direction == 'up' and pacman.ycor() < 300:
        same_point = False
        for point in wps:
            
            if point.same_point(pacman.xcor(), pacman.ycor()):
                same_point = True
                
                if 'up' in point.directions:
                    pacman.sety(pacman.ycor() + 1.25)
                #else:
                    #pacman.direction = 'stop'
        if same_point == False:
            pacman.sety(pacman.ycor() + 1.25)
            
    if pacman.direction == 'down' and pacman.ycor()> -300:
        same_point = False
        for point in wps:

            
            if point.same_point(pacman.xcor(), pacman.ycor()):
                same_point = True
                
                if 'down' in point.directions:
                    pacman.sety(pacman.ycor() - 1.25)
                #else:
                    #pacman.direction = 'stop'
                    
        if same_point == False:
            pacman.sety(pacman.ycor() - 1.25)
            
    if pacman.direction == 'right' and pacman.xcor() < 300:

        same_point = False
        for point in wps:
            if point.same_point(pacman.xcor(), pacman.ycor()):
                same_point = True
                if 'right' in point.directions:
                    pacman.setx(pacman.xcor() + 1.25)
                #else:
                    #pacman.direction = 'stop'
        if not same_point:
            pacman.setx(pacman.xcor() + 1.25)
    if pacman.direction == 'left' and pacman.xcor() > -300:
        same_point = False

        for point in wps:
            
            if point.same_point(pacman.xcor(), pacman.ycor()):
                same_point = True
                if 'left' in point.directions:
                    pacman.setx(pacman.xcor() - 1.25)
                #else:
                    #pacman.direction = 'stop'
        if not same_point:
            pacman.setx(pacman.xcor() - 1.25)

def move_Ghost(ghost, time):
    """
    Controls the movements of the Ghosts, which will turn
    at random upon reaching a vertice that enables turns
    """
    global main_game_timer
    global timer
    global direction_list
    global wps
    rl = ['right', 'left']
        
    if main_game_timer == time + 200:
        ghost.direction = rl[random.randint(0,1)]
    if main_game_timer >= time:
        for point in wps:
            if point.same_point(ghost.xcor(), ghost.ycor()):
                ghost.direction = point.directions[random.randint(0,len(point.directions) - 1)]
        if ghost.direction == 'up':
            
            ghost.sety(ghost.ycor() + .5)
            timer+=1
            
        elif ghost.direction == 'down':
           
            ghost.sety(ghost.ycor() - .5)
            timer+=1
            
            
        elif ghost.direction == 'right':
            
            ghost.setx(ghost.xcor() + .5)
            timer+=1
         
            
        if ghost.direction == 'left':

            ghost.setx(ghost.xcor() - .5)
            timer +=1

pac_timer = 0
del_rfinal = False
first_time = True
def up():
    """
    Queues Pacman to move up for the pac_direction function to assess
    """
    global pac_timer
    pac_timer = 0
    pacman.qdirection = 'up'
def down():
    """
    Queues Pacman to move down for the pac_direction function to assess
    """
    global pac_timer
    pac_timer = 0
    pacman.qdirection = 'down'
    
def left():
    """
    Queues Pacman to move left for the pac_direction function to assess
    """
    global pac_timer
    global del_rfinal
    del_rfinal = True
    pac_timer = 0
    pacman.qdirection = 'left'
def right():
    """
    Queues Pacman to move right for the pac_direction function to assess
    """
    global pac_timer
    global del_rfinal
    del_rfinal = True
    pac_timer = 0
    pacman.qdirection = 'right'

def quit_Game():
    """
    Stops the processes of the game
    """
    turtle.done()
turtle.listen()
turtle.onkey(up, 'Up')
turtle.onkey(down, 'Down')
turtle.onkey(right, 'Right')
turtle.onkey(left, 'Left')
turtle.onkey(quit_Game, 'q')
main_game_timer = 0


score = 0
strack = turtle.Turtle()
strack.penup()
strack.setposition(-300,350)
strack.color('blue')
strack.hideturtle()

while True:
    strack.write(str(score),font = ('arial',30,'normal'), align = 'left')
    for g in ghostlist:
        if abs(g.xcor() - pacman.xcor()) < 30 and abs(g.ycor() - pacman.ycor()) < 30:
            turtle.color('red')
            turtle.write("Game Over!", font = ('arial', 100, 'bold'), align = 'center')
            quit_Game()
            
    for p in point_list:
        if abs(p.xcor() - pacman.xcor()) < 30 and abs(p.ycor() - pacman.ycor()) < 30:
            score += 100
            p.hideturtle()
            point_list.remove(p)
            strack.clear()
    
    bg.update()
    pac_Direction()
    move_Pac()
    move_Ghost(ghost, 200)
    move_Ghost(ghost2, 1000)
    move_Ghost(ghost3, 2000)
    main_game_timer+=1
    pac_timer += 1
    
    if first_time and del_rfinal:
        wps.remove(rfinal)
        first_time = False

    

